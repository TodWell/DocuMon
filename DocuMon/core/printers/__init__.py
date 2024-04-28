import abc
import pathlib
from typing import Optional, Type, Tuple, List
from typing import TypeVar

from DocuMon import ModuleD, ClassD, ObjectD
from DocuMon.core.elements import DescriptorT
from DocuMon.core.elements.default_function import FunctionD
from DocuMon.core.elements.default_method import MethodD
from DocuMon.core.printers.MdFile import MdFile


class PartialPrinter(abc.ABC):

    def __init__(self, parent: "ModularPrinter"):
        self._parent = parent

    @abc.abstractmethod
    def path(self, foo):
        pass

    @abc.abstractmethod
    def print_summary(self, foo, md: MdFile, indent=0):
        pass

    @property
    def parent(self):
        return self._parent


class FunctionPrinter(PartialPrinter, abc.ABC):

    @abc.abstractmethod
    def print_function(self, foo: FunctionD):
        pass


class ClassPrinter(PartialPrinter, abc.ABC):


    @abc.abstractmethod
    def print_class(self, _class: ClassD) -> MdFile:
        pass


class MethodPrinter(PartialPrinter, abc.ABC):


    @abc.abstractmethod
    def print_method(self, method: MethodD):
        pass


class ModulePrinter(PartialPrinter, abc.ABC):


    @abc.abstractmethod
    def print_module(self, module: ModuleD):
        pass


class ObjectPrinter(PartialPrinter, abc.ABC):



    @abc.abstractmethod
    def print_object(self, obj: ObjectD):
        pass


class AbsPrinter:

    def print_module(self, module: ModuleD):
        pass


PrinterT = TypeVar("PrinterT", bound=AbsPrinter)
MethodPrinterT = TypeVar("MethodPrinterT", bound=MethodPrinter)
FunctionPrinterT = TypeVar("FunctionPrinterT", bound=FunctionPrinter)
ClassPrinterT = TypeVar("ClassPrinterT", bound=ClassPrinter)
ModulePrinterT = TypeVar("ModulePrinterT", bound=ModulePrinter)
ObjectPrinterT = TypeVar("ObjectPrinterT", bound=ObjectPrinter)


class ModularPrinter(AbsPrinter):

    def __init__(
            self, root: Optional[pathlib.Path] = None,
    ):
        self._root = root if root else pathlib.Path.cwd()
        self._method_printers: List[Tuple[Type[DescriptorT], MethodPrinterT]] = []
        self._function_printers: List[Tuple[Type[DescriptorT], FunctionPrinterT]] = []
        self._class_printers: List[Tuple[Type[DescriptorT], ClassPrinterT]] = []
        self._object_printers: List[Tuple[Type[DescriptorT], ObjectPrinterT]] = []
        self._module_printers: List[Tuple[Type[DescriptorT], ModulePrinterT]] = []

    def set_root(self, root: pathlib.Path):
        self._root = root

    def method_printer(self, prints: Type[DescriptorT]):

        def _lambda(foo: MethodPrinterT):
            self._method_printers.append((prints, foo(self),))

        return _lambda

    def function_printer(self, prints: Type[DescriptorT]):
        def _lambda(foo: FunctionPrinterT):
            self._function_printers.append((prints, foo(self),))

        return _lambda

    def class_printer(self, prints: Type[DescriptorT]):
        def _lambda(foo: ClassPrinterT):
            self._class_printers.append((prints, foo(self),))

        return _lambda

    def object_printer(self, prints: Type[DescriptorT]):
        def _lambda(foo: ObjectPrinterT):
            self._object_printers.append((prints, foo(self),))

        return _lambda

    def module_printer(self, prints: Type[DescriptorT]):
        def _lambda(foo: ModulePrinterT):
            self._module_printers.append((prints, foo(self),))

        return _lambda

    def get_printer(self, selection, element):
        for mro in element.__class__.__mro__:
            for descriptor, printer in selection:
                if descriptor == mro:
                    return printer
        raise NotImplementedError("Could not find a matching printer")

    def get_class_printer(self, _class: ClassD):
        return self.get_printer(self._class_printers, _class)

    def get_object_printer(self, obj: ObjectD):
        return self.get_printer(self._object_printers, obj)

    def get_method_printer(self, method: MethodD):
        return self.get_printer(self._method_printers, method)

    def get_function_printer(self, foo: FunctionD) -> FunctionPrinter:
        return self.get_printer(self._function_printers, foo)

    def get_module_printer(self, module: ModuleD):
        return self.get_printer(self._module_printers, module)

    def print_module(self, module: ModuleD):
        self.get_printer(self._module_printers, module).print_module(module)

    def print_children(self, parent):
        for element in parent.type_iterator("module"):
            self.get_module_printer(element).print_module(element)
        for element in parent.type_iterator("class"):
            self.get_class_printer(element).print_class(element)
        for element in parent.type_iterator("function"):
            self.get_function_printer(element).print_function(element)
        for element in parent.type_iterator("method"):
            self.get_method_printer(element).print_method(element)
        for element in parent.type_iterator("object"):
            self.get_object_printer(element).print_object(element)

    @property
    def root(self):
        if self._root is None:
            raise ValueError("Root not yet set")
        return self._root

    # def print_module(self, module: ModuleD):
    #     try:
    #         return self._module_ref_storage[module.name]
    #     except KeyError:
    #         pass
    #     printer: ModulePrinterT = self.get_printer(self._module_printers, module)
    #     result = printer.print_module(module)
    #     self._module_ref_storage[module.name] = result
    #     return result
    #
    # def print_function(self, foo: FunctionD):
    #     try:
    #         return self._function_storage[(foo.module, foo.name,)]
    #     except KeyError:
    #         pass
    #     printer: FunctionPrinterT = self.get_printer(self._function_printers, foo)
    #     result = printer.print_function(foo)
    #     self._function_storage[(foo.module, foo.name,)] = result
    #     return result
    #
    # def print_class(self, _class: ClassD):
    #     printer: ClassPrinterT = self.get_printer(self._class_printers, _class)
    #     return printer.print_class(_class)
    #
    # def print_method(self, method: MethodD):
    #     printer: MethodPrinterT = self.get_printer(self._method_printers, method)
    #     return printer.print_method(method)
    #
    # def print_object(self, obj: ObjectD):
    #     printer: ObjectPrinterT = self.get_printer(self._object_printers, obj)
    #     return printer.print_object(obj)
