import inspect
from typing import List, Generator, Any, Tuple

from DocuMon.core.elements import AbsDescriptor, DescriptorT
from DocuMon.core.logger import logger
from DocuMon.core.types import ClassT


def inherited_dict(_class: ClassT) -> Generator[Tuple[str, Any], None, None]:
    """
    author: TDU
    description: Extracts __dict__ values or takes them from parents if not available in _class
    args:
        _class: Class the elements should be iterated over
    returns:
        - key of element
        - element
    ---
    """
    output = {}
    for cls in reversed(_class.__mro__):
        for key, element in cls.__dict__.items():
            output[key] = element
    for k, v in output.items():
        yield k, v


class ClassD(AbsDescriptor):
    methods: List[DescriptorT]

    def __init__(self, extractor, _class):
        """
        author: TDU
        args:
            extractor: Extractor used to read doc
            _class: class the doc is read out of
        ---
        """
        AbsDescriptor.__init__(self, extractor, _class)
        # Iterate over properties
        for key, element in inherited_dict(_class):
            # If it is a constructor, document
            # if key == "__init__":
            #     try:
            #         new_element = self.extractor.process_method(element, _class)
            #     except ValueError:
            #         continue
            #     self.elements.append(new_element)
            #     continue
            # if it is otherwise private, ignore
            if key[0] == "_":
                continue
            # If it is a class function, create class Object
            if inspect.isclass(element):
                try:
                    new_element = self.extractor.process_class(element)
                except ValueError:
                    continue
                self.elements.append(new_element)
                continue
            # If it is a function, create a method object
            if inspect.isfunction(element):
                try:
                    new_element = self.extractor.process_method(element, _class)
                except ValueError:
                    continue
                self.elements.append(new_element)
                continue
            if isinstance(element, object):
                try:
                    new_element = self.extractor.process_object(element, key)
                except ValueError:
                    continue
                self.elements.append(new_element)
            logger.debug(f"Element with key '{key}' not added to class elements")

    def type_iterator(self, _type):
        for element in self.elements:
            if element.type == _type:
                yield element
