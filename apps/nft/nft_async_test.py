import asyncio
import datetime
from core.web3.main import Web3
from settings import settings
from collections import Counter

w3 = Web3(Web3.AsyncHTTPProvider(settings.chain_url, request_kwargs=settings.request_kwargs))
scs = w3.async_scs

# 铸造成功耗时
success_times = []
# 首次请求铸造成功耗时
first_success_times = []
# 首次请求即铸造成功统计
first_success = 0
fail = []
request_count = 0
request_counts = []

retry = True
interval = 0

def average(data: list[int | float], r=2):
    if len(data) == 0:
        return 0
    return round(sum(data) / len(data), r)


async def mint(contract_address, start=None, request=None):
    global request_count
    global first_success
    beg = datetime.datetime.now().timestamp() if start is None else start
    if request is None:
        request = 0
    request_count += 1
    try:
        result = await scs.mint(1,
                                contract_address,
                                nft_name='武夷山藏品-单个',
                                c_id='',
                                nft_uri='http://nps.shang-chain.com:30023/profile/tmp/ahjdfhf.json',
                                copy_right='熵链科技版权',
                                issuer='熵链科技发行',
                                operator='熵链科技运营',
                                remark='武夷山世界遗产',
                                collect_sn='collect_sn',
                                use_alone=True)
        request_counts.append(request + 1)
        diff = round(datetime.datetime.now().timestamp() - beg, 2)
        success_times.append(diff)
        if start is None:
            first_success += 1
            first_success_times.append(diff)
        print(f'已请求数：{request_count}，剩余未铸造数：{c - len(success_times)}')
    except Exception as e:
        fail.append(str(e))
        print(e)
        print(f'已请求数：{request_count}，剩余未铸造数：{c - len(success_times)}')
        if retry:
            if interval:
                await asyncio.sleep(interval)
            return await mint(contract_address, beg, request + 1)
        fail.append(str(e))
        result = None
    return result


async def main(count: int):
    # 部署合约
    tx_hash = await scs.deploy_contract_get_hash(count)

    # 获取合约地址
    contract_address = None
    while contract_address is None:
        contract_address = await scs.contract_address_by_hash(tx_hash)
        if contract_address is None:
            await asyncio.sleep(1)
    print(f'合约地址：{contract_address}')

    # 铸造
    tasks = []
    for _ in range(count):
        task = asyncio.create_task(mint(contract_address))
        tasks.append(task)
    gather_result = await asyncio.gather(*tasks)
    success = list(filter(lambda x: x is not None, gather_result))
    print(f'铸造成功统计（共{len(success)}个）：')
    print(success)


if __name__ == '__main__':
    c = 500
    asyncio.run(main(c))
    if retry:
        assert len(success_times) == c, f'{len(success_times)} {c}'
    print(f'铸造失败统计（共{len(fail)}个）：')
    print(fail)
    print(f'失败类型统计：{dict(Counter(fail))}')

    print(f'等待铸造耗时统计（铸造成功平均耗时{average(success_times)}秒')
    print(success_times)

    print(f'等待铸造耗时统计（首次请求铸造成功平均耗时{average(first_success_times)}秒')
    print(first_success_times)

    print(f'共请求次数{request_count}，平均请求次数{round(request_count / c, 2)}')

    print(f'单次铸造最长耗时{max(success_times)}')

    print('*' * 200)
    print(f'不重试，首次请求即可成功铸造的数量: {first_success}')
    print(f'不重试，首次请求即成功的平均耗时：{average(first_success_times)}')
    print(f'不重试，首次请求即成功的最长单次铸造时间：{max(first_success_times)}')
    print(f'重试直到成功平均请求次数，请求次数：{request_count}')
    print(f'重试直到成功平均请求次数，请求次数 / 铸造数量：{round(request_count / c, 2)}')
    print(f'重试直到成功，单个铸造的最大请求次数：{max(request_counts)}')
    print(f'重试直到成功，从第一次请求到铸造成功的平均耗时：{average(success_times)}')
    print(f'重试直到成功，铸造成功的最长时间：{max(success_times)}')
    print('*' * 200)
