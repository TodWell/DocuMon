import inspect
from typing import TypeVar, List, Any

from DocuMon.core.extractor import ExtractorT
from DocuMon.core.types import ElementT


class AbsAbsDescriptor:
    description: str
    title: str
    type: str
    element: Any

class AbsDescriptor(AbsAbsDescriptor):
    description: str
    author: str
    title: str
    elements: List["DescriptorT"]

    def __init__(self, extractor: ExtractorT, element: ElementT, *parents: ElementT, _type=None):
        """
        author: TDU
        args:
            extractor: Extractor class reading doc string
            element: Element whose doc string should be read
            parents: Possible elements where doc string data should be looked for, if not available in element
            _type: Type of element. Has to be used if inspect is not able to provide the right parameter. i.e. Methods
        ---
        """
        self._type=_type
        check_row = [element, *parents] if parents else [element]
        self.element = element
        self._extractor = extractor
        self._meta = {}
        self.doc = ""
        for el in reversed(check_row):
            meta, txt = self._extractor.read_doc(el.__doc__)
            doc = txt.read()
            if doc:
                self.doc = doc
            try:
                self._meta = {**self._meta, **self._extractor.read_meta(meta)}
            except:
                continue
        self.description = self._meta.get("description") or ""
        self.author = self._meta.get("author") or ""
        self.title = self._meta.get("title") or element.__name__
        self.elements = []

    @property
    def module(self) -> str:
        """
        returns: Name of the module of the element
        ---
        """
        return self.element.__module__

    @property
    def name(self):
        """
        returns: Name of the element
        ---
        """
        if inspect.ismodule(self.element):
            return self.element.__name__
        return self.element.__qualname__

    @property
    def type(self):
        if self._type:
            return self._type
        if inspect.ismodule(self.element):
            return "module"
        if inspect.isclass(self.element):
            return "class"
        if inspect.isfunction(self.element):
            return "function"
        return "unknown"

    @property
    def extractor(self):
        """
        returns: Used extractor
        ---
        """
        return self._extractor


DescriptorT = TypeVar("DescriptorT", bound=AbsAbsDescriptor)
