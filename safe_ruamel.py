"""
This module is published at https://gist.github.com/wonderbeyond/f6c24690db42c8787cd8feabe1dd91d5
"""
from typing import cast, IO, Union
import io
import os
from concurrent.futures import ProcessPoolExecutor

import ruamel.yaml

__all__ = ['YAML', 'yaml']

_process_cache: dict = {}

_x_process_executor = ProcessPoolExecutor(max_workers=os.cpu_count())


def _yaml_load(input: str):
    yaml = _process_cache.get('yaml')
    if not yaml:
        yaml = _process_cache['yaml'] = ruamel.yaml.YAML()
    return yaml.load(input)


def _yaml_dump(data) -> str:
    yaml = _process_cache.get('yaml')
    if not yaml:
        yaml = _process_cache['yaml'] = ruamel.yaml.YAML()
    buf = io.StringIO()
    yaml.dump(data, buf)
    buf.seek(0)
    return buf.read()


class YAML:
    """A proxy class for ruamel.yaml.YAML that bypass the thread safety issue."""
    def load(self, raw: Union[str, bytes, IO]):
        raw = cast(IO, raw).read() if isinstance(raw, io.IOBase) else raw
        fut = _x_process_executor.submit(_yaml_load, cast(str, raw))
        return fut.result()

    def dump(self, data, stream: Union[IO, None] = None) -> IO:
        stream = io.StringIO() if stream is None else stream
        fut = _x_process_executor.submit(_yaml_dump, data)
        out = fut.result()
        stream.write(out.encode('utf-8') if isinstance(stream, io.BytesIO) else out)  # type: ignore
        stream.seek(0)
        return stream


yaml = YAML()
