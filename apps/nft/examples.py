import asyncio
import time
from apps.nft.nft import NFT
from core.web3.main import Web3
from settings import test_settings, settings


def main_business():
    """
    主流程示例
    """
    nft = NFT()
    nft.set_settings(test_settings)
    count = 10
    # 部署合约
    ca = nft.deploy_contract(count)
    # 发起铸造
    s = nft.mint_data_insert(count, ca)
    # 获取铸造结果
    tokens = nft.get_token_by_hash(s)
    # 查询铸造hash状态
    token_id = 1
    mint_result_0 = nft.scs.get_transaction_receipt(tokens[token_id - 1]['hash'])
    assert (hash_status := mint_result_0.get('status')) == '0x1', f'第{token_id}个藏品铸造hash状态错误：{hash_status}'
    # 查询藏品owner
    assert (actual := nft.w3.toChecksumAddress(nft.get_owner(ca, token_id))) == (expect := nft.w3.toChecksumAddress(
        nft.settings.master_address)), f'藏品拥有者不正确，期望：{expect}， 实际：{actual}'
    # 转移
    to_address = '0x9b4F8a365aBE68cb065AfdB1a8835Da460114efb'
    tran_hash = nft.transfer_from(ca, to_address, token_id)
    for _ in range(10):
        tran_result = nft.scs.get_transaction_receipt(tran_hash)
        if tran_result:
            if (tran_status := tran_result.get('status')) == '0x1':
                break
            else:
                raise Exception(f'交易hash状态错误：{tran_status}')
        time.sleep(1)
    else:
        raise Exception('获取交易hash状态超时')
    # 查询藏品owner
    assert (actual := nft.w3.toChecksumAddress(nft.get_owner(ca, token_id))) == (
        expect := nft.w3.toChecksumAddress(to_address)), f'藏品拥有者不正确，期望：{expect}， 实际：{actual}'



def transfer_drop():
    """
    转账 1 Drop
    """
    nft = NFT()
    nft.set_settings(test_settings)
    to_address = '0xdcc8711651485388ee2100be8aaab0a0141a6a0a'
    nft.scs.contract(to_address).transfer_drop(1)


def async_example():
    """
    协程示例
    """
    async def run():
        scs = Web3(Web3.AsyncHTTPProvider(settings.chain_url)).async_scs
        await scs.get_balance(scs.settings.master_address)

    asyncio.run(run())


if __name__ == '__main__':
    # async_example()
    main_business()