from typing import TYPE_CHECKING, Any
from hexbytes import HexBytes
from core.web3.encoder import encode_abi

if TYPE_CHECKING:
    from core.web3.contract_method import Method
    from core.web3.contract import Contract


def default_scs_call_params_processor(contract: 'Contract', method: 'Method', *args):
    """
    默认的scs_call参数处理器
    """
    encode_txn = encode_abi(contract.scs.web3, method.contract_method, args)
    params = [
        {
            'from': contract.scs.default_account,
            'to': contract.address,
            'gas': contract.scs.settings.gas,
            'gasPrice': '',
            'value': '',
            'data': encode_txn
        },
        'latest'
    ]
    return params


def sign_transaction_params_processor(contract: 'Contract', method: 'Method', *args, **kwargs):
    encode_txn = encode_abi(contract.scs.web3, method.contract_method, args)
    transaction = {
        'nonce': kwargs['nonce'],
        'gas': kwargs.get('gas', contract.scs.settings.gas),
        'gasPrice': kwargs.get('gas_price', contract.scs.settings.gas_price),
        'to': contract.address,
        'value': kwargs.get('value', '0x0'),
        'data': encode_txn,
        'chainId': contract.scs.settings.chain_id_hex
    }
    signed_txn = contract.scs.account.sign_transaction(transaction, contract.scs.settings.private_key)
    return [HexBytes(signed_txn.rawTransaction).hex()]


def transfer_drop_params_processor(contract: 'Contract', method: 'Method', *args, **kwargs):
    # encode_txn = encode_abi(contract.scs.web3, method.contract_method, args)
    transaction = {
        'nonce': kwargs['nonce'],
        'gas': kwargs.get('gas', contract.scs.settings.gas),
        'gasPrice': kwargs.get('gas_price', contract.scs.settings.gas_price),
        'to': contract.address,     # 目标地址
        'value': contract.scs.web3.toWei(args[0], 'ether'),
        # 'data': '',
        'data': '202212161541443369983337',
        'chainId': contract.scs.settings.chain_id_hex
    }
    signed_txn = contract.scs.account.sign_transaction(transaction, contract.scs.settings.private_key)
    return [HexBytes(signed_txn.rawTransaction).hex()]


def default_chain_method_scs_existing_evidence_params_processor(contract: 'Contract', method: 'Method', *args, **kwargs):
    sign_txn = sign_transaction_params_processor(contract, method, *args, **kwargs)
    return [*args, *sign_txn]


def default_chain_method_scs_call(contract: 'Contract', method: 'Method', *args, **kwargs):
    return contract.scs.call


def default_chain_method_scs_send_raw_transaction(contract: 'Contract', method: 'Method', *args, **kwargs):
    return contract.scs.send_raw_transaction


def default_chain_method_scs_existing_evidence(contract: 'Contract', method: 'Method', *args, **kwargs):
    return contract.scs.existing_evidence
