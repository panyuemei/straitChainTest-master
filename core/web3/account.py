from typing import TYPE_CHECKING

from eth_account import Account as RawAccount
if TYPE_CHECKING:
    from core.web3.scs import Scs, BaseScs


class Account(RawAccount):
    def __init__(self, scs: 'Scs | BaseScs'):
        self.scs = scs

    def transfer_drop(self, to, value):
        return self.scs.contract(to).transfer_drop(value)
