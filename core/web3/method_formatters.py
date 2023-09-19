from typing import Dict, Callable, Any, Union

from cytoolz.functoolz import compose
from eth_utils import is_0x_prefixed, is_integer
from eth_utils.curried import apply_formatter_if
from web3._utils.method_formatters import to_integer_if_hex, ERROR_FORMATTERS, combine_formatters
from web3.types import RPCEndpoint, RPCResponse
from core.web3.scs_rpc_abi import RPC


def no_raise_on_minting(response: RPCResponse) -> RPCResponse:
    print(response)
    return response


# 使用scs规范格式化result
PYTHONIC_RESULT_FORMATTERS: Dict[RPCEndpoint, Callable[..., Any]] = {
    # Scs
    RPC.scs_gasPrice: to_integer_if_hex,
    RPC.scs_protocolVersion: compose(
        apply_formatter_if(is_0x_prefixed, to_integer_if_hex),
        apply_formatter_if(is_integer, str),
    ),
    RPC.scs_getBalance: to_integer_if_hex,
    RPC.scs_getBlockTransactionCountByHash: to_integer_if_hex,
    RPC.scs_getBlockTransactionCountByNumber: to_integer_if_hex,
    RPC.scs_estimateGas: to_integer_if_hex,
    RPC.scs_blockNumber: to_integer_if_hex
}


def get_error_formatters(
        method_name: Union[RPCEndpoint, Callable[..., RPCEndpoint]],
        *args
) -> Callable[..., Any]:
    """
    目前有两处error_formatters来源（Method(error_formatters)、error_formatter_maps），新增*args，整合两处的formatters
    TODO: 将error_formatters唯一化
    """
    error_formatter_maps = (ERROR_FORMATTERS,)
    formatters = combine_formatters(error_formatter_maps, method_name)

    return compose(*args, *formatters)
