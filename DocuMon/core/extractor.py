import io
import textwrap
from typing import TypeVar


class ExtractorMgr:

    def __init__(self, default_class, default_module, default_object):
        self._class_extractors = [(object, True, default_class,)]
        self._object_extractors = [(object, True, default_object,)]
        self._module_extractor = default_module

    def class_extractor(self, children_of, included=True):

        def _lambda(foo):
            self._class_extractors.append((children_of, included, foo,))
            return foo

        return _lambda

    def object_extractor(self, children_of, included=True):

        def _lambda(foo):
            self._object_extractors.append((children_of, included, foo,))

        return _lambda

    def process_module(self, module):
        from DocuMon.core.elements.module import ModuleD
        return ModuleD(self, module)

    def process_class(self, _class):
        for c in _class.__mro__:
            sel = [cls for child, _, cls in self._class_extractors if c == child]
            if sel:
                return sel[0](self, _class)
        raise NotImplementedError("This should be caught by the default extractor")

    def process_function(self, _function):
        from DocuMon.core.elements.default_function import FunctionD
        return FunctionD(self, _function)

    def process_method(self, _method, _class):
        from DocuMon.core.elements.default_method import MethodD
        return MethodD(self, _method, _class)

    def process_object(self, obj, name):
        for c in obj.__class__.__mro__:
            sel = [cls for child, _, cls in self._object_extractors if c == child]
            if sel:
                return sel[0](self, obj, name)
        raise NotImplementedError("This should be caught by the default extractor")

    def read_meta(self, meta: str):
        import yaml
        return yaml.load(meta, yaml.CLoader) or {}

    def read_doc(self, text):
        if text is None:
            return io.StringIO(), io.StringIO()
        text = textwrap.dedent(text)
        stream = io.StringIO(text)
        meta = io.StringIO()
        doc = io.StringIO()
        for line in stream:
            if line.startswith("---"):
                break
            meta.write(line)
        for line in stream:
            doc.write(line)
        meta.seek(0)
        doc.seek(0)
        return meta, doc

    def read_params(self, text: io.StringIO):
        params = {}
        for line in text:
            if line.startswith("@"):
                d = line[1:].split(": ")
                params[d[0]] = ": ".join(d[1:])
        return params

ExtractorT = TypeVar("ExtractorT", bound=ExtractorMgr)
