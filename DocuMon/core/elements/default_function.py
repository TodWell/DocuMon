import dataclasses
import inspect
import itertools
import typing
from inspect import _ParameterKind
from typing import List, Optional, Any

from DocuMon.core.elements import AbsDescriptor
from DocuMon.core.logger import logger


@dataclasses.dataclass
class Argument:
    name: str
    default: Optional[Any] = None
    annotation: str = ""
    description: str = ""

@dataclasses.dataclass
class Returns:
    annotation: str
    description: str = ""


KEY_UNIFIIER_1 = {
    "Args": "args",
    "args*": "add_args",
    "_*": "add_args",
    "Kwargs": "kwargs",
    "args**": "kwargs",
    "_**": "kwargs",
    "Returns": "returns",
    "Results": "returns",
    "results": "returns"
}

class FunctionD(AbsDescriptor):
    args: List[Argument]
    add_args: Optional[Argument]
    kwargs: Optional[Argument]
    returns: typing.Union[Returns, List[Returns]]

    def __init__(self, extractor, element: callable):
        self.args = []
        self.add_args = None
        self.kwargs = None
        super().__init__(extractor, element)
        self.title = self.title + "(...)"
        signature = inspect.signature(element)
        arg_meta = {
            (KEY_UNIFIIER_1.get(k) or k): v for k, v in self._meta.items()
        }
        keyword_args = arg_meta.get("args") or {}
        for key, s in signature.parameters.items():
            if s.kind in [_ParameterKind.POSITIONAL_OR_KEYWORD, _ParameterKind.KEYWORD_ONLY]:
                self.args.append(Argument(
                    name=key,
                    default=s.default if s.default != inspect._empty else None,
                    annotation=s.annotation.__name__,
                    description=keyword_args.get(key) or ""
                ))
                continue
            if s.kind == _ParameterKind.VAR_POSITIONAL:
                pass
                self.add_args = Argument(
                    name=key,
                    description=arg_meta.get("add_args") or "",
                    annotation=s.annotation.__name__
                )
            if s.kind == _ParameterKind.VAR_KEYWORD:
                self.kwargs = Argument(
                    name=key,
                    description=arg_meta.get("kwargs") or "",
                    annotation=s.annotation.__name__
                )
                continue
            print("")
        try:
            is_tuple = signature.return_annotation._name == "Tuple"
        except AttributeError:
            is_tuple = False
        if is_tuple:
            self.returns = [
                Returns(
                    annotation=annotation.__name__,
                    description=element
                ) for element, annotation in itertools.zip_longest(arg_meta.get("returns") or [], signature.return_annotation.__args__, fillvalue="")
            ]
        elif arg_meta.get("returns") and isinstance(arg_meta.get("returns"), list):
            if signature.return_annotation != inspect._empty and len(arg_meta["returns"]) != 1:
                logger.warning("Got a list of return values but a not matching annotation")
                return
            if signature.return_annotation != inspect._empty and len(arg_meta["returns"]) == 1:
                self.returns = Returns(
                    annotation="",
                    description=arg_meta["returns"][0]
                )
            else:
                self.returns = [
                    Returns(
                        annotation="Any",
                        description=element
                    ) for element in arg_meta["returns"]
                ]
        else:
            self.returns = Returns(
                annotation=signature.return_annotation.__name__,
                description=arg_meta.get("returns") or ""
            )

