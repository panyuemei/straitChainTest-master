from typing import TypeVar, Callable, Any, Generic, Optional, Type, TYPE_CHECKING, List
from web3.types import RPCEndpoint
if TYPE_CHECKING:
    from core.web3.contract_module import Module


TFunc = TypeVar('TFunc', bound=Callable[..., Any])


def default_result_formatter(result, *args, **kwargs):
    return result


class Method(Generic[TFunc]):

    def __init__(
            self,
            contract_method: Optional[RPCEndpoint] = None,
            chain_method: Callable[..., Any] = None,
            params_processor: Callable[..., Any] = None,
            result_formatters: List[Callable[..., Any]] | Callable[..., Any] = None,
            error_formatter: Callable[..., Any] = None,
    ):
        self.contract_method = contract_method
        self.chain_method = chain_method
        self.params_processor = params_processor
        if result_formatters is None:
            self.result_formatters = [default_result_formatter, ]
        elif not isinstance(result_formatters, list | tuple):
            self.result_formatters = [result_formatters]
        else:
            self.result_formatters = result_formatters

    def __get__(self, obj: Optional["Module"] = None,
                obj_type: Optional[Type["Module"]] = None) -> TFunc:
        if obj is None:
            raise TypeError(
                "Direct calls to methods are not supported. "
                "Methods must be called from an module instance, "
                "usually attached to a web3 instance.")
        return obj.retrieve_caller_fn(self)