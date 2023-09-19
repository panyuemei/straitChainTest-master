import base64
import os
import random
import time
from functools import partial
from typing import Dict, TYPE_CHECKING

import asyncio
from eth_account.signers.local import LocalAccount
from tenacity import retry as raw_retry, wait_fixed, stop_after_delay, retry_if_exception_type, retry_if_result
if TYPE_CHECKING:
    from core.utils.make_setting import Settings
from core.web3.datatypes import Address
from settings import settings
from core.logger import logger
from core.web3.main import Web3

# 自定义偏函数，默认的重试装饰器。e.g. @retry()
retry = partial(
    raw_retry,
    wait=wait_fixed(1),
    stop=stop_after_delay(10),
    retry=retry_if_exception_type(AssertionError),
    reraise=True)


def is_None(value):
    return value is None


class BaseNFT:
    ...


class NFT(BaseNFT):
    def __init__(self, w3: "Web3" = None):
        self.w3 = w3 or Web3(Web3.HTTPProvider(settings.chain_url, request_kwargs=settings.request_kwargs))
        self.scs = self.w3.scs
        self.async_scs = self.w3.async_scs  # 暂不支持异步
        self.settings = self.scs.settings

    def set_settings(self, setting: "Settings"):
        self.scs.settings = self.settings = setting

    @logger('部署合约')
    def deploy_contract(self, count, address=None, app_id=None, contract_type=None):
        # contract_type 普通合约：None, 4907可租赁：1，1155可定量：2
        tx_hash = self.scs.deploy_contract_get_hash(count, address, app_id, contract_type)
        return self.get_contract_address(tx_hash)

    @raw_retry(wait=wait_fixed(1), stop=stop_after_delay(60), reraise=True, retry=retry_if_result(lambda x: x is None))
    @logger('获取合约地址')
    def get_contract_address(self, tx_hash):
        contract_address = self.scs.contract_address_by_hash(tx_hash)
        return contract_address

    @logger('铸造返回铸造hash')
    def mint_data_insert(
            self,
            count,
            contract_address,
            nft_name='武夷山藏品',
            c_id='',
            nft_uri='https://cdnstrait.shang-chain.com/default/test.json',
            copy_right='熵链科技版权',
            issuer='熵链科技发行',
            operator='熵链科技运营',
            remark='武夷山世界遗产',
            collect_sn='collect_sn',
            *args,
            **kwargs
    ):
        return self.scs.mint(count, contract_address, nft_name, c_id, nft_uri, copy_right, issuer, operator, remark,
                             collect_sn, *args, **kwargs)

    @raw_retry(wait=wait_fixed(3), reraise=True, retry=retry_if_result(lambda x: x is None))
    @logger('获取铸造结果')
    def get_token_by_hash(self, hash_num):
        try:
            tokens = self.scs.get_token_by_hash(hash_num)
            return tokens
        except ValueError as e:
            error_msg = str(e)
            if ('铸造中' in error_msg) or ('转移中' in error_msg):
                return None
            else:
                raise e

    @logger('铸造')
    def mint(self, count, contract_type=None, **kwargs):
        contract_address = self.deploy_contract(count, contract_type=contract_type)
        return self.mint_data_insert(count, contract_address, **kwargs)

    @logger('铸造一个')
    def mint_alone(self, contract_address, count=1, **kwargs):
        return self.mint_data_insert(count, contract_address, mint_type=1, **kwargs)

    @logger('1155铸造')
    def mint_1155(self, contract_address, count, **kwargs):
        return self.mint_data_insert(count, contract_address, mint_type=2, **kwargs)

    @logger('铸造并等待结果')
    def mint_and_wait_result(self, count, contract_type=None, **kwargs):
        mint_hash = self.mint(count, contract_type, **kwargs)
        return self.get_token_by_hash(mint_hash)

    @logger('转移')
    def transfer_from(self, contract_address, to_address, token_id):
        return self.scs.contract(contract_address).transfer_from(Address(self.scs.settings.master_address),
                                                                 Address(to_address), token_id)

    @logger('获取藏品拥有者')
    def get_owner(self, contract_address, token_id):
        return self.scs.contract(contract_address).get_owner(token_id)

    @logger('存证（临时放在这）')
    def evidence(self, c_id, content, contract_address=None):
        if contract_address is None:
            contract_address = self.scs.evidence_contract_address
        return self.scs.contract(contract_address).evidence(c_id=c_id, content=content)

    @logger('身份三要素认证')
    def real_name_auth(self, auth_name, auth_number, img_path):
        with open(img_path, 'rb') as f:
            return self.scs.real_name_auth(auth_name, auth_number, str(base64.b64encode(f.read()), 'UTF-8'))


if __name__ == '__main__':
    nft = NFT()
    nft.scs.get_union_id_mint_count('1511896195545976832')
