from eth_keys import keys
from web3 import Web3
from settings import settings


def private_key_to_public_key(private_key):
    p = Web3.toBytes(hexstr=private_key)
    pk = keys.PrivateKey(p)
    return pk.public_key.to_hex()


def private_key_to_address(private_key):
    p = Web3.toBytes(hexstr=private_key)
    pk = keys.PrivateKey(p)
    return pk.public_key.to_checksum_address()


if __name__ == '__main__':
    print(private_key_to_public_key(settings.private_key))
    print(private_key_to_address(settings.private_key))