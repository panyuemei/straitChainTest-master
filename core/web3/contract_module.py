from typing import Callable, Union, Any, TypeVar, TYPE_CHECKING

from toolz import pipe
from web3._utils.filters import LogFilter

from settings import settings
from core.web3.contract_method import Method
from eth_utils.toolz import curry

if TYPE_CHECKING:
    from core.web3.scs import Scs, AsyncScs
    from core.web3.contract import Contract

TReturn = TypeVar('TReturn')


def default_scs_call_params_process(to, from_address=settings.master_address, gas=settings.gas, gas_price='', value='',
                                    data='', block_identifier='latest') -> list:
    return [
        {
            'from': from_address,
            'to': to,
            'gas': gas,
            'gasPrice': gas_price,
            'value': value,
            'data': data
        },
        block_identifier
    ]


@curry
def retrieve_contract_method_call_fn(
        scs: "Scs", contract: "Contract", method: Method[Callable[..., TReturn]]
) -> Callable[..., Union[TReturn, LogFilter]]:
    def caller(*args: Any, **kwargs: Any) -> Union[TReturn, LogFilter]:
        params = method.params_processor(contract, method, *args, **kwargs)
        chain_method = method.chain_method(contract, method, *args, **kwargs)
        return pipe(chain_method(*params), *method.result_formatters)

    return caller


@curry
def retrieve_async_method_call_fn(
        scs: "Scs", contract: "Contract", method: Method[Callable[..., TReturn]]
) -> Callable[..., Union[TReturn, LogFilter]]:
    async def caller(*args: Any, **kwargs: Any) -> Union[TReturn, LogFilter]:
        params = method.params_processor(contract, method, *args, **kwargs)
        chain_method = method.chain_method(contract, method, *args, **kwargs)
        result = await chain_method(*params)
        return pipe(result, *method.result_formatters)

    return caller


class Module:
    is_async = False

    def __init__(self, scs: Union["Scs", "AsyncScs"]) -> None:
        if self.is_async:
            self.retrieve_caller_fn = retrieve_async_method_call_fn(scs, self)
        else:
            self.retrieve_caller_fn = retrieve_contract_method_call_fn(scs, self)
        self.scs = scs
