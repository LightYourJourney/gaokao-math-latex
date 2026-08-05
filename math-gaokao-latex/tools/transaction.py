from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import unicodedata
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Type

from manifest import canonical_json, durable_fsync

MANIFEST_TARGET = "math-gaokao-latex/source-manifest.json"
TRANSACTIONS_RELATIVE = Path("math-gaokao-latex/.work/transactions")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
STAGED_PATTERN = re.compile(r"^target-[0-9]{4}\.bin$")
# 四位 staged 索引覆盖 0000 至 9999，因此单个事务最多包含 10000 个目标。
MAX_TARGET_COUNT = 10000
EventHook = Optional[Callable[[str, Path], None]]
ErrorType = Type[Exception]

_NOFOLLOW = getattr(os, "O_NOFOLLOW", None)
if _NOFOLLOW is None:
    raise RuntimeError("当前平台不支持 O_NOFOLLOW，拒绝启用事务写入")
_DIRECTORY_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | _NOFOLLOW
_FILE_READ_FLAGS = os.O_RDONLY | _NOFOLLOW
_FILE_WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | _NOFOLLOW


def _repository_root(path: Path) -> Path:
    path = Path(path).resolve()
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return Path(result.stdout.strip()).resolve()


def _repo_relative_path(raw: str) -> Path:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise ValueError(f"非法仓库相对路径：{raw!r}")
    path = Path(raw)
    if not path.parts or path.is_absolute() or raw.startswith("/") or any(
        part in {"", ".", ".."} for part in path.parts
    ):
        raise ValueError(f"非法仓库相对路径：{raw!r}")
    return path


def _validate_target_count(count: int, error_type: ErrorType) -> None:
    if count > MAX_TARGET_COUNT:
        raise error_type(
            f"事务目标数量不得超过 {MAX_TARGET_COUNT}，实际 {count}"
        )


def _path_key(path: Path) -> Tuple[str, ...]:
    return tuple(
        unicodedata.normalize(
            "NFC", unicodedata.normalize("NFC", part).casefold()
        )
        for part in path.parts
    )


def _is_protocol_or_git_path(path: Path) -> bool:
    parts = _path_key(path)
    protocol = _path_key(TRANSACTIONS_RELATIVE)
    return parts[:len(protocol)] == protocol or ".git" in parts


def _validated_repo_relative(raw: str, error_type: ErrorType) -> Path:
    try:
        path = _repo_relative_path(raw)
    except ValueError as error:
        raise error_type(str(error)) from error
    if _is_protocol_or_git_path(path):
        raise error_type(f"保留路径不得作为事务输入或目标：{path.as_posix()}")
    return path


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _emit(event_hook: EventHook, event: str, path: Path) -> None:
    if event_hook is not None:
        event_hook(event, path)


def _raise_component_error(
    error_type: ErrorType,
    path: Path,
    component: Path,
    parent_fd: int,
    name: str,
    error: OSError,
) -> None:
    try:
        status = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except OSError:
        status = None
    if status is not None and stat.S_ISLNK(status.st_mode):
        raise error_type(f"路径包含符号链接：{component}（完整路径 {path}）") from error
    if status is not None and not stat.S_ISDIR(status.st_mode):
        raise error_type(f"路径组件不是目录：{component}（完整路径 {path}）") from error
    raise error_type(f"无法安全打开路径组件 {component}（完整路径 {path}）：{error}") from error


def _open_root(root: Path, error_type: ErrorType) -> int:
    try:
        fd = os.open(str(root), _DIRECTORY_FLAGS)
    except OSError as error:
        raise error_type(f"无法安全打开仓库根目录 {root}：{error}") from error
    if not stat.S_ISDIR(os.fstat(fd).st_mode):
        os.close(fd)
        raise error_type(f"仓库根路径不是目录：{root}")
    return fd


def _fsync_directory_fd(fd: int, path: Path, event_hook: EventHook) -> None:
    os.fsync(fd)
    _emit(event_hook, "directory_fsynced", path)


def _same_inode(left: os.stat_result, right: os.stat_result) -> bool:
    return (left.st_dev, left.st_ino) == (right.st_dev, right.st_ino)


def _assert_opened_entry_current(
    parent_fd: int,
    name: str,
    opened_fd: int,
    display_path: Path,
    error_type: ErrorType,
) -> None:
    status = _entry_status(parent_fd, name)
    if status is None or not _same_inode(status, os.fstat(opened_fd)):
        raise error_type(f"路径项在打开期间被替换：{display_path}")


def _verify_opened_entry(
    parent_fd: int,
    name: str,
    opened_fd: int,
    display_path: Path,
    error_type: ErrorType,
) -> None:
    try:
        _assert_opened_entry_current(
            parent_fd, name, opened_fd, display_path, error_type
        )
    except BaseException:
        os.close(opened_fd)
        raise


def _open_directory_chain(
    root: Path,
    relative: Path,
    *,
    create: bool,
    missing_ok: bool,
    error_type: ErrorType,
    event_hook: EventHook = None,
) -> Optional[int]:
    current_fd = _open_root(root, error_type)
    current_path = root
    try:
        for part in relative.parts:
            next_path = current_path / part
            try:
                next_fd = os.open(part, _DIRECTORY_FLAGS, dir_fd=current_fd)
            except FileNotFoundError:
                if not create:
                    if missing_ok:
                        os.close(current_fd)
                        return None
                    raise error_type(f"目录不存在：{next_path}")
                try:
                    os.mkdir(part, mode=0o755, dir_fd=current_fd)
                except FileExistsError:
                    pass
                except OSError as error:
                    _raise_component_error(
                        error_type, root / relative, next_path, current_fd, part, error
                    )
                try:
                    next_fd = os.open(part, _DIRECTORY_FLAGS, dir_fd=current_fd)
                except OSError as error:
                    _raise_component_error(
                        error_type, root / relative, next_path, current_fd, part, error
                    )
                _emit(event_hook, "directory_created", next_path)
                _fsync_directory_fd(next_fd, next_path, event_hook)
                _fsync_directory_fd(current_fd, current_path, event_hook)
            except OSError as error:
                _raise_component_error(
                    error_type, root / relative, next_path, current_fd, part, error
                )
            _verify_opened_entry(
                current_fd, part, next_fd, next_path, error_type
            )
            os.close(current_fd)
            current_fd = next_fd
            current_path = next_path
        return current_fd
    except BaseException:
        try:
            os.close(current_fd)
        except OSError:
            pass
        raise


def _open_parent(
    root: Path,
    relative: Path,
    *,
    create: bool,
    missing_ok: bool,
    error_type: ErrorType,
    event_hook: EventHook = None,
) -> Tuple[Optional[int], Path, str]:
    parent_relative = Path(*relative.parts[:-1]) if len(relative.parts) > 1 else Path()
    parent_fd = _open_directory_chain(
        root,
        parent_relative,
        create=create,
        missing_ok=missing_ok,
        error_type=error_type,
        event_hook=event_hook,
    )
    return parent_fd, root / parent_relative, relative.name


def _assert_directory_current(
    root: Path,
    relative: Path,
    opened_fd: int,
    error_type: ErrorType,
) -> None:
    fresh_fd = _open_directory_chain(
        root,
        relative,
        create=False,
        missing_ok=False,
        error_type=error_type,
    )
    assert fresh_fd is not None
    try:
        if not _same_inode(os.fstat(opened_fd), os.fstat(fresh_fd)):
            raise error_type(
                f"目录在操作期间被替换或移出仓库：{root / relative}"
            )
    finally:
        os.close(fresh_fd)


def _assert_parent_current(
    root: Path,
    relative: Path,
    opened_parent_fd: int,
    error_type: ErrorType,
) -> None:
    parent_relative = Path(*relative.parts[:-1]) if len(relative.parts) > 1 else Path()
    _assert_directory_current(root, parent_relative, opened_parent_fd, error_type)


def _open_regular_at(
    parent_fd: int,
    name: str,
    display_path: Path,
    error_type: ErrorType,
) -> Optional[int]:
    try:
        fd = os.open(name, _FILE_READ_FLAGS, dir_fd=parent_fd)
    except FileNotFoundError:
        return None
    except OSError as error:
        try:
            status = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError:
            status = None
        if status is not None and stat.S_ISLNK(status.st_mode):
            raise error_type(f"路径包含符号链接：{display_path}") from error
        raise error_type(f"无法安全打开文件 {display_path}：{error}") from error
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise error_type(f"不是普通文件：{display_path}")
    _verify_opened_entry(parent_fd, name, fd, display_path, error_type)
    return fd


def _sha256_fd(fd: int) -> str:
    digest = hashlib.sha256()
    os.lseek(fd, 0, os.SEEK_SET)
    while True:
        chunk = os.read(fd, 1024 * 1024)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def _optional_sha256_relative(
    root: Path,
    relative: Path,
    error_type: ErrorType,
) -> Optional[str]:
    parent_fd, parent_path, name = _open_parent(
        root,
        relative,
        create=False,
        missing_ok=True,
        error_type=error_type,
    )
    if parent_fd is None:
        return None
    try:
        fd = _open_regular_at(parent_fd, name, parent_path / name, error_type)
        if fd is None:
            _assert_parent_current(root, relative, parent_fd, error_type)
            return None
        try:
            digest = _sha256_fd(fd)
            _assert_opened_entry_current(
                parent_fd, name, fd, parent_path / name, error_type
            )
            _assert_parent_current(root, relative, parent_fd, error_type)
            return digest
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


def _read_bytes_relative(root: Path, relative: Path, error_type: ErrorType) -> bytes:
    parent_fd, parent_path, name = _open_parent(
        root,
        relative,
        create=False,
        missing_ok=False,
        error_type=error_type,
    )
    assert parent_fd is not None
    try:
        fd = _open_regular_at(parent_fd, name, parent_path / name, error_type)
        if fd is None:
            raise error_type(f"文件不存在：{parent_path / name}")
        try:
            chunks = []
            while True:
                chunk = os.read(fd, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            _assert_opened_entry_current(
                parent_fd, name, fd, parent_path / name, error_type
            )
            _assert_parent_current(root, relative, parent_fd, error_type)
            return b"".join(chunks)
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


def _entry_status(parent_fd: int, name: str) -> Optional[os.stat_result]:
    try:
        return os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def _open_transaction_parent(
    root: Path,
    *,
    create: bool,
    missing_ok: bool,
    error_type: ErrorType,
    event_hook: EventHook = None,
) -> Optional[int]:
    return _open_directory_chain(
        root,
        TRANSACTIONS_RELATIVE,
        create=create,
        missing_ok=missing_ok,
        error_type=error_type,
        event_hook=event_hook,
    )


def _open_transaction_dir(
    root: Path,
    transaction_id: str,
    error_type: ErrorType,
) -> Tuple[int, int]:
    parent_fd = _open_transaction_parent(
        root,
        create=False,
        missing_ok=False,
        error_type=error_type,
    )
    assert parent_fd is not None
    transaction_path = root / TRANSACTIONS_RELATIVE / transaction_id
    try:
        status = _entry_status(parent_fd, transaction_id)
        if status is None:
            raise error_type(f"事务目录不存在：{transaction_path}")
        if stat.S_ISLNK(status.st_mode):
            raise error_type(f"事务 UUID 项是符号链接：{transaction_path}")
        if not stat.S_ISDIR(status.st_mode):
            raise error_type(f"事务 UUID 项不是目录：{transaction_path}")
        try:
            transaction_fd = os.open(transaction_id, _DIRECTORY_FLAGS, dir_fd=parent_fd)
        except OSError as error:
            raise error_type(f"无法安全打开事务目录 {transaction_path}：{error}") from error
        _verify_opened_entry(
            parent_fd, transaction_id, transaction_fd, transaction_path, error_type
        )
        return parent_fd, transaction_fd
    except BaseException:
        os.close(parent_fd)
        raise


def _create_transaction_dir(
    root: Path,
    transaction_id: str,
    event_hook: EventHook,
) -> None:
    parent_fd = _open_transaction_parent(
        root,
        create=True,
        missing_ok=False,
        error_type=ValueError,
        event_hook=event_hook,
    )
    assert parent_fd is not None
    transaction_path = root / TRANSACTIONS_RELATIVE / transaction_id
    try:
        status = _entry_status(parent_fd, transaction_id)
        if status is not None:
            if stat.S_ISLNK(status.st_mode):
                raise ValueError(f"事务 UUID 项是符号链接：{transaction_path}")
            raise RuntimeError(f"事务已经 prepare：{transaction_path}")
        try:
            os.mkdir(transaction_id, mode=0o700, dir_fd=parent_fd)
            transaction_fd = os.open(transaction_id, _DIRECTORY_FLAGS, dir_fd=parent_fd)
        except OSError as error:
            raise ValueError(f"无法安全创建事务目录 {transaction_path}：{error}") from error
        _verify_opened_entry(
            parent_fd, transaction_id, transaction_fd, transaction_path, ValueError
        )
        try:
            _emit(event_hook, "directory_created", transaction_path)
            _fsync_directory_fd(transaction_fd, transaction_path, event_hook)
            _fsync_directory_fd(
                parent_fd, root / TRANSACTIONS_RELATIVE, event_hook
            )
        finally:
            os.close(transaction_fd)
    finally:
        os.close(parent_fd)


def _atomic_write_transaction_json(
    root: Path,
    transaction_id: str,
    value: Mapping[str, Any],
    event_hook: EventHook,
) -> str:
    parent_fd, transaction_fd = _open_transaction_dir(root, transaction_id, RuntimeError)
    transaction_path = root / TRANSACTIONS_RELATIVE / transaction_id
    temporary_name = f".journal.json.{uuid.uuid4().hex}.tmp"
    fd: Optional[int] = None
    try:
        try:
            fd = os.open(temporary_name, _FILE_WRITE_FLAGS, 0o600, dir_fd=transaction_fd)
            payload = canonical_json(value).encode("utf-8")
            offset = 0
            while offset < len(payload):
                offset += os.write(fd, payload[offset:])
            capability = durable_fsync(fd)
            _assert_opened_entry_current(
                transaction_fd,
                temporary_name,
                fd,
                transaction_path / temporary_name,
                RuntimeError,
            )
            _assert_directory_current(
                root, TRANSACTIONS_RELATIVE, parent_fd, RuntimeError
            )
            _assert_opened_entry_current(
                parent_fd,
                transaction_id,
                transaction_fd,
                transaction_path,
                RuntimeError,
            )
            os.replace(
                temporary_name,
                "journal.json",
                src_dir_fd=transaction_fd,
                dst_dir_fd=transaction_fd,
            )
            _assert_opened_entry_current(
                transaction_fd,
                "journal.json",
                fd,
                transaction_path / "journal.json",
                RuntimeError,
            )
            os.close(fd)
            fd = None
            _assert_directory_current(
                root, TRANSACTIONS_RELATIVE, parent_fd, RuntimeError
            )
            _assert_opened_entry_current(
                parent_fd,
                transaction_id,
                transaction_fd,
                transaction_path,
                RuntimeError,
            )
            _fsync_directory_fd(transaction_fd, transaction_path, event_hook)
            return capability
        finally:
            if fd is not None:
                os.close(fd)
            try:
                os.unlink(temporary_name, dir_fd=transaction_fd)
            except FileNotFoundError:
                pass
    finally:
        os.close(transaction_fd)
        os.close(parent_fd)


def _write_staged(
    root: Path,
    transaction_id: str,
    name: str,
    value: bytes,
    event_hook: EventHook,
) -> str:
    parent_fd, transaction_fd = _open_transaction_dir(root, transaction_id, RuntimeError)
    transaction_path = root / TRANSACTIONS_RELATIVE / transaction_id
    fd: Optional[int] = None
    try:
        try:
            fd = os.open(name, _FILE_WRITE_FLAGS, 0o600, dir_fd=transaction_fd)
            offset = 0
            while offset < len(value):
                offset += os.write(fd, value[offset:])
            os.fchmod(fd, 0o400)
            capability = durable_fsync(fd)
            _assert_opened_entry_current(
                transaction_fd,
                name,
                fd,
                transaction_path / name,
                RuntimeError,
            )
            _assert_directory_current(
                root, TRANSACTIONS_RELATIVE, parent_fd, RuntimeError
            )
            _assert_opened_entry_current(
                parent_fd,
                transaction_id,
                transaction_fd,
                transaction_path,
                RuntimeError,
            )
            os.close(fd)
            fd = None
        except BaseException:
            if fd is not None:
                os.close(fd)
                fd = None
            try:
                os.unlink(name, dir_fd=transaction_fd)
            except FileNotFoundError:
                pass
            raise
        _fsync_directory_fd(transaction_fd, transaction_path, event_hook)
        _emit(event_hook, "staged_durable", transaction_path / name)
        return capability
    finally:
        os.close(transaction_fd)
        os.close(parent_fd)


def _read_transaction_file(
    root: Path,
    transaction_id: str,
    name: str,
    error_type: ErrorType,
) -> bytes:
    parent_fd, transaction_fd = _open_transaction_dir(root, transaction_id, error_type)
    display = root / TRANSACTIONS_RELATIVE / transaction_id / name
    try:
        fd = _open_regular_at(transaction_fd, name, display, error_type)
        if fd is None:
            raise error_type(f"事务文件不存在：{display}")
        try:
            chunks = []
            while True:
                chunk = os.read(fd, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            _assert_opened_entry_current(
                transaction_fd, name, fd, display, error_type
            )
            _assert_opened_entry_current(
                parent_fd,
                transaction_id,
                transaction_fd,
                root / TRANSACTIONS_RELATIVE / transaction_id,
                error_type,
            )
            return b"".join(chunks)
        finally:
            os.close(fd)
    finally:
        os.close(transaction_fd)
        os.close(parent_fd)


def _optional_transaction_sha256(
    root: Path,
    transaction_id: str,
    name: str,
    error_type: ErrorType,
) -> Optional[str]:
    parent_fd, transaction_fd = _open_transaction_dir(root, transaction_id, error_type)
    display = root / TRANSACTIONS_RELATIVE / transaction_id / name
    try:
        fd = _open_regular_at(transaction_fd, name, display, error_type)
        if fd is None:
            return None
        try:
            digest = _sha256_fd(fd)
            _assert_opened_entry_current(
                transaction_fd, name, fd, display, error_type
            )
            _assert_opened_entry_current(
                parent_fd,
                transaction_id,
                transaction_fd,
                root / TRANSACTIONS_RELATIVE / transaction_id,
                error_type,
            )
            return digest
        finally:
            os.close(fd)
    finally:
        os.close(transaction_fd)
        os.close(parent_fd)


def _remove_tree_contents(fd: int, display: Path, error_type: ErrorType) -> None:
    for name in os.listdir(fd):
        status = _entry_status(fd, name)
        if status is None:
            continue
        child_display = display / name
        if stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode):
            try:
                child_fd = os.open(name, _DIRECTORY_FLAGS, dir_fd=fd)
            except OSError as error:
                raise error_type(f"无法安全打开待删除目录 {child_display}：{error}") from error
            try:
                _remove_tree_contents(child_fd, child_display, error_type)
            finally:
                os.close(child_fd)
            os.rmdir(name, dir_fd=fd)
        else:
            os.unlink(name, dir_fd=fd)


def _cleanup_transaction(
    root: Path,
    transaction_id: str,
    event_hook: EventHook,
) -> None:
    parent_fd, transaction_fd = _open_transaction_dir(root, transaction_id, RuntimeError)
    transaction_path = root / TRANSACTIONS_RELATIVE / transaction_id
    try:
        opened = os.fstat(transaction_fd)
        _remove_tree_contents(transaction_fd, transaction_path, RuntimeError)
        current = _entry_status(parent_fd, transaction_id)
        if current is None or stat.S_ISLNK(current.st_mode):
            raise RuntimeError(f"事务目录在清理期间发生变化：{transaction_path}")
        if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
            raise RuntimeError(f"事务目录在清理期间被替换：{transaction_path}")
        os.rmdir(transaction_id, dir_fd=parent_fd)
        _emit(event_hook, "transaction_removed", transaction_path)
        os.fsync(parent_fd)
        _emit(
            event_hook,
            "transactions_parent_fsynced",
            root / TRANSACTIONS_RELATIVE,
        )
    finally:
        os.close(transaction_fd)
        os.close(parent_fd)


class RepoLock:
    def __init__(self, root: Path, recover: bool = True) -> None:
        self.root = _repository_root(Path(root))
        self.recover = recover
        self.lock_path: Optional[Path] = None
        self._handle: Any = None

    def acquire(self) -> "RepoLock":
        if self._handle is not None:
            raise RuntimeError("仓库锁已经取得")
        result = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--git-common-dir"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        common = Path(result.stdout.strip())
        if not common.is_absolute():
            common = self.root / common
        common = common.resolve()
        self.lock_path = common / "gaokao-latex.lock"
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
        try:
            lock_fd = os.open(str(self.lock_path), flags, 0o600)
        except OSError as error:
            raise RuntimeError(f"无法安全打开仓库锁 {self.lock_path}：{error}") from error
        self._handle = os.fdopen(lock_fd, "a+b")
        try:
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            self._handle.close()
            self._handle = None
            if error.errno in {errno.EACCES, errno.EAGAIN}:
                raise BlockingIOError(
                    error.errno, "仓库已有写事务", str(self.lock_path)
                ) from error
            raise
        if self.recover:
            try:
                recover_transactions(self.root)
            except BaseException:
                self.release()
                raise
        return self

    def release(self) -> None:
        if self._handle is None:
            return
        try:
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        finally:
            self._handle.close()
            self._handle = None

    def __enter__(self) -> "RepoLock":
        return self.acquire()

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.release()


class Transaction:
    def __init__(
        self,
        root: Path,
        event_hook: EventHook = None,
        transaction_id: Optional[str] = None,
    ) -> None:
        self.root = _repository_root(Path(root))
        self.event_hook = event_hook
        self.transaction_id = transaction_id or str(uuid.uuid4())
        if UUID_PATTERN.fullmatch(self.transaction_id) is None:
            raise ValueError(f"非法 transaction_id：{self.transaction_id!r}")
        self.transactions_parent = self.root / TRANSACTIONS_RELATIVE
        self.transaction_dir = self.transactions_parent / self.transaction_id
        self.journal_path = self.transaction_dir / "journal.json"
        self._prepared = False

    def prepare(
        self,
        mode: str,
        targets: Mapping[str, bytes],
        inputs: Mapping[str, Optional[str]],
        expected_revision: Optional[int] = None,
    ) -> "Transaction":
        if self._prepared:
            raise RuntimeError("事务已经 prepare")
        target_items, clean_inputs = self._validate_prepare_arguments(
            mode, targets, inputs, expected_revision
        )

        before_hashes: Dict[str, Optional[str]] = {}
        for relative, _ in target_items:
            path = Path(relative)
            before_hashes[relative] = _optional_sha256_relative(
                self.root, path, ValueError
            )
        for relative in clean_inputs:
            _optional_sha256_relative(self.root, Path(relative), ValueError)

        _create_transaction_dir(self.root, self.transaction_id, self.event_hook)
        journal_published = False
        try:
            for relative, _ in target_items:
                parent_fd, _, _ = _open_parent(
                    self.root,
                    Path(relative),
                    create=True,
                    missing_ok=False,
                    error_type=ValueError,
                    event_hook=self.event_hook,
                )
                assert parent_fd is not None
                os.close(parent_fd)

            target_records: List[Dict[str, Any]] = []
            capabilities = set()
            for index, (relative, value) in enumerate(target_items):
                current_before = _optional_sha256_relative(
                    self.root, Path(relative), ValueError
                )
                if current_before != before_hashes[relative]:
                    raise ValueError(f"目标在 prepare 期间发生变化：{relative}")
                staged_name = f"target-{index:04d}.bin"
                capability = _write_staged(
                    self.root,
                    self.transaction_id,
                    staged_name,
                    value,
                    self.event_hook,
                )
                capabilities.add(capability)
                target_records.append({
                    "path": relative,
                    "before_sha256": current_before,
                    "expected_sha256": _sha256_bytes(value),
                    "staged": staged_name,
                })

            journal: Dict[str, Any] = {
                "version": 1,
                "transaction_id": self.transaction_id,
                "mode": mode,
                "status": "prepared",
                "expected_revision": expected_revision,
                "inputs": clean_inputs,
                "targets": target_records,
                "applied": [],
                "durability": {
                    "file_sync": sorted(capabilities),
                    "directory_sync": "fsync",
                },
            }
            _atomic_write_transaction_json(
                self.root, self.transaction_id, journal, self.event_hook
            )
            journal_published = True
            _emit(self.event_hook, "journal_prepared", self.journal_path)
            self._prepared = True
            return self
        except BaseException:
            if not journal_published:
                _cleanup_transaction(self.root, self.transaction_id, self.event_hook)
            raise

    def commit(self) -> None:
        try:
            _read_transaction_file(
                self.root, self.transaction_id, "journal.json", RuntimeError
            )
        except RuntimeError as error:
            raise RuntimeError("事务尚未 prepare") from error
        _commit_transaction(self.root, self.transaction_id, self.event_hook)

    def _validate_prepare_arguments(
        self,
        mode: str,
        targets: Mapping[str, bytes],
        inputs: Mapping[str, Optional[str]],
        expected_revision: Optional[int],
    ) -> Tuple[List[Tuple[str, bytes]], Dict[str, Optional[str]]]:
        if mode not in {"state", "content"}:
            raise ValueError(f"未知事务模式：{mode}")
        if not isinstance(targets, Mapping):
            raise ValueError("targets 必须是非空映射")
        target_count = len(targets)
        if target_count == 0:
            raise ValueError("targets 必须是非空映射")
        _validate_target_count(target_count, ValueError)
        if not isinstance(inputs, Mapping):
            raise ValueError("inputs 必须是映射")

        target_items: List[Tuple[str, bytes]] = []
        seen_target_keys: Dict[Tuple[str, ...], str] = {}
        for raw_path, value in targets.items():
            relative_path = _validated_repo_relative(raw_path, ValueError)
            relative = relative_path.as_posix()
            key = _path_key(relative_path)
            if key in seen_target_keys:
                raise ValueError(
                    f"重复目标或路径别名：{seen_target_keys[key]} / {relative}"
                )
            if not isinstance(value, bytes):
                raise TypeError(f"目标内容必须是 bytes：{relative}")
            seen_target_keys[key] = relative
            target_items.append((relative, value))

        clean_inputs: Dict[str, Optional[str]] = {}
        seen_input_keys: Dict[Tuple[str, ...], str] = {}
        for raw_path, expected_hash in inputs.items():
            relative_path = _validated_repo_relative(raw_path, ValueError)
            relative = relative_path.as_posix()
            key = _path_key(relative_path)
            if key in seen_input_keys:
                raise ValueError(
                    f"重复输入或路径别名：{seen_input_keys[key]} / {relative}"
                )
            if expected_hash is not None and (
                not isinstance(expected_hash, str)
                or SHA256_PATTERN.fullmatch(expected_hash) is None
            ):
                raise ValueError(f"输入哈希必须是 sha256 或 null：{relative}")
            seen_input_keys[key] = relative
            clean_inputs[relative] = expected_hash

        overlap_keys = set(seen_target_keys).intersection(seen_input_keys)
        if overlap_keys:
            aliases = [
                f"{seen_target_keys[key]} / {seen_input_keys[key]}"
                for key in sorted(overlap_keys)
            ]
            raise ValueError(f"inputs 与 targets 不得相交或互为路径别名：{aliases}")

        target_paths = [path for path, _ in target_items]
        manifest_key = _path_key(Path(MANIFEST_TARGET))
        if mode == "content":
            if manifest_key in seen_target_keys:
                raise ValueError("content 模式禁止把 manifest 或其路径别名列为目标")
            if expected_revision is not None:
                raise ValueError("content 模式不得设置 expected_revision")
        else:
            if type(expected_revision) is not int or expected_revision < 0:
                raise ValueError("state 模式要求非负整数 expected_revision")
            if (
                target_paths.count(MANIFEST_TARGET) != 1
                or target_paths[-1] != MANIFEST_TARGET
            ):
                raise ValueError("state 模式要求 manifest 是唯一且最后的 manifest 目标")
            self._validate_state_manifest(target_items[-1][1], expected_revision)
        return target_items, clean_inputs

    def _validate_state_manifest(self, value: bytes, expected_revision: int) -> None:
        try:
            manifest = json.loads(value.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ValueError(f"state manifest 目标不是合法 JSON：{error}") from error
        if not isinstance(manifest, Mapping):
            raise ValueError("state manifest 目标必须是对象")
        revision = manifest.get("revision")
        if type(revision) is not int or revision < 0:
            raise ValueError("state manifest revision 必须是非负整数")
        if revision != expected_revision + 1:
            raise ValueError("state manifest revision 必须递增 1")
        if manifest.get("last_transaction_id") != self.transaction_id:
            raise ValueError("state manifest last_transaction_id 必须等于事务 ID")


def _load_journal(root: Path, transaction_id: str) -> Dict[str, Any]:
    journal_path = root / TRANSACTIONS_RELATIVE / transaction_id / "journal.json"
    try:
        raw = _read_transaction_file(
            root, transaction_id, "journal.json", RuntimeError
        )
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"无法读取事务 journal：{journal_path}: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"事务 journal 顶层不是对象：{journal_path}")
    required = {
        "version", "transaction_id", "mode", "status", "inputs", "targets", "applied"
    }
    missing = required - set(value)
    if missing:
        raise RuntimeError(f"事务 journal 缺少字段：{sorted(missing)}")
    if type(value["version"]) is not int or value["version"] != 1:
        raise RuntimeError(f"不支持的事务 journal：{journal_path}")
    if value["mode"] not in {"state", "content"}:
        raise RuntimeError(f"不支持的事务 journal：{journal_path}")
    if value["status"] not in {"prepared", "committed"}:
        raise RuntimeError(f"未知事务状态：{value['status']}")
    if value["transaction_id"] != transaction_id:
        raise RuntimeError("事务目录与 journal ID 不一致")
    if not isinstance(value["inputs"], dict) or not isinstance(value["targets"], list):
        raise RuntimeError("事务 journal inputs/targets 格式错误")
    if not isinstance(value["applied"], list) or not all(
        isinstance(item, str) for item in value["applied"]
    ):
        raise RuntimeError("事务 journal applied 格式错误")
    return value


def _validated_input_records(
    inputs: Mapping[str, Any],
    error_type: ErrorType,
) -> List[Tuple[Path, str, Optional[str], Tuple[str, ...]]]:
    records = []
    seen: Dict[Tuple[str, ...], str] = {}
    for raw_path, expected in inputs.items():
        relative_path = _validated_repo_relative(raw_path, error_type)
        relative = relative_path.as_posix()
        key = _path_key(relative_path)
        if key in seen:
            raise error_type(
                f"事务输入重复或互为路径别名：{seen[key]} / {relative}"
            )
        if expected is not None and (
            not isinstance(expected, str) or SHA256_PATTERN.fullmatch(expected) is None
        ):
            raise error_type(f"非法输入哈希：{relative}")
        seen[key] = relative
        records.append((relative_path, relative, expected, key))
    return records


def _validated_records(
    root: Path,
    transaction_id: str,
    journal: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    seen: Dict[Tuple[str, ...], str] = {}
    staged_seen = set()
    _validate_target_count(len(journal["targets"]), RuntimeError)
    for raw in journal["targets"]:
        if not isinstance(raw, dict):
            raise RuntimeError("事务 target 记录不是对象")
        try:
            relative_path = _validated_repo_relative(raw["path"], RuntimeError)
            relative = relative_path.as_posix()
            before = raw["before_sha256"]
            expected = raw["expected_sha256"]
            staged_name = raw["staged"]
        except KeyError as error:
            raise RuntimeError(f"非法事务 target 记录：{raw!r}") from error
        key = _path_key(relative_path)
        if key in seen:
            raise RuntimeError(
                f"事务 target 重复或互为路径别名：{seen[key]} / {relative}"
            )
        seen[key] = relative
        if before is not None and (
            not isinstance(before, str) or SHA256_PATTERN.fullmatch(before) is None
        ):
            raise RuntimeError(f"非法 target 前置哈希：{relative}")
        if not isinstance(expected, str) or SHA256_PATTERN.fullmatch(expected) is None:
            raise RuntimeError(f"非法 target 期望哈希：{relative}")
        if not isinstance(staged_name, str) or STAGED_PATTERN.fullmatch(staged_name) is None:
            raise RuntimeError(f"非法 staged 文件名：{staged_name!r}")
        if staged_name in staged_seen:
            raise RuntimeError(f"重复 staged 文件名：{staged_name}")
        staged_seen.add(staged_name)
        staged_hash = _optional_transaction_sha256(
            root, transaction_id, staged_name, RuntimeError
        )
        if journal["status"] != "committed" and staged_hash != expected:
            raise RuntimeError(f"staged 内容哈希不匹配：{relative}")
        if journal["status"] == "committed" and staged_hash not in {None, expected}:
            raise RuntimeError(f"committed 事务 staged 内容哈希不匹配：{relative}")
        _optional_sha256_relative(root, relative_path, RuntimeError)
        records.append({
            "path": relative,
            "relative": relative_path,
            "before_sha256": before,
            "expected_sha256": expected,
            "staged": staged_name,
        })
    if not records:
        raise RuntimeError("事务没有目标")
    manifest_key = _path_key(Path(MANIFEST_TARGET))
    if journal["mode"] == "content" and manifest_key in seen:
        raise RuntimeError("content journal 非法包含 manifest 或其路径别名")
    if journal["mode"] == "state" and (
        [record["path"] for record in records].count(MANIFEST_TARGET) != 1
        or records[-1]["path"] != MANIFEST_TARGET
    ):
        raise RuntimeError("state journal 的 manifest 不是最后目标")
    input_records = _validated_input_records(journal["inputs"], RuntimeError)
    overlap_keys = set(seen).intersection(record[3] for record in input_records)
    if overlap_keys:
        aliases = [
            f"{seen[key]} / {relative}"
            for _, relative, _, key in input_records
            if key in overlap_keys
        ]
        raise RuntimeError(
            f"事务 journal 的 inputs 与 targets 相交或互为路径别名：{aliases}"
        )
    applied_keys = set()
    for raw_applied in journal["applied"]:
        applied_path = _validated_repo_relative(raw_applied, RuntimeError)
        applied_key = _path_key(applied_path)
        if (
            applied_key in applied_keys
            or applied_key not in seen
            or raw_applied != seen[applied_key]
        ):
            raise RuntimeError("事务 journal applied 包含未知、重复或别名目标")
        applied_keys.add(applied_key)
    if journal["mode"] == "state":
        expected_revision = journal.get("expected_revision")
        if type(expected_revision) is not int or expected_revision < 0:
            raise RuntimeError("state journal expected_revision 非法")
        staged = _optional_transaction_sha256(
            root, transaction_id, records[-1]["staged"], RuntimeError
        )
        if staged is None and journal["status"] == "committed":
            manifest_raw = _read_bytes_relative(
                root, records[-1]["relative"], RuntimeError
            )
        else:
            manifest_raw = _read_transaction_file(
                root, transaction_id, records[-1]["staged"], RuntimeError
            )
        try:
            manifest = json.loads(manifest_raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise RuntimeError(f"state 目标不是合法 manifest：{error}") from error
        revision = manifest.get("revision") if isinstance(manifest, Mapping) else None
        if type(revision) is not int or revision < 0:
            raise RuntimeError("state 目标 revision 必须是非负整数")
        if (
            revision != expected_revision + 1
            or manifest.get("last_transaction_id") != journal["transaction_id"]
        ):
            raise RuntimeError("state 目标 revision/last_transaction_id 与 journal 不一致")
    return records


def _validate_inputs(root: Path, inputs: Mapping[str, Any]) -> None:
    validated = _validated_input_records(inputs, RuntimeError)
    for relative, display, expected, _ in validated:
        current = _optional_sha256_relative(root, relative, RuntimeError)
        if current != expected:
            raise RuntimeError(
                f"输入 {display} 漂移：期望 {expected}，实际 {current}"
            )


def _validate_target_preconditions(
    root: Path,
    records: List[Dict[str, Any]],
) -> Dict[str, Optional[str]]:
    current_hashes: Dict[str, Optional[str]] = {}
    for record in records:
        current = _optional_sha256_relative(
            root, record["relative"], RuntimeError
        )
        current_hashes[record["path"]] = current
        if current not in {record["before_sha256"], record["expected_sha256"]}:
            raise RuntimeError(
                f"目标 {record['path']} 出现第三种哈希：{current}；"
                f"事务前 {record['before_sha256']}；期望 {record['expected_sha256']}"
            )
    return current_hashes


def _read_manifest_revision(root: Path, relative: Path) -> Tuple[int, Any]:
    path = root / relative
    try:
        value = json.loads(_read_bytes_relative(root, relative, RuntimeError).decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"无法读取 state manifest：{path}: {error}") from error
    if not isinstance(value, Mapping):
        raise RuntimeError("state manifest 顶层不是对象")
    revision = value.get("revision")
    if type(revision) is not int or revision < 0:
        raise RuntimeError("state manifest revision 必须是非负整数")
    return revision, value.get("last_transaction_id")


def _validate_state_revision(
    root: Path,
    journal: Mapping[str, Any],
    records: List[Dict[str, Any]],
) -> None:
    expected_revision = journal.get("expected_revision")
    if type(expected_revision) is not int or expected_revision < 0:
        raise RuntimeError("state journal expected_revision 非法")
    revision, transaction_id = _read_manifest_revision(
        root, records[-1]["relative"]
    )
    if revision == expected_revision:
        return
    if revision == expected_revision + 1 and transaction_id == journal["transaction_id"]:
        return
    raise RuntimeError(
        f"manifest revision CAS 失败：期望 {expected_revision}，实际 {revision}"
    )


def _validate_state_cas(
    root: Path,
    journal: Mapping[str, Any],
    records: List[Dict[str, Any]],
    current_hashes: Mapping[str, Optional[str]],
) -> None:
    expected_revision = journal["expected_revision"]
    manifest = records[-1]
    revision, transaction_id = _read_manifest_revision(root, manifest["relative"])
    if revision == expected_revision + 1 and transaction_id == journal["transaction_id"]:
        incomplete = [
            record["path"]
            for record in records
            if current_hashes[record["path"]] != record["expected_sha256"]
        ]
        if incomplete:
            raise RuntimeError(f"manifest 已提交但其他目标不完整：{incomplete}")


def _same_directory(fd: int, other_fd: int) -> bool:
    left = os.fstat(fd)
    right = os.fstat(other_fd)
    return (left.st_dev, left.st_ino) == (right.st_dev, right.st_ino)


def _revalidate_parent_identity(
    root: Path,
    relative: Path,
    opened_parent_fd: int,
) -> None:
    fresh_fd, _, _ = _open_parent(
        root,
        relative,
        create=False,
        missing_ok=False,
        error_type=RuntimeError,
    )
    assert fresh_fd is not None
    try:
        if not _same_directory(opened_parent_fd, fresh_fd):
            raise RuntimeError(
                f"目标父目录在操作期间被替换：{relative.as_posix()}"
            )
    finally:
        os.close(fresh_fd)


def _replace_target(
    root: Path,
    transaction_id: str,
    record: Mapping[str, Any],
    event_hook: EventHook,
) -> None:
    relative = record["relative"]
    parent_fd, parent_path, target_name = _open_parent(
        root,
        relative,
        create=False,
        missing_ok=False,
        error_type=RuntimeError,
    )
    assert parent_fd is not None
    transaction_parent_fd, transaction_fd = _open_transaction_dir(
        root, transaction_id, RuntimeError
    )
    staged_path = root / TRANSACTIONS_RELATIVE / transaction_id / record["staged"]
    temporary_name = f".{target_name}.{uuid.uuid4().hex}.tmp"
    temporary_fd: Optional[int] = None
    target_path = root / relative
    try:
        staged_fd = _open_regular_at(
            transaction_fd, record["staged"], staged_path, RuntimeError
        )
        if staged_fd is None:
            raise RuntimeError(f"staged 文件不存在：{staged_path}")
        try:
            temporary_fd = os.open(
                temporary_name, _FILE_WRITE_FLAGS, 0o600, dir_fd=parent_fd
            )
            digest = hashlib.sha256()
            while True:
                chunk = os.read(staged_fd, 1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
                offset = 0
                while offset < len(chunk):
                    offset += os.write(temporary_fd, chunk[offset:])
            if digest.hexdigest() != record["expected_sha256"]:
                raise RuntimeError(f"staged 内容哈希不匹配：{record['path']}")
            _assert_opened_entry_current(
                transaction_fd,
                record["staged"],
                staged_fd,
                staged_path,
                RuntimeError,
            )
            _assert_opened_entry_current(
                transaction_parent_fd,
                transaction_id,
                transaction_fd,
                root / TRANSACTIONS_RELATIVE / transaction_id,
                RuntimeError,
            )
            durable_fsync(temporary_fd)
            _assert_opened_entry_current(
                parent_fd,
                temporary_name,
                temporary_fd,
                parent_path / temporary_name,
                RuntimeError,
            )
        finally:
            os.close(staged_fd)

        _revalidate_parent_identity(root, relative, parent_fd)
        current_fd = _open_regular_at(
            parent_fd, target_name, target_path, RuntimeError
        )
        if current_fd is None:
            current = None
        else:
            try:
                current = _sha256_fd(current_fd)
                _assert_opened_entry_current(
                    parent_fd,
                    target_name,
                    current_fd,
                    target_path,
                    RuntimeError,
                )
            finally:
                os.close(current_fd)
        if current == record["expected_sha256"]:
            os.unlink(temporary_name, dir_fd=parent_fd)
            os.close(temporary_fd)
            temporary_fd = None
            os.fsync(parent_fd)
            _emit(event_hook, "target_directory_fsynced", parent_path)
            return
        if current != record["before_sha256"]:
            raise RuntimeError(f"目标 {record['path']} 出现第三种哈希：{current}")
        _revalidate_parent_identity(root, relative, parent_fd)
        _assert_opened_entry_current(
            parent_fd,
            temporary_name,
            temporary_fd,
            parent_path / temporary_name,
            RuntimeError,
        )
        os.replace(
            temporary_name,
            target_name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        _assert_opened_entry_current(
            parent_fd,
            target_name,
            temporary_fd,
            target_path,
            RuntimeError,
        )
        os.close(temporary_fd)
        temporary_fd = None
        _emit(event_hook, "target_replaced", target_path)
        os.fsync(parent_fd)
        _emit(event_hook, "target_directory_fsynced", parent_path)
    finally:
        if temporary_fd is not None:
            os.close(temporary_fd)
        try:
            os.unlink(temporary_name, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        os.close(transaction_fd)
        os.close(transaction_parent_fd)
        os.close(parent_fd)


def _sync_target_directory(
    root: Path,
    relative: Path,
    event_hook: EventHook,
) -> None:
    parent_fd, parent_path, _ = _open_parent(
        root,
        relative,
        create=False,
        missing_ok=False,
        error_type=RuntimeError,
    )
    assert parent_fd is not None
    try:
        _revalidate_parent_identity(root, relative, parent_fd)
        os.fsync(parent_fd)
        _emit(event_hook, "target_directory_fsynced", parent_path)
    finally:
        os.close(parent_fd)


def _write_journal(
    root: Path,
    transaction_id: str,
    journal: Dict[str, Any],
    event_hook: EventHook,
) -> None:
    _atomic_write_transaction_json(root, transaction_id, journal, event_hook)


def _commit_transaction(
    root: Path,
    transaction_id: str,
    event_hook: EventHook,
) -> None:
    journal = _load_journal(root, transaction_id)
    records = _validated_records(root, transaction_id, journal)
    _validate_inputs(root, journal["inputs"])
    if journal["mode"] == "state":
        _validate_state_revision(root, journal, records)
    current_hashes = _validate_target_preconditions(root, records)
    if journal["mode"] == "state":
        _validate_state_cas(root, journal, records, current_hashes)

    if journal["status"] == "committed":
        incomplete = [
            record["path"]
            for record in records
            if current_hashes[record["path"]] != record["expected_sha256"]
        ]
        if incomplete:
            raise RuntimeError(f"committed 事务目标不完整：{incomplete}")
        _cleanup_transaction(root, transaction_id, event_hook)
        return

    applied = list(journal.get("applied", []))
    for record in records:
        current = _optional_sha256_relative(
            root, record["relative"], RuntimeError
        )
        if current == record["before_sha256"]:
            _replace_target(root, transaction_id, record, event_hook)
        elif current == record["expected_sha256"]:
            _sync_target_directory(root, record["relative"], event_hook)
        else:
            raise RuntimeError(f"目标 {record['path']} 出现第三种哈希：{current}")
        if record["path"] not in applied:
            applied.append(record["path"])
            journal["applied"] = applied
            _write_journal(root, transaction_id, journal, event_hook)
            _emit(
                event_hook,
                "journal_applied",
                root / TRANSACTIONS_RELATIVE / transaction_id / "journal.json",
            )

    for record in records:
        current = _optional_sha256_relative(
            root, record["relative"], RuntimeError
        )
        if current != record["expected_sha256"]:
            raise RuntimeError(f"目标未达到期望哈希：{record['path']}")
        _sync_target_directory(root, record["relative"], event_hook)

    journal_path = root / TRANSACTIONS_RELATIVE / transaction_id / "journal.json"
    _emit(event_hook, "before_mark_committed", journal_path)
    journal["status"] = "committed"
    _write_journal(root, transaction_id, journal, event_hook)
    _emit(event_hook, "journal_committed", journal_path)
    _cleanup_transaction(root, transaction_id, event_hook)


def recover_transactions(root: Path, event_hook: EventHook = None) -> List[str]:
    repository = _repository_root(Path(root))
    transactions_parent = repository / TRANSACTIONS_RELATIVE
    parent_fd = _open_transaction_parent(
        repository,
        create=False,
        missing_ok=True,
        error_type=RuntimeError,
    )
    if parent_fd is None:
        return []
    recovered: List[str] = []
    try:
        names = sorted(os.listdir(parent_fd))
        for name in names:
            status = _entry_status(parent_fd, name)
            if status is None:
                continue
            transaction_path = transactions_parent / name
            if UUID_PATTERN.fullmatch(name) is None:
                raise RuntimeError(f"transactions 中存在非法目录：{transaction_path}")
            if stat.S_ISLNK(status.st_mode):
                raise RuntimeError(f"事务 UUID 项是符号链接：{transaction_path}")
            if not stat.S_ISDIR(status.st_mode):
                raise RuntimeError(f"transactions 中存在非目录项：{transaction_path}")
            try:
                transaction_fd = os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_fd)
            except OSError as error:
                raise RuntimeError(
                    f"无法安全打开事务 UUID 项 {transaction_path}：{error}"
                ) from error
            try:
                journal_status = _entry_status(transaction_fd, "journal.json")
                if journal_status is not None and stat.S_ISLNK(journal_status.st_mode):
                    raise RuntimeError(f"事务 journal 是符号链接：{transaction_path / 'journal.json'}")
            finally:
                os.close(transaction_fd)
            if journal_status is None:
                _cleanup_transaction(repository, name, event_hook)
                recovered.append(name)
                continue
            if not stat.S_ISREG(journal_status.st_mode):
                raise RuntimeError(f"事务 journal 不是普通文件：{transaction_path / 'journal.json'}")
            _commit_transaction(repository, name, event_hook)
            recovered.append(name)
        return recovered
    finally:
        os.close(parent_fd)
