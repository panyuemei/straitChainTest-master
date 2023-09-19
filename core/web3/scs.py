import datetime
import hashlib
from typing import Union, Callable, Optional, Tuple, Any, Sequence
from eth_typing import ChecksumAddress, Address, HexStr
from eth_utils import is_checksum_address
from hexbytes import HexBytes
from toolz import assoc
from web3._utils.empty import Empty
from web3.datastructures import AttributeDict
from web3.module import Module
from web3.types import BlockIdentifier, Wei, ENS, _Hash32, TxParams, CallOverrideParams
from settings import settings
from core.ipfs.ipfs import IPFS, AsyncIPFS
from core.web3.account import Account
from core.web3.contract import Contract, AsyncContract
from core.web3.method import Method, default_root_munger
from core.web3.scs_rpc_abi import RPC


class BaseScs(Module):
    # account = Account()
    settings = settings
    # _default_account: Union[ChecksumAddress, Empty] = empty
    _default_account = settings.master_address
    _default_block: BlockIdentifier = "latest"
    gasPriceStrategy = None

    _gas_price: Method[Callable[[], Wei]] = Method(
        RPC.scs_gasPrice,
        mungers=None,
    )

    @property
    def account(self):
        return Account(self)

    def ipfs(self) -> IPFS | AsyncIPFS:
        if self.is_async:
            return AsyncIPFS(self)
        else:
            return IPFS(self)

    def contract(
            self, address=None, **kwargs: Any
    ) -> AsyncContract | Contract:
        address = self.web3.toChecksumAddress(address)
        if self.is_async:
            return AsyncContract(address, self)
        else:
            return Contract(address, self)

    def md5_sign(self, *args):
        params = ['' if param is None else str(param) for param in args]
        params_str = '&'.join(params + [self.settings.app_key])
        params_md5 = hashlib.md5(params_str.encode('utf-8')).hexdigest()
        params.append(params_md5)
        return params

    @property
    def default_block(self) -> BlockIdentifier:
        return self._default_block

    @default_block.setter
    def default_block(self, value: BlockIdentifier) -> None:
        self._default_block = value

    @property
    def default_account(self) -> Union[ChecksumAddress, Empty]:
        return self._default_account

    @default_account.setter
    def default_account(self, account: Union[ChecksumAddress, Empty]) -> None:
        self._default_account = account

    def block_id_munger(
            self,
            account: Union[Address, ChecksumAddress, ENS],
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Tuple[Union[Address, ChecksumAddress, ENS], BlockIdentifier]:
        """
        通用的(account, block_identifier)参数类型
        """
        if block_identifier is None:
            block_identifier = self.default_block
        return account, block_identifier

    def nonce_munger(self, address=None, block_identifier=None):
        if address is None:
            address = self.default_account
        if block_identifier is None:
            block_identifier = self.default_block
        return address, block_identifier

    _protocol_version: Method[Callable[[], str]] = Method(
        RPC.scs_protocolVersion,
        mungers=None,
    )

    _get_balance = Method(
        RPC.scs_getBalance,
        mungers=[block_id_munger]
    )

    _get_transaction_count = Method(
        RPC.scs_getTransactionCount,
        mungers=[nonce_munger]
    )

    _send_raw_transaction: Method[Callable[[Union[HexStr, bytes]], HexBytes]] = Method(
        RPC.scs_sendRawTransaction,
        mungers=[default_root_munger],
    )

    def call_munger(
            self,
            transaction: TxParams,
            block_identifier: Optional[BlockIdentifier] = None,
            state_override: Optional[CallOverrideParams] = None,
    ) -> Union[Tuple[TxParams, BlockIdentifier], Tuple[TxParams, BlockIdentifier, CallOverrideParams]]:  # noqa-E501
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.default_account):
            transaction = assoc(transaction, 'from', self.default_account)

        # TODO: move to middleware
        if block_identifier is None:
            block_identifier = self.default_block

        if state_override is None:
            return transaction, block_identifier
        else:
            return transaction, block_identifier, state_override

    _call: Method[Callable[[Union[HexStr, bytes], BlockIdentifier], HexBytes]] = Method(
        RPC.scs_call,
        mungers=[call_munger]
    )

    _get_block_transaction_count_by_hash = Method(
        RPC.scs_getBlockTransactionCountByHash,
        mungers=[default_root_munger]
    )

    _get_block_transaction_count_by_number = Method(
        RPC.scs_getBlockTransactionCountByNumber,
        mungers=[default_root_munger]
    )

    _get_code = Method(
        RPC.scs_getCode,
        mungers=[block_id_munger]
    )

    def estimate_gas_munger(
            self,
            transaction: TxParams,
            block_identifier: Optional[BlockIdentifier] = None
    ) -> Sequence[Union[TxParams, BlockIdentifier]]:
        if 'from' not in transaction and is_checksum_address(self.default_account):
            transaction = assoc(transaction, 'from', self.default_account)

        if block_identifier is None:
            params: Sequence[Union[TxParams, BlockIdentifier]] = [transaction]
        else:
            params = [transaction, block_identifier]

        return params

    _estimate_gas = Method(
        RPC.scs_estimateGas,
        mungers=[estimate_gas_munger]
    )

    def get_block_munger(
            self, block_identifier: BlockIdentifier, full_transactions: bool = None
    ) -> Tuple[BlockIdentifier, bool]:
        if full_transactions is None:
            full_transactions = False
        return block_identifier, full_transactions

    _get_block_by_hash = Method(
        RPC.scs_getBlockByHash,
        mungers=[get_block_munger]
    )

    _get_block_by_number = Method(
        RPC.scs_getBlockByNumber,
        mungers=[default_root_munger]
    )

    _get_transaction_receipt = Method(
        RPC.scs_getTransactionReceipt,
        mungers=[default_root_munger]
    )

    _get_transaction_by_hash = Method(
        RPC.scs_getTransactionByHash,
        mungers=[default_root_munger]
    )

    _last_block_number = Method(
        RPC.scs_blockNumber
    )

    _nft_mint: Method[Callable[..., _Hash32]] = Method(
        RPC.scs_nft_mint,
        mungers=[default_root_munger, md5_sign]
    )

    _nft_mint_alone: Method[Callable[..., _Hash32]] = Method(
        RPC.scs_nft_mint_alone,
        mungers=[default_root_munger, md5_sign]
    )

    _1155_nft_mint: Method[Callable[..., _Hash32]] = Method(
        RPC.scs_1155_nft_mint,
        mungers=[default_root_munger, md5_sign]
    )

    def deploy_contract_munger(self, count, address=None, app_id=None, contract_type=None):
        if address is None:
            address = self.default_account
        if app_id is None:
            app_id = self.settings.app_id
        ret = (address, count, app_id)
        if contract_type is not None:
            ret = ret + (contract_type, )
        return ret

    _deploy_contract: Method[Callable[..., _Hash32]] = Method(
        RPC.scs_deploy_contract,
        mungers=[deploy_contract_munger],
    )

    _contract_address_by_hash: Method[Callable[..., Address]] = Method(
        RPC.scs_contractAddressByHash,
        mungers=[default_root_munger]
    )

    _get_token_by_hash: Method[Callable[..., list[AttributeDict]]] = Method(
        RPC.scs_getTokenByHash,
        mungers=[default_root_munger]
    )

    _get_nft_list: Method[Callable[..., _Hash32]] = Method(
        RPC.scs_nft_list,
        mungers=[default_root_munger]
    )

    _get_evidence_contract_address = Method(
        RPC.scs_get_evidence_contract_address
    )

    def existing_evidence_munger(self, c_id, content, hex_sign, app_id=None, service_id=None):
        if app_id is None:
            app_id = self.settings.app_id
        if service_id is None:
            service_id = ''
        return app_id, service_id, c_id, content, hex_sign

    _existing_evidence = Method(
        RPC.scs_existing_evidence,
        mungers=[existing_evidence_munger, md5_sign]
    )

    _digital_collection_mint = Method(
        RPC.scs_digital_collection_mint,
        mungers=[default_root_munger, md5_sign]
    )

    _digital_collection_list = Method(
        RPC.scs_digital_collection_list,
        mungers=[default_root_munger]
    )

    _digital_collection_transaction = Method(
        RPC.scs_digital_collection_transaction,
        mungers=[default_root_munger, md5_sign]
    )

    _pangu_evidence = Method(
        RPC.scs_pangu_evidence,
        mungers=[default_root_munger, md5_sign]
    )

    _real_name_auth = Method(
        RPC.scs_real_name_auth,
        mungers=[default_root_munger, md5_sign]
    )

    _get_union_id_mint_count = Method(
        RPC.scs_get_unionId_mint_count,
        mungers=[default_root_munger, md5_sign]
    )


class AsyncScs(BaseScs):
    is_async = True

    @property
    async def last_block_number(self):
        return await self._last_block_number()

    @property
    async def protocol_version(self) -> str:
        return await self._protocol_version()

    @property
    async def gas_price(self) -> Wei:
        return await self._gas_price()

    @property
    async def evidence_contract_address(self):
        return await self._get_evidence_contract_address()

    async def get_transaction_count(self, address=None, block_identifier=None):
        return await self._get_transaction_count(address, block_identifier)

    @property
    async def nonce_pending(self):
        return await self.get_transaction_count(block_identifier='pending')

    async def get_balance(self, account):
        return await self._get_balance(account)

    async def call(self, content, tag='latest'):
        return await self._call(content, tag)

    async def send_raw_transaction(self, transaction: Union[HexStr, bytes]) -> HexBytes:
        return await self._send_raw_transaction(transaction)

    async def get_block_transaction_count_by_hash(self, block_hash):
        return await self._get_block_transaction_count_by_hash(block_hash)

    async def get_block_transaction_count_by_number(self, block_number):
        return await self._get_block_transaction_count_by_number(block_number)

    async def get_code(self, address):
        return await self._get_code(address)

    async def estimate_gas(self, transaction: dict):
        return await self._estimate_gas(transaction)

    async def get_block_by_hash(self, hash_str, full_transactions=None):
        return await self._get_block_by_hash(hash_str, full_transactions)

    async def get_block_by_number(self, number, full_transactions=None):
        return await self._get_block_by_number(number, full_transactions)

    async def get_transaction_receipt(self, hash_str):
        return await self._get_transaction_receipt(hash_str)

    async def get_transaction_by_hash(self, hash_str):
        return await self._get_transaction_by_hash(hash_str)

    async def mint(self,
                   count,
                   contract_address,
                   nft_name,
                   c_id,
                   nft_uri,
                   copy_right,
                   issuer,
                   operator,
                   remark,
                   collect_sn,
                   owner=None,
                   app_id=None,
                   service_id=None,
                   mint_type=0
                   ):
        if mint_type == 2:
            func = self._1155_nft_mint
        elif mint_type == 1:
            func = self._nft_mint_alone
        else:
            func = self._nft_mint
        # noinspection PyCallingNonCallable
        return await func(
            app_id or self.settings.app_id,
            nft_name,
            c_id,
            nft_uri,
            copy_right,
            issuer,
            operator,
            remark,
            count,
            owner or self.default_account,
            contract_address,
            collect_sn,
            service_id or self.settings.nft_service_id,
        )

    async def deploy_contract_get_hash(self, max_count: int, address=None, app_id=None, contract_type=None) -> _Hash32:
        return await self._deploy_contract(max_count, address, app_id, contract_type)

    async def contract_address_by_hash(self, tx_hash: _Hash32) -> Address:
        return await self._contract_address_by_hash(tx_hash)

    async def get_token_by_hash(self, hash_num):
        return await self._get_token_by_hash(hash_num)

    async def get_nft_list(self, address):
        return await self._get_nft_list(address)

    async def existing_evidence(self, c_id, content, hex_sign, *args, **kwargs):
        return await self._existing_evidence(c_id, content, hex_sign, *args, **kwargs)


class Scs(BaseScs):

    @property
    def last_block_number(self):
        return self._last_block_number()

    @property
    def protocol_version(self) -> str:
        return self._protocol_version()

    @property
    def gas_price(self) -> Wei:
        return self._gas_price()

    @property
    def evidence_contract_address(self):
        return self._get_evidence_contract_address()

    def get_transaction_count(self, address=None, block_identifier=None):
        return self._get_transaction_count(address, block_identifier)

    @property
    def nonce_pending(self):
        return self.get_transaction_count(block_identifier='pending')

    def get_balance(self, account):
        return self._get_balance(account)

    def send_raw_transaction(self, transaction: Union[HexStr, bytes]) -> HexBytes:
        return self._send_raw_transaction(transaction)

    def call(self, content, tag='latest'):
        return self._call(content, tag)

    def get_block_transaction_count_by_hash(self, block_hash):
        return self._get_block_transaction_count_by_hash(block_hash)

    def get_block_transaction_count_by_number(self, block_number):
        return self._get_block_transaction_count_by_number(block_number)

    def get_code(self, address):
        return self._get_code(address)

    def estimate_gas(self, transaction: dict):
        return self._estimate_gas(transaction)

    def get_block_by_hash(self, hash_str, return_all=False):
        return self._get_block_by_hash(hash_str, return_all)

    def get_block_by_number(self, number, return_all=False):
        return self._get_block_by_number(number, return_all)

    def get_transaction_receipt(self, hash_str):
        return self._get_transaction_receipt(hash_str)

    def get_transaction_by_hash(self, hash_str):
        return self._get_transaction_by_hash(hash_str)

    def mint(self,
             count,
             contract_address,
             nft_name,
             c_id,
             nft_uri,
             copy_right,
             issuer,
             operator,
             remark,
             collect_sn,
             owner=None,
             app_id=None,
             service_id=None,
             mint_type=0
             ):
        if mint_type == 2:
            func = self._1155_nft_mint
        elif mint_type == 1:
            func = self._nft_mint_alone
        else:
            func = self._nft_mint
        # noinspection PyCallingNonCallable
        return func(
            app_id or self.settings.app_id,
            nft_name,
            c_id,
            nft_uri,
            copy_right,
            issuer,
            operator,
            remark,
            count,
            owner or self.default_account,
            contract_address,
            collect_sn,
            service_id or self.settings.nft_service_id,
        )

    def mint_alone(self, *args, **kwargs):
        return self.mint(*args, **kwargs, mint_type=1)

    def mint_1155(self, *args, **kwargs):
        return self.mint(*args, **kwargs, mint_type=2)

    def deploy_contract_get_hash(self, max_count: int, address=None, app_id=None, contract_type=None) -> _Hash32:
        return self._deploy_contract(max_count, address, app_id, contract_type)

    def contract_address_by_hash(self, tx_hash: _Hash32) -> Address:
        return self._contract_address_by_hash(tx_hash)

    def get_token_by_hash(self, hash_num):
        return self._get_token_by_hash(hash_num)

    def get_nft_list(self, address):
        return self._get_nft_list(address)

    def existing_evidence(self, c_id, content, hex_sign, *args, **kwargs):
        return self._existing_evidence(c_id, content, hex_sign, *args, **kwargs)

    def digital_collection_mint(self,
                                count,
                                name,
                                c_id,
                                nft_uri,
                                copy_right,
                                issuer,
                                operator,
                                remark,
                                owner=None,
                                app_id=None):
        return self._digital_collection_mint(app_id or self.settings.app_id,
                                             name,
                                             c_id,
                                             nft_uri,
                                             copy_right,
                                             issuer,
                                             operator,
                                             remark,
                                             count,
                                             owner or self.settings.master_address)

    def digital_collection_list(self, hash_num):
        return self._digital_collection_list(hash_num)

    def scs_digital_collection_transaction(self,
                                           to,
                                           token_id,
                                           number,
                                           from_address=None,
                                           app_id=None):
        return self._digital_collection_transaction(app_id or self.settings.app_id,
                                                    from_address or self.settings.master_address,
                                                    to,
                                                    token_id,
                                                    number)

    def pangu_evidence(self,
                       pk,
                       issue_id,
                       second_issue_id,
                       desc,
                       value,
                       user_hash,
                       app_id=None):
        return self._pangu_evidence(app_id or self.settings.app_id,
                                    pk,
                                    issue_id,
                                    second_issue_id,
                                    desc,
                                    value,
                                    user_hash)

    def real_name_auth(self, auth_name, auth_number, img_base64, app_id=None):
        return self._real_name_auth(app_id or self.settings.app_id, auth_name, auth_number, img_base64)

    def get_union_id_mint_count(self, union_id, app_id=None, app_type=1):
        return self._get_union_id_mint_count(app_id or self.settings.app_id, union_id, app_type)
