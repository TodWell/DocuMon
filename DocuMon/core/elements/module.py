import importlib
import inspect
import pathlib
from typing import List

from DocuMon.core.elements import AbsDescriptor, DescriptorT
from DocuMon.core.logger import logger
from DocuMon.core.types import ModuleT


class ModuleD(AbsDescriptor):

    elements: List[DescriptorT]

    def __init__(self, extractor, module: ModuleT):
        AbsDescriptor.__init__(self, extractor, module)
        for key, element in module.__dict__.items():
            if key.startswith("_"):
                continue
            if inspect.isfunction(element):
                if element.__module__ != module.__name__:
                    continue
                new_foo = self._extractor.process_function(element)
                self.elements.append(new_foo)
            if inspect.isclass(element):
                if element.__module__ != module.__name__:
                    continue
                try:
                    new_element = self._extractor.process_class(element)
                except ValueError:
                    logger.warning(f"Could not extract element with key '{key}'")
                else:
                    self.elements.append(new_element)
                continue
            if key == key.upper():
                continue
            logger.debug(f"Module element with key '{key}' not in elements")

        if self.is_init:
            for sub_mod in self.path.parent.glob("*.py"):
                if sub_mod == self.path:
                    continue
                new_mod = importlib.import_module(self.name + "." + sub_mod.stem)
                new_mod_d = self._extractor.process_module(new_mod)
                self.elements.append(new_mod_d)
            for sub_mod in self.path.parent.glob("*/__init__.py"):
                new_mod = importlib.import_module(self.name + "." + sub_mod.parent.name)
                new_mod_d = self._extractor.process_module(new_mod)
                self.elements.append(new_mod_d)

    def type_iterator(self, _type: str):
        for element in self.elements:
            if element.type == _type:
                yield element


    @property
    def path(self):
        return pathlib.Path(self.element.__file__)

    @property
    def is_init(self):
        return self.element.__file__.endswith("__init__.py")

    @property
    def module(self):
        return self.element.__name__