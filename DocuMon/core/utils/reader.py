import io
from typing import Union


class LineReader:

    def __init__(self, path: str):
        self._path = path
        self._file: Union[io.FileIO, None] = None
        self._lines = [0]
        self._flush_point = 0
        self._eof = 0

    def open(self):
        self._file = open(self._path, "rb")
        self._file.seek(-1, 2)
        self._eof = self._file.tell()
        self._file.seek(0, 0)

    def next(self):
        line = self._file.readline()
        current = self._file.tell()
        if current > self._lines[-1]:
            self._lines.append(self._file.tell())
        return line.decode()

    def jump_back(self):
        self._file.seek(self._flush_point)

    def flush(self):
        self._flush_point = self._file.tell()

    def close(self):
        self._file.close()

    def empty(self):
        return self._file.tell() >= self._eof