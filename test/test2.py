import asyncio

from settings import settings
from core.web3.main import Web3

contract_address = Web3.toChecksumAddress('0x935b0cf837a576a9519462c34d97ead815091e40')
to_address = Web3.toChecksumAddress('0x98a309d087ba9408ea48ae778eda961b9c534ed8')

contract_addresses = iter([
    Web3.toChecksumAddress('0xf8bb445368d0e1d3295139d4e9f98d99b228d5a6'),
    Web3.toChecksumAddress('0x2251f69321910be201ceeab15f3215abd589bf98')
])

hashs = iter(['0xb88d179eb9d5be43fed64e812dc79d900b39b535b0a88b79ae855b02171c5d5f',
              '0xdc3391f2f7d4a4ef1c33a2e7571df5e2926c1a91f2f2ad8fd7b5e87e5c92b55c'])

mint_hashes = iter([
    '326425a2e3f04cb0bfb98af4fab15381',
    '7d86747a85a0496b9f565e75d1f5488b',
])


def sync_test(attr, *args, **kwargs):
    scs = Web3(Web3.HTTPProvider(settings.chain_url)).scs
    # result = getattr(scs, attr)(*args, **kwargs)
    result = getattr(scs, attr)
    print(result)


def async_test(attr, *args, **kwargs):
    async def task():
        scs = Web3(Web3.AsyncHTTPProvider(settings.chain_url)).async_scs
        # result = await getattr(scs, attr)(*args, **kwargs)
        result = await getattr(scs, attr)
        print(result)
        return result

    asyncio.run(task())


def run():
    print(f'{"-" * 20}开始同步测试{"-" * 20}')
    sync_test(func_name, *params)
    print(f'{"-" * 20}结束同步测试{"-" * 20}')

    print('*' * 100)
    print(f'{"-" * 20}开始异步测试{"-" * 20}')
    # async_test(func_name, *params)
    print(f'{"-" * 20}结束异步测试{"-" * 20}')


if __name__ == '__main__':
    func_name = 'evidence_contract_address'
    params = []
    run()
