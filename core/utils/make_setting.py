import os
import yaml
from eth_utils import to_hex


class Settings:
    def __init__(self, base_path, env, username=None, address=None, chain_name=None, use_urn_name='chain_urn'):
        conf_path = os.path.join(base_path, 'conf')
        config_path = os.path.join(conf_path, 'config.yaml')
        env_config_path = os.path.join(conf_path, f'config-{env}.yaml')
        accounts_config_path = os.path.join(conf_path, 'accounts.yaml')
        chains_config_path = os.path.join(conf_path, 'chains.yaml')

        self.config: dict = yaml.safe_load(open(config_path, encoding='utf-8'))
        self.env_config: dict = yaml.safe_load(open(env_config_path, encoding='utf-8'))
        self.accounts_config: list = yaml.safe_load(open(accounts_config_path, encoding='utf-8'))
        self.chains_config: list = yaml.safe_load(open(chains_config_path, encoding='utf-8'))

        self.jsonrpc = str(self.config['jsonrpc'])
        self.headers = self.config['default_request_headers']
        self.request_kwargs = self.config['request_kwargs']
        self.chain_func_prefix = self.config['chain_func_prefix']
        self.gas = to_hex(self.config['gas'])
        self.gas_price = self.config['gas_price']
        self.log_level = self.config['log_level']
        self.chain_url = self.env_config['chain_url'] + self.config[use_urn_name]

        user = list(filter(lambda x: x['username'] == username, self.env_config['accounts']))[0]
        account = list(filter(lambda x: x['address'] == (address or user['address']), self.accounts_config))[0]
        chain = list(filter(lambda x: x['chain_name'] == (chain_name or user['chain_name']), self.chains_config))[0]
        self.username = user.get('username', None)
        self.password = user.get('password', None)
        self.app_id = user['app_id']
        self.app_key = user['app_key']
        self.nft_service_id = user['nft_service_id']
        self.master_address = address or user['address']
        self.private_key = account['private_key']
        self.chain_code = chain['chain_code']
        self.chain_id = chain['chain_id']
        self.chain_id_hex = to_hex(self.chain_id)

        self.chain_url = self.env_config['chain_url'] + self.config[use_urn_name] + (
            f'?chainCode={self.chain_code}' if self.chain_code else '')
        self.IPFSUpload_url = self.env_config['chain_url'] + self.config['ipfs_urn']
