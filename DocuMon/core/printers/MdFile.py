import io
import pathlib
from typing import Union, Optional



class MdFile:

    indent = "  "

    def __init__(self, path: Union[pathlib.Path, str]):
        self._path = pathlib.Path(path) if isinstance(path, str) else path
        self._f: Optional[io.FileIO] = None

    def write(self, line: str):
        if self._f is None:
            raise ValueError("I/O operation on closed file.")
        self._f.write(line)

    def title(self, title: str, indent=1):
        self.write(indent * "#" + f" {title}")
        self.write("\n\n")

    def paragraph(self, text: str):
        self.write(text)
        self.write("\n\n")

    def element(self, text: str, indent=0):
        self.write(indent * "  " + "- " + text + "  ")
        self.write("\n")

    def write_md(self, text, indent=0):
        text = text.replace("# ", (indent * "#") + "# ")
        # self.write(textwrap.indent(text, indent * self.indent))
        self.write(text)
        self.write("\n\n")

    def __enter__(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._f = open(self._path, "wt")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._f.close()

    def rel_path(self, to: pathlib.Path):
        path = self.path.parent
        return to.relative_to(path)
        # re_to = to if to.is_dir() else to.parent
        # return self._path.relative_to(re_to)

    @classmethod
    def clean(cls, txt):
        return txt.replace("_", "\_").replace("*", "\*")
        # counter = 0
        # while True:
        #     try:
        #         res = self._path.relative_to(re_to)
        #         break
        #     except:
        #         counter += 1
        #         re_to = re_to.parent
        # if counter == 0:
        #     return res
        # return pathlib.Path(counter * "../") / res


    @property
    def path(self):
        return self._path