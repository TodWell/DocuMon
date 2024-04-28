import pathlib

from DocuMon import ModuleD, ClassD, ObjectD, PropertyD
from DocuMon.core.elements.default_function import FunctionD
from DocuMon.core.elements.default_method import MethodD
from DocuMon.core.printers import ModularPrinter, ClassPrinter, FunctionPrinter, MethodPrinter, \
    ModulePrinter, ObjectPrinter
from DocuMon.core.printers.MdFile import MdFile


#
# class DefaultPrinter(AbsPrinter):
#
#     def __init__(self, root: pathlib.Path):
#         self._root = root
#
#     def print_module(self, module: ModuleD):
#         with MdFile(self._root / (module.name.replace(".", "/") + ".md")) as md:
#             md.title(module.title)
#             md.paragraph(module.doc)
#
#             if module.is_init and (module.path.parent / "README.md").is_file():
#                 md.title("README", 2)
#                 with open(module.path.parent / "README.md") as f:
#                     md.write_md(f.read(), indent=2)
#
#             md.title("Modules", 2)
#
#             for element in module.elements:
#                 if element.type != "module":
#                     continue
#                 new_module = self.print_module(element)
#                 md.element(f"[{element.title}]({new_module.rel_path(md.path)})" + (
#                     f": {element.description}" if element.description else ""))
#
#             def write_elements(element, indent, _filter):
#                 for sub_element in element.elements:
#                     if sub_element.type != _filter:
#                         continue
#                     element_md = self.print_element(sub_element)
#                     md.element(
#                         f"[{sub_element.title}]({element_md.rel_path(md.path)})" + (
#                             f": {sub_element.description}" if sub_element.description else ""
#                         ), indent=indent
#                     )
#                     if sub_element.elements:
#                         write_elements(sub_element, indent + 1, _filter)
#
#             md.title("Functions", 2)
#             write_elements(module, 0, "function")
#             md.title("Classes", 2)
#             write_elements(module, 0, "class")
#         return md
#
#     def print_class(self, _class: ClassD):
#         with MdFile(self._root / _class.module.replace(".", "/") / (_class.name + ".md")) as md:
#             md.title(_class.title)
#             md.paragraph(_class.doc)
#
#             md.title("Properties", indent=2)
#
#             for foo in _class.elements:
#                 if foo.type != "object":
#                     continue
#                 md.element(f"{foo.title}" + (f": {foo.description}" if foo.description else ""))
#
#             md.title("Methods", indent=2)
#
#             for foo in _class.elements:
#                 if foo.type != "method":
#                     continue
#                 foo_md = self.print_function(foo)
#                 md.element(
#                     f"[{foo.title}]({foo_md.rel_path(md.path)})" + (f": {foo.description}" if foo.description else ""))
#
#             md.title("Inner Classes", indent=2)
#
#             for foo in _class.elements:
#                 if foo.type != "class":
#                     continue
#                 foo_md = self.print_class(foo)
#                 md.element(
#                     f"[{foo.title}]({foo_md.rel_path(foo_md)})" + (f": {foo.description}" if foo.description else ""))
#         return md
#
#     def print_function(self, element: FunctionD):
#         with MdFile(self._root / element.module.replace(".", "/") / (element.name + ".md")) as md:
#             md.title(element.title)
#             md.paragraph(element.doc)
#
#             md.title("Arguments", indent=2)
#             for arg in element.args:
#                 md.element(f"`{arg.name}` ({arg.annotation}, default: `{arg.default}`): {arg.description}")
#             if element.add_args:
#                 md.element(
#                     f"`*` ({element.add_args.annotation}, default: `{element.add_args.default}`): {element.add_args.description}")
#             if element.kwargs:
#                 md.element(
#                     f"`**` ({element.kwargs.annotation}, default: `{element.kwargs.default}`): {element.kwargs.description}")
#
#             md.title("Returns", indent=2)
#             if isinstance(element.returns, list):
#                 for res in element.returns:
#                     md.element(f"`{res.annotation}`: {res.description}")
#             else:
#                 md.element(f"`{element.returns.annotation}`: {element.returns.description}")
#         return md
#
#     def print_method(self, element: MethodD):
#         with MdFile(self._root / element.module.replace(".", "/") / (element.name + ".md")) as md:
#             md.title(element.title)
#             md.paragraph(element.doc)
#
#             md.title("Arguments", indent=2)
#             for arg in element.args:
#                 md.element(f"`{arg.name}` ({arg.annotation}, default: `{arg.default}`): {arg.description}")
#             if element.add_args:
#                 md.element(
#                     f"`*` ({element.add_args.annotation}, default: `{element.add_args.default}`): {element.add_args.description}")
#             if element.kwargs:
#                 md.element(
#                     f"`**` ({element.kwargs.annotation}, default: `{element.kwargs.default}`): {element.kwargs.description}")
#
#             md.title("Returns", indent=2)
#             if isinstance(element.returns, list):
#                 for res in element.returns:
#                     md.element(f"`{res.annotation}`: {res.description}")
#             else:
#                 md.element(f"`{element.returns.annotation}`: {element.returns.description}")
#         return md
#
#     def print_element(self, element: DescriptorT):
#         if element.type == "module":
#             return self.print_module(element)
#         if element.type == "class":
#             return self.print_class(element)
#         if element.type == "function":
#             return self.print_function(element)
#         print(element.name)

class DefaultModularPrinter(ModularPrinter):
    pass


modular_printer = DefaultModularPrinter()


@modular_printer.module_printer(ModuleD)
class DefaultModulePrinter(ModulePrinter):

    def print_module(self, module: ModuleD):
        with MdFile(self.path(module)) as md:
            md.title(f"Module: {module.title}")
            md.paragraph(module.doc)
            md.title("Elements", 2)
            self.print_inner_summary(module, md, indent=0)

        self.parent.print_children(module)

    def print_summary(self, module: ModuleD, md: MdFile, indent=0, depht=-1):
        md.element(f"[{module.title}]({md.rel_path(self.path(module))}): {module.description}", indent)
        self.print_inner_summary(module, md, indent + 1)

    def print_inner_summary(self, module: ModuleD, md: MdFile, indent=0):
        md.element("Functions", indent)
        for element in module.type_iterator("function"):
            self.parent.get_function_printer(element).print_summary(element, md, indent + 1)
        md.element("Classes", indent + 0)
        for element in module.type_iterator("class"):
            self.parent.get_class_printer(element).print_summary(element, md, indent + 1)
        md.element("Properties", indent + 0)
        for element in module.type_iterator("object"):
            self.parent.get_object_printer(element).print_summary(element, md, indent + 1)
        md.element("Modules", indent)
        for element in module.type_iterator("module"):
            self.parent.get_module_printer(element).print_summary(element, md, indent + 1)

    def path(self, module: ModuleD):
        return self.parent.root / (module.module.replace(".", "/") + ".md")

    def rel_path(self, module, to: pathlib.Path):
        path = self.path(module)
        re_to = to if to.is_dir() else to.parent
        return path.relative_to(re_to)


@modular_printer.class_printer(ClassD)
class DefaultClassPrinter(ClassPrinter):

    def path(self, _class: ClassD) -> pathlib.Path:
        return self._parent.root / _class.module.replace(".", "/") / (_class.name + ".md")

    def print_class(self, _class: ClassD) -> MdFile:
        with MdFile(self.path(_class)) as md:
            md.title("Class: " + _class.title)
            md.paragraph(_class.doc)
            md.title("Properties", 2)
            for element in _class.type_iterator("object"):
                self._parent.get_object_printer(element).print_summary(element, md, indent=0)

            md.title("Methods", 2)
            for element in _class.type_iterator("method"):
                self._parent.get_method_printer(element).print_summary(element, md, indent=0)

            md.title("Inner Classes", 2)
            for element in _class.type_iterator("class"):
                self._parent.get_class_printer(element).print_summary(element, md, indent=0)

        self.parent.print_children(_class)

    def print_summary(self, _class: ClassD, md: MdFile, indent=0):
        md.element(f"[{_class.title}]({md.rel_path(self.path(_class))}): {_class.description}", indent)
        md.element("**Properties:**", indent=indent + 1)
        for element in _class.type_iterator("object"):
            self._parent.get_object_printer(element).print_summary(element, md, indent=indent + 2)

        md.element("**Methods:**", indent=indent + 1)
        for element in _class.type_iterator("method"):
            self._parent.get_method_printer(element).print_summary(element, md, indent=indent + 2)

        md.element("**InnerClasses:**", indent=indent + 1)
        for element in _class.type_iterator("class"):
            self._parent.get_class_printer(element).print_summary(element, md, indent=indent + 2)


@modular_printer.function_printer(FunctionD)
class DefaultFunctionPrinter(FunctionPrinter):

    def path(self, foo: FunctionD):
        return self._parent.root / foo.module.replace(".", "/") / (foo.name + ".md")

    def print_function(self, foo: FunctionD):
        with MdFile(self.path(foo)) as md:
            md.title("Function: " + foo.title)
            md.paragraph(foo.doc)
            md.title("Arguments", 2)
            for arg in foo.args:
                d = f" = {arg.default}" if arg.default else ""
                t = f": {arg.annotation}" if arg.annotation else ""
                td = t + d if (t + d) else ""
                md.element(f"`{arg.name}{td}`" + (f": {arg.description}" if arg.description else ""))

    def print_summary(self, foo: FunctionD, md: MdFile, indent=0, depht=-1):
        md.element(f"[{foo.title}]({md.rel_path(self.path(foo))}): {foo.description}", indent=indent)
        self.print_inner_summary(foo, md, indent=indent + 1)

    def print_inner_summary(self, foo: FunctionD, md: MdFile, indent=0):
        md.element("Arguments", indent)
        for arg in foo.args:
            md.element(f"{arg.name}: {arg.description}", indent + 1)
            if arg.annotation:
                md.element(f"Type: `{arg.annotation}`", indent + 2)
            if arg.default:
                md.element(f"Default: `{arg.default}`", indent + 2)
        if foo.add_args:
            md.element("Additional Arguments:", indent + 0)
            if foo.add_args.annotation:
                md.element(f"Type: `{foo.add_args.annotation}`", indent + 1)
            if foo.add_args.default:
                md.element(f"Default: `{foo.add_args.default}`", indent + 1)


@modular_printer.method_printer(MethodD)
class DefaultMethodPrinter(MethodPrinter):

    def print_summary(self, method: MethodD, md: MdFile, indent=0):
        md.element(f"[{method.title}]({md.rel_path(self.path(method))}): {method.description}", indent)
        self.print_inner_summary(method, md, indent + 1)

    def print_inner_summary(self, method: MethodD, md: MdFile, indent=0, depht=-1):
        for arg in method.args:
            md.element(f"{arg.name}: {arg.description}", indent)
            if arg.annotation:
                md.element(f"Type: `{arg.annotation}`", indent + 1)
            if arg.default:
                md.element(f"Default: `{arg.default}`", indent + 1)
        if method.add_args:
            md.element("Additional Arguments:", indent)
            if method.add_args.annotation:
                md.element(f"Type: `{method.add_args.annotation}`", indent + 1)
            if method.add_args.default:
                md.element(f"Default: `{method.add_args.default}`", indent + 1)

    def print_method(self, method: MethodD):
        with MdFile(self.path(method)) as md:
            md.title("Method: " + method.title)
            md.paragraph(f"Method of [Parent]({md.rel_path(self.parent_path(method))}).")
            md.paragraph(method.doc)
            md.title("Arguments", 2)
            self.print_inner_summary(method, md, indent=0)

    def path(self, method: MethodD) -> pathlib.Path:
        return self._parent.root / method.module.replace(".", "/") / (method.name + ".md")

    def parent_path(self, method: MethodD):
        return self.parent.root / method.module.replace(".", "/") / (method.class_name + ".md")


@modular_printer.object_printer(ObjectD)
class DefaultObjectPrinter(ObjectPrinter):

    def print_object(self, obj: ObjectD):
        pass

    def print_summary(self, obj: ObjectD, md: MdFile, indent=0, depht=-1):
        md.element(f"{obj.title}: {obj.description}", indent)

    def path(self, obj: ObjectD):
        return ""


@modular_printer.object_printer(PropertyD)
class DefaultPropertyPrinter(ObjectPrinter):

    def print_object(self, obj: ObjectD):
        pass

    def print_summary(self, obj: PropertyD, md: MdFile, indent=0, depht=-1):
        md.element(f"{obj.title} (property): {obj.description}", indent)

    def path(self, obj: ObjectD):
        return ""
