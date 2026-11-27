from __future__ import annotations

import re
from typing import Any, Mapping

SUPPORTED = {
    "$schema", "$id", "$defs", "$ref", "type", "required", "properties",
    "items", "contains", "enum", "const", "pattern", "minimum", "minItems", "maxItems",
    "uniqueItems", "additionalProperties", "oneOf", "allOf",
    "description", "title", "default",
}

TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


class SchemaError(ValueError):
    pass


def validate(instance: Any, schema: Mapping[str, Any]) -> None:
    if not isinstance(schema, Mapping):
        raise SchemaError("$: Schema 必须是对象")
    _check_schema(schema, schema, "$", set())
    _validate(instance, schema, schema, "$")


def _check_schema(
    schema: Mapping[str, Any],
    root: Mapping[str, Any],
    path: str,
    ancestors: set,
) -> None:
    identity = id(schema)
    if identity in ancestors:
        raise SchemaError(f"{path}: 不支持递归 Schema")
    ancestors = set(ancestors)
    ancestors.add(identity)
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise SchemaError(f"{path}: 不支持的 Schema 关键字：{sorted(unknown)}")

    expected = schema.get("type")
    if expected is not None:
        allowed = expected if isinstance(expected, list) else [expected]
        if not allowed or not all(isinstance(item, str) and item in TYPE_MAP for item in allowed):
            raise SchemaError(f"{path}: 不支持的类型：{expected!r}")
        if len(allowed) != len(set(allowed)):
            raise SchemaError(f"{path}: type 中存在重复项")

    for keyword in ("$defs", "properties"):
        children = schema.get(keyword, {})
        if not isinstance(children, Mapping):
            raise SchemaError(f"{path}.{keyword}: 必须是对象")
        for name, child in children.items():
            if not isinstance(child, Mapping):
                raise SchemaError(f"{path}.{keyword}.{name}: Schema 必须是对象")
            _check_schema(child, root, f"{path}.{keyword}.{name}", ancestors)

    if "items" in schema:
        child = schema["items"]
        if not isinstance(child, Mapping):
            raise SchemaError(f"{path}.items: Schema 必须是对象")
        _check_schema(child, root, f"{path}.items", ancestors)

    if "contains" in schema:
        child = schema["contains"]
        if not isinstance(child, Mapping):
            raise SchemaError(f"{path}.contains: Schema 必须是对象")
        _check_schema(child, root, f"{path}.contains", ancestors)

    for keyword in ("oneOf", "allOf"):
        branches = schema.get(keyword, [])
        if not isinstance(branches, list) or not branches:
            if keyword in schema:
                raise SchemaError(f"{path}.{keyword}: 必须是非空数组")
            continue
        for index, branch in enumerate(branches):
            if not isinstance(branch, Mapping):
                raise SchemaError(f"{path}.{keyword}[{index}]: Schema 必须是对象")
            _check_schema(branch, root, f"{path}.{keyword}[{index}]", ancestors)

    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, (bool, Mapping)):
        raise SchemaError(f"{path}.additionalProperties: 必须是布尔值或对象")
    if isinstance(additional, Mapping):
        _check_schema(additional, root, f"{path}.additionalProperties", ancestors)

    if "$ref" in schema:
        target = _resolve_ref(root, schema["$ref"])
        _check_schema(target, root, f"{path}.$ref", ancestors)

    if "required" in schema and (
        not isinstance(schema["required"], list)
        or not all(isinstance(item, str) for item in schema["required"])
    ):
        raise SchemaError(f"{path}.required: 必须是字符串数组")
    if "enum" in schema and not isinstance(schema["enum"], list):
        raise SchemaError(f"{path}.enum: 必须是数组")
    if "minimum" in schema and (
        isinstance(schema["minimum"], bool)
        or not isinstance(schema["minimum"], (int, float))
    ):
        raise SchemaError(f"{path}.minimum: 必须是数值")
    for keyword in ("minItems", "maxItems"):
        if keyword in schema and (
            isinstance(schema[keyword], bool)
            or not isinstance(schema[keyword], int)
            or schema[keyword] < 0
        ):
            raise SchemaError(f"{path}.{keyword}: 必须是非负整数")
    if (
        "minItems" in schema and "maxItems" in schema
        and schema["minItems"] > schema["maxItems"]
    ):
        raise SchemaError(f"{path}: minItems 不得大于 maxItems")
    if "uniqueItems" in schema and not isinstance(schema["uniqueItems"], bool):
        raise SchemaError(f"{path}.uniqueItems: 必须是布尔值")
    if "pattern" in schema:
        try:
            re.compile(schema["pattern"])
        except (re.error, TypeError) as error:
            raise SchemaError(f"{path}.pattern: 非法正则表达式：{error}") from error


def _resolve_ref(root: Mapping[str, Any], ref: Any) -> Mapping[str, Any]:
    if not isinstance(ref, str) or not ref.startswith("#/"):
        raise SchemaError(f"只支持本地 $ref：{ref}")
    node: Any = root
    try:
        for part in ref[2:].split("/"):
            key = part.replace("~1", "/").replace("~0", "~")
            if not isinstance(node, Mapping):
                raise KeyError(key)
            node = node[key]
    except KeyError as error:
        raise SchemaError(f"$ref 目标不存在：{ref}") from error
    if not isinstance(node, Mapping):
        raise SchemaError(f"$ref 目标不是对象：{ref}")
    return node


def _matches_type(value: Any, expected: str) -> bool:
    if expected in {"integer", "number"} and isinstance(value, bool):
        return False
    return isinstance(value, TYPE_MAP[expected])


def _json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if (
        isinstance(left, (int, float))
        and isinstance(right, (int, float))
    ):
        return left == right
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            _json_equal(left_item, right_item)
            for left_item, right_item in zip(left, right)
        )
    if isinstance(left, dict) and isinstance(right, dict):
        return set(left) == set(right) and all(
            _json_equal(left[key], right[key]) for key in left
        )
    return type(left) is type(right) and left == right


def _validate(value: Any, schema: Mapping[str, Any], root: Mapping[str, Any], path: str) -> None:
    if "$ref" in schema:
        _validate(value, _resolve_ref(root, schema["$ref"]), root, path)

    for branch in schema.get("allOf", []):
        _validate(value, branch, root, path)

    if "oneOf" in schema:
        passed = 0
        for branch in schema["oneOf"]:
            try:
                _validate(value, branch, root, path)
                passed += 1
            except SchemaError:
                pass
        if passed != 1:
            raise SchemaError(f"{path}: oneOf 应恰好命中一项，实际 {passed}")

    expected = schema.get("type")
    if expected is not None:
        allowed = expected if isinstance(expected, list) else [expected]
        if not any(_matches_type(value, item) for item in allowed):
            raise SchemaError(f"{path}: 类型应为 {allowed}")

    if "enum" in schema and not any(_json_equal(value, item) for item in schema["enum"]):
        raise SchemaError(f"{path}: 值不在 enum 中")
    if "const" in schema and not _json_equal(value, schema["const"]):
        raise SchemaError(f"{path}: 值必须等于 {schema['const']!r}")
    if isinstance(value, str) and "pattern" in schema and not re.search(schema["pattern"], value):
        raise SchemaError(f"{path}: 字符串不匹配 {schema['pattern']}")
    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and "minimum" in schema
        and value < schema["minimum"]
    ):
        raise SchemaError(f"{path}: 数值小于 minimum")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise SchemaError(f"{path}: 数组长度不足")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise SchemaError(f"{path}: 数组长度超限")
        if schema.get("uniqueItems"):
            for index, item in enumerate(value):
                if any(_json_equal(item, prior) for prior in value[:index]):
                    raise SchemaError(f"{path}: 数组元素不唯一")
        if "items" in schema:
            for index, item in enumerate(value):
                _validate(item, schema["items"], root, f"{path}[{index}]")
        if "contains" in schema:
            matched = False
            for index, item in enumerate(value):
                try:
                    _validate(item, schema["contains"], root, f"{path}[{index}]")
                except SchemaError:
                    continue
                matched = True
                break
            if not matched:
                raise SchemaError(f"{path}: contains 未命中任何数组元素")

    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                raise SchemaError(f"{path}.{name}: 缺少必填字段")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for name, child in value.items():
            if name in properties:
                _validate(child, properties[name], root, f"{path}.{name}")
            elif additional is False:
                raise SchemaError(f"{path}.{name}: 未知字段")
            elif isinstance(additional, Mapping):
                _validate(child, additional, root, f"{path}.{name}")
