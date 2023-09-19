from typing import TYPE_CHECKING

from eth_typing import HexStr
from eth_utils import function_signature_to_4byte_selector, to_hex
from hexbytes import HexBytes
from web3._utils.abi import map_abi_data
from web3._utils.normalizers import abi_ens_resolver, abi_address_to_hex, abi_bytes_to_bytes, abi_string_to_text

from core.web3.datatypes import AbiInputType
from core.web3.scs_rpc_abi import RPC_SCS_ABIS

if TYPE_CHECKING:
    from core.web3.main import Web3
import json


def get_params_list(params):
    """
    当传入dict时，按顺序取value组成列表
    当传入list或tuple时，直接返回
    其余，将值组合为列表的index=0
    :param params:
    :return:
    """
    if isinstance(params, dict):
        params_list = list(map(lambda x: '' if x is None else x, [val for idx, val in params.items()]))
    elif not (isinstance(params, list) or isinstance(params, tuple)):
        params_list = [params]
    else:
        params_list = params
    return params_list


def encode_abi(web3: "Web3", method: str, params) -> HexStr:
    """
    对合约方法进行编码
    """
    params = get_params_list(params)
    normalizers = [
        abi_ens_resolver(web3),
        abi_address_to_hex,
        abi_bytes_to_bytes,
        abi_string_to_text,
    ]
    if len(params) == 0:
        param_type = []
    else:
        param_type = RPC_SCS_ABIS[method]
    # param_type = []
    # for param in params:
    #     assert isinstance(param, AbiInputType), f'参数{param!r}类型应为{AbiInputType}，得到{type(param)}'
    #     param_type.append(param.type)
    # try:
    #     param_type = [param.type for param in params]
    # except AttributeError:
    #     raise AttributeError('参数类型必须定义为<AbiInputType>')
    normalized_params = map_abi_data(
        normalizers,
        param_type,
        params,
    )
    encoded_params = web3.codec.encode_abi(
        param_type,
        normalized_params,
    )
    event_signature_str = f'{method}({",".join(param_type)})'
    fn_selector = function_signature_to_4byte_selector(event_signature_str)
    return to_hex(HexBytes(fn_selector) + encoded_params)