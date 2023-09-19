from typing import Optional, Union, Callable, Any
from ens import ENS
from eth_typing import Address, ChecksumAddress
from web3 import Web3
from web3._utils.method_formatters import to_integer_if_hex

from core.web3.contarct_call_method import default_scs_call_params_processor, default_chain_method_scs_call, \
    default_chain_method_scs_send_raw_transaction, sign_transaction_params_processor, \
    default_chain_method_scs_existing_evidence, default_chain_method_scs_existing_evidence_params_processor, \
    transfer_drop_params_processor
from core.web3.contract_method import Method
from core.web3.contract_module import Module
from core.web3.scs_rpc_abi import RPC


def address64_to_40(address: str):
    if address == '0x':
        return address
    if len(address) != 66 or not address.lower().startswith('0x'):
        raise ValueError(f'错误的address格式 {address}')
    return address[:2] + address[-40:]


def hex_formatter(hex_str: str):
    if hex_str == '0x':
        return hex_str
    else:
        return Web3.toHex(int(hex_str, 16))


def hex_str_to_int(hex_str):
    return Web3.toInt(hexstr=hex_str)


class BaseContract(Module):

    def __init__(self, address: Optional[Union[Address, ChecksumAddress, ENS]], *args, **kwargs):
        self.address = address
        super().__init__(*args, **kwargs)

    _get_owner = Method(
        RPC.ownerOf,
        chain_method=default_chain_method_scs_call,
        params_processor=default_scs_call_params_processor,
        result_formatters=address64_to_40
    )

    _transfer_from = Method(
        RPC.transferFrom,
        chain_method=default_chain_method_scs_send_raw_transaction,
        params_processor=sign_transaction_params_processor,
    )

    _transfer_drop = Method(
        chain_method=default_chain_method_scs_send_raw_transaction,
        params_processor=transfer_drop_params_processor
    )

    _token_uri = Method(
        RPC.tokenURI,
        chain_method=default_chain_method_scs_call,
        params_processor=default_scs_call_params_processor,
    )

    _total_supply = Method(
        RPC.totalSupply,
        chain_method=default_chain_method_scs_call,
        params_processor=default_scs_call_params_processor,
        result_formatters=[hex_formatter, to_integer_if_hex]
    )

    _evidence = Method(
        RPC.evidence,
        chain_method=default_chain_method_scs_existing_evidence,
        params_processor=default_chain_method_scs_existing_evidence_params_processor
    )

    # 4907 租赁功能
    _set_user = Method(
        RPC.setUser,
        chain_method=default_chain_method_scs_send_raw_transaction,
        params_processor=sign_transaction_params_processor,
    )

    _user_of = Method(
        RPC.userOf,
        chain_method=default_chain_method_scs_call,
        params_processor=default_scs_call_params_processor,
        result_formatters=address64_to_40
    )

    _user_expires = Method(
        RPC.userExpires,
        chain_method=default_chain_method_scs_call,
        params_processor=default_scs_call_params_processor,
        result_formatters=[hex_formatter, to_integer_if_hex]
    )

    # 1155合约
    _safe_transfer_from = Method(
        RPC.safeTransferFrom,
        chain_method=default_chain_method_scs_send_raw_transaction,
        params_processor=sign_transaction_params_processor,
    )

    _balance_of = Method(
        RPC.balanceOf,
        chain_method=default_chain_method_scs_call,
        params_processor=default_scs_call_params_processor
    )

    _balance_of_batch = Method(
        RPC.balanceOfBatch,
        chain_method=default_chain_method_scs_call,
        params_processor=default_scs_call_params_processor
    )


class AsyncContract(BaseContract):
    """
    实现异步调用合约方法
    需要用到nonce的，很难实现实时获取nonce去使用
    """
    is_async = True

    async def get_owner(self, token_id):
        return await self._get_owner(token_id)

    async def transfer_from(self, from_address, to_address, token_id):
        return await self._transfer_from(from_address, to_address, token_id,
                                         nonce=await self.scs.get_transaction_count(block_identifier='pending'))

    async def get_token_uri(self, token_id):
        return await self._token_uri(token_id)

    async def get_total_supply(self):
        return await self._total_supply()

    async def evidence(self, c_id, content):
        return await self._evidence(c_id, content,
                                    nonce=await self.scs.get_transaction_count(block_identifier='pending'))

    async def transfer_drop(self, value):
        """目标地址为合约地址"""
        return await self._transfer_drop(value, nonce=await self.scs.nonce_pending)


class Contract(BaseContract):

    def get_owner(self, token_id):
        return self._get_owner(token_id)

    def transfer_from(self, from_address, to_address, token_id):
        return self._transfer_from(from_address, to_address, token_id,
                                   nonce=self.scs.nonce_pending)

    def get_token_uri(self, token_id):
        return self._token_uri(token_id)

    def get_total_supply(self):
        return self._total_supply()

    def evidence(self, c_id, content):
        return self._evidence(c_id, content, nonce=self.scs.nonce_pending)

    def transfer_drop(self, value):
        """目标地址为合约地址"""
        return self._transfer_drop(value, nonce=self.scs.nonce_pending)

    def set_user(self, token_id, user, expires):
        return self._set_user(token_id, user, expires, nonce=self.scs.nonce_pending)

    def user_of(self, token_id):
        return self._user_of(token_id)

    def user_expires(self, token_id):
        return self._user_expires(token_id)

    def safe_transfer_from(self, from_address, to_address, token_id, amount, data):
        return self._safe_transfer_from(from_address, to_address, token_id, amount, data,
                                        nonce=self.scs.nonce_pending)

    def balance_of(self, account, token_id):
        return self._balance_of(account, token_id)

    def balance_of_batch(self, accounts, token_ids):
        return self._balance_of(accounts, token_ids)
