import inspect
from typing import Any

from DocuMon.core.elements import AbsAbsDescriptor
from DocuMon.core.extractor import ExtractorT
from DocuMon.core.types import ElementT


class ObjectD(AbsAbsDescriptor):
    type = "object"

    def __init__(self, extractor: ExtractorT, element: ElementT, name: str):
        self.title = name
        self.description = "Initial value: " + str(element)
        self.element = element


class PropertyD(AbsAbsDescriptor):
    type = "object"

    def __init__(self, extractor: ExtractorT, _property, name):
        self.element = _property
        self.title = name
        meta, txt = extractor.read_doc(_property.__doc__)
        meta = extractor.read_meta(meta)
        self.description = meta.get("description") or meta.get("returns") or meta.get("Returns") or ""
