import pathlib

from DocuMon import extractor
from DocuMon.core.printers.default_printer import modular_printer
import example
print("hello")

modular_printer.set_root(pathlib.Path(r"C:\Users\todue\OneDrive\Desktop\tmp"))
module_tree = extractor.process_module(example)

modular_printer.print_module(module_tree)
