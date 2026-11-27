import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from schema_validate import SchemaError, validate


class SchemaValidateTests(unittest.TestCase):
    def test_rejects_unknown_property(self):
        schema = {
            "type": "object",
            "required": ["state"],
            "properties": {"state": {"enum": ["ready", "blocked"]}},
            "additionalProperties": False,
        }
        with self.assertRaisesRegex(SchemaError, r"\$\.extra"):
            validate({"state": "ready", "extra": 1}, schema)

    def test_rejects_unsupported_keyword(self):
        with self.assertRaisesRegex(SchemaError, "不支持的 Schema 关键字"):
            validate("x", {"type": "string", "format": "date-time"})

    def test_resolves_local_defs(self):
        schema = {
            "$defs": {"id": {"type": "string", "pattern": "^[a-z0-9-]+$"}},
            "$ref": "#/$defs/id",
        }
        validate("gk-2021-x2", schema)

    def test_rejects_unsupported_keyword_in_unvisited_branch(self):
        schema = {
            "type": "object",
            "properties": {"optional": {"type": "string", "maxLength": 3}},
        }
        with self.assertRaisesRegex(SchemaError, "不支持的 Schema 关键字"):
            validate({}, schema)

    def test_boolean_is_not_an_integer_or_number(self):
        with self.assertRaisesRegex(SchemaError, "类型"):
            validate(True, {"type": ["integer", "number"]})

    def test_rejects_unknown_type_and_broken_ref_as_schema_errors(self):
        with self.assertRaisesRegex(SchemaError, "不支持的类型"):
            validate("x", {"type": "date"})
        with self.assertRaisesRegex(SchemaError, r"\$ref"):
            validate("x", {"$ref": "#/$defs/missing", "$defs": {}})

    def test_one_of_requires_exactly_one_branch(self):
        schema = {"oneOf": [{"type": "number"}, {"type": "integer"}]}
        with self.assertRaisesRegex(SchemaError, "恰好命中一项"):
            validate(1, schema)

    def test_recursive_json_equality_distinguishes_booleans_from_numbers(self):
        const_schema = {"const": {"nested": [1, {"value": True}]}}
        with self.assertRaisesRegex(SchemaError, "必须等于"):
            validate({"nested": [1, {"value": 1}]}, const_schema)

        enum_schema = {"enum": [{"nested": [False]}]}
        with self.assertRaisesRegex(SchemaError, "enum"):
            validate({"nested": [0]}, enum_schema)

    def test_recursive_json_equality_compares_numbers_mathematically(self):
        validate({"nested": [1.0, {"value": 2}]}, {
            "const": {"nested": [1, {"value": 2.0}]},
        })
        validate({"nested": [1.0]}, {"enum": [{"nested": [1]}]})

    def test_unique_items_uses_json_numeric_equality(self):
        with self.assertRaisesRegex(SchemaError, "不唯一"):
            validate([1, 1.0], {"type": "array", "uniqueItems": True})

    def test_one_of_counts_recursively_equal_const_branches(self):
        schema = {
            "oneOf": [
                {"const": {"nested": [1]}},
                {"const": {"nested": [1.0]}},
            ],
        }
        with self.assertRaisesRegex(SchemaError, "恰好命中一项.*2"):
            validate({"nested": [1]}, schema)

    def test_ref_siblings_still_apply(self):
        schema = {
            "$defs": {"anything": {}},
            "$ref": "#/$defs/anything",
            "type": "string",
        }
        with self.assertRaisesRegex(SchemaError, "类型"):
            validate(1, schema)

    def test_malformed_supported_keyword_fails_as_schema_error(self):
        with self.assertRaisesRegex(SchemaError, "minimum"):
            validate(1, {"type": "integer", "minimum": "zero"})
