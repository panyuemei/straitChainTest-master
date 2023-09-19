import json
from dataclasses import asdict, dataclass
from pprint import pprint
from typing import Optional

import rlp
from eth_typing import HexStr
from eth_utils import keccak, to_bytes
from rlp.sedes import Binary, big_endian_int, binary
from web3 import Web3
from web3.auto import w3


class Transaction(rlp.Serializable):
    fields = [
        ("nonce", big_endian_int),
        ("gasPrice", big_endian_int),
        ("gas", big_endian_int),
        ("to", Binary.fixed_length(20, allow_empty=True)),
        ("value", big_endian_int),
        ("data", binary),
        ("v", big_endian_int),
        ("r", big_endian_int),
        ("s", big_endian_int),
    ]


@dataclass
class DecodedTx:
    hash_tx: str
    from_: str
    to: Optional[str]
    nonce: int
    gas: int
    gasPrice: int
    value: int
    data: str
    chainId: int
    r: str
    s: str
    v: int


def hex_to_bytes(data: str) -> bytes:
    return to_bytes(hexstr=HexStr(data))


def decode_raw_tx(raw_tx: str):
    tx = rlp.decode(hex_to_bytes(raw_tx), Transaction)
    hash_tx = Web3.toHex(keccak(hex_to_bytes(raw_tx)))
    from_ = w3.eth.account.recover_transaction(raw_tx)
    to = w3.toChecksumAddress(tx.to) if tx.to else None
    data = w3.toHex(tx.data)
    r = hex(tx.r)
    s = hex(tx.s)
    chainId = (tx.v - 35) // 2 if tx.v % 2 else (tx.v - 36) // 2
    return DecodedTx(hash_tx, from_, to, tx.nonce, tx.gas, tx.gasPrice, tx.value, data, chainId, r, s, tx.v)


def main():
    # raw_tx = "0xf8a910850684ee180082e48694a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4880b844a9059cbb000000000000000000000000b8b59a7bc828e6074a4dd00fa422ee6b92703f9200000000000000000000000000000000000000000000000000000000010366401ba0e2a4093875682ac6a1da94cdcc0a783fe61a7273d98e1ebfe77ace9cab91a120a00f553e48f3496b7329a7c0008b3531dd29490c517ad28b0e6c1fba03b79a1dee"  # noqa
    raw_tx = "0xf8738211808583156a3e07830249f0946d61dbfb32599cd94fee1c8fab1e80e2ee8623d8880d04ffa0af34b4d88084026911ada0a8b09bb28f72a4bf4847431a94098964965cf35f95dda51704fa65b7b84aba91a03b65af764f3dc80948ea89d6bc7fb1ebd812c638195df7bd92540202c5c0eb45"  # noqa
    res = decode_raw_tx(raw_tx)
    result = asdict(res)
    print(json.dumps(result))


if __name__ == "__main__":
    main()