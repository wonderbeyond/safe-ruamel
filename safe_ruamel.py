"""
This module is published at https://gist.github.com/wonderbeyond/f6c24690db42c8787cd8feabe1dd91d5
"""
from typing import cast, IO, Union
import io
from contextvars import ContextVar

import ruamel.yaml

__all__ = ['YAML', 'yaml']

_yaml: ContextVar[ruamel.yaml.YAML] = ContextVar('yaml')


def _set_yaml():
    if not _yaml.get(None):
        _yaml.set(ruamel.yaml.YAML())


def _yaml_load(input: str):
    _set_yaml()
    yaml = _yaml.get()
    return yaml.load(input)


def _yaml_dump(data) -> str:
    _set_yaml()
    yaml = _yaml.get()
    buf = io.StringIO()
    yaml.dump(data, buf)
    buf.seek(0)
    return buf.read()


class YAML:
    """A proxy class for ruamel.yaml.YAML that bypass the thread safety issue."""
    def load(self, raw: Union[str, bytes, IO]):
        raw = cast(IO, raw).read() if isinstance(raw, io.IOBase) else raw
        return _yaml_load(cast(str, raw))

    def dump(self, data, stream: Union[IO, None] = None) -> IO:
        stream = io.StringIO() if stream is None else stream
        out = _yaml_dump(data)
        stream.write(out.encode('utf-8') if isinstance(stream, io.BytesIO) else out)  # type: ignore
        stream.seek(0)
        return stream


yaml = YAML()
