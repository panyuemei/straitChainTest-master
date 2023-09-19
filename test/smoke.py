import random
import unittest
from apps.nft.nft import NFT


class NFTTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.nft = NFT()
        super().__init__(*args, **kwargs)

    def test_mint(self):
        count = random.randint(1, 100)
        res = self.nft.mint_and_wait_result(count)
        self.assertTrue(len(res) == count, "铸造发起数量与铸造结果数量不符")  # 总数
        self.assertTrue(all([map(lambda x: x in [y['tokenId'] for y in res], list(range(1, count + 1)))]),
                        '铸造返回tokenId异常')  # tokenId一对一
        self.assertTrue(len(set([x['hash'] for x in res])) == count, '铸造返回hash存在重复项')  # hash去重

    def test_transfer_from(self):
        self.nft.mint_and_wait_result(5)
        self.nft.transfer_from()


if __name__ == '__main__':
    unittest.main()
