from eth_utils import to_checksum_address


class AbiInputType:
    data_type = None

    def __init__(self, data, name=None):
        self.type = self.data_type
        self.data = data
        self.name = name


class Address(str, AbiInputType):
    data_type = 'address'

    def __new__(cls, address):
        return super().__new__(cls, to_checksum_address(address))

class Uint256(int, AbiInputType):
    data_type = 'uint256'


class String(str, AbiInputType):
    data_type = 'string'
