"""
author: TDU
description: Bla bal
---
Some info
"""
from typing import Tuple

CONST = "SOME constant string"  # This string can be use for stuff

"""
# Section
"""

def some_fun_function(a: str, b: float, *args, **kwargs) -> Tuple[int, str]:
    """
    author: TDU
    description: Anything
    raises: NotImplemented
    args:
        a: input a
        b: input b
    args*: other parameters
    args**: kwarg parameters
    ---
    This stuff is really cool
    ```python
    # Code in action
    some_fun_function("a", 1.2)
    ```
    """
    raise NotImplemented("")

class SomeClass:
    """
    author: TDU
    description: Further description
    ---
    This class is also fun
    """

    a: int = 1# a description
    b: str  # b description

    def __init__(self, a: int, b: int):
        """
        ---
        Some info
        """
        self.a = a
        self.b = str(b)

    def return_a(self) -> int:
        """
        author: TDU
        description: hey
        returns: Some element
        ---
        bd
        """
        return self.a

    @property
    def aa(self) -> int:
        """
        author: TDU
        description: Property description
        ---
        """
        return self.a

    class Innter:
        b: str

class SomeSubclass(SomeClass):

    def return_b(self):
        return self.b

    def return_a(self) -> int:
        pass

