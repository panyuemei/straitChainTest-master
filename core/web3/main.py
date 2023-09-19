from typing import Optional, Sequence, Any, Union, Dict, Type, cast

from ens import ENS
from eth_abi.codec import ABICodec
from web3 import Web3 as W3
from web3._utils.abi import build_default_registry
from web3._utils.empty import empty
from web3.main import get_default_modules
from web3.module import Module
from web3.providers import BaseProvider
from core.web3.providers.rpc import HTTPProvider
from core.web3.manager import RequestManager
from core.web3.scs import Scs, AsyncScs


def get_default_modules_add_scs() -> Dict[str, Union[Type[Module], Sequence[Any]]]:
    """
    在default_modules中添加scs
    """
    default_modules = get_default_modules()
    default_modules.update({'scs': Scs, 'async_scs': AsyncScs})
    return default_modules


class Web3(W3):
    HTTPProvider = HTTPProvider
    RequestManager = RequestManager
    scs: Scs
    async_scs: AsyncScs

    def __init__(
        self,
        provider: Optional[BaseProvider] = None,
        middlewares: Optional[Sequence[Any]] = None,
        modules: Optional[Dict[str, Union[Type[Module], Sequence[Any]]]] = None,
        external_modules: Optional[Dict[str, Union[Type[Module], Sequence[Any]]]] = None,
        ens: ENS = cast(ENS, empty)
    ) -> None:
        self.manager = self.RequestManager(self, provider, middlewares)
        # this codec gets used in the module initialization,
        # so it needs to come before attach_modules
        self.codec = ABICodec(build_default_registry())

        if modules is None:
            # 添加scs
            modules = get_default_modules_add_scs()

        self.attach_modules(modules)

        if external_modules is not None:
            self.attach_modules(external_modules)

        self.ens = ens


