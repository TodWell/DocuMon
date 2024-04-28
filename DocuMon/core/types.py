from typing import TypeVar, Union

ModuleT = TypeVar("ModuleT")
ClassT = TypeVar("ClassT")
FunctionT = callable

ElementT = Union[ModuleT, ClassT, FunctionT]