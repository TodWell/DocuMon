from DocuMon.core.elements.default_class import ClassD
from DocuMon.core.elements.default_object import ObjectD, PropertyD
from DocuMon.core.elements.module import ModuleD
from DocuMon.core.extractor import ExtractorMgr

extractor = ExtractorMgr(ClassD, ModuleD, ObjectD)

extractor.object_extractor(property)(PropertyD)

