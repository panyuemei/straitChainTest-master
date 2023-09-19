import sys
import os

sys.path.insert(2, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import datetime
import math
import random
import pymysql
import requests
from PIL import Image
from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
import uuid
from settings import settings
from apps.nft.nft import NFT
from core.logger import log
from core.web3.main import Web3
from apscheduler.schedulers.blocking import BlockingScheduler


class Million:
    def __init__(self):
        self.target_count = 1100000
        self.end_date = datetime.date(2022, 5, 31)
        self.w3 = Web3(Web3.HTTPProvider(settings.chain_url))
        self.scs = self.w3.scs
        self.nft = NFT(self.w3)
        self.ipfs = self.scs.ipfs()
        self.db = pymysql.connect(host='175.24.234.243', user='root', password='1669971502', database='straits_temp')
        self.cursor = self.db.cursor()
        self.base_url = 'http://nps.shang-chain.com:30023/profile/nft/'
        self.base_file_path = '/home/profile/nft'
        self.img_path = os.path.join(self.base_file_path, 'img')
        self.json_path = os.path.join(self.base_file_path, 'json')
        self.cid_cache_file = open('../../test/tools/cid_cache.txt', 'a', encoding='utf-8')
        self.mint_cache_file = open('../../test/tools/mint_cache.txt', 'a', encoding='utf-8')
        self.mint_count_pool = [*[3000] * 1, *[5000] * 2, *[8000] * 2, *[10000] * 6, *[20000] * 1]

    @property
    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def today(self):
        return datetime.date.today()

    @property
    def uid(self):
        return ''.join(str(uuid.uuid4()).split('-'))

    def random_planned_execute_time(self, today=None):
        if today is None:
            today = self.today
        start = int(datetime.datetime(today.year, today.month, today.day, 7, 0, 0).timestamp())
        end = int(datetime.datetime(today.year, today.month, today.day, 22, 0, 0).timestamp())
        random_timestamp = random.randint(start, end)
        return datetime.datetime.fromtimestamp(random_timestamp)

    def random_account(self):
        account: LocalAccount = self.scs.account.create()
        address = account.address
        private_key = HexBytes(account.key).hex()
        return address, private_key

    def commit_sql(self, sql, *args):
        try:
            self.cursor.execute(sql, *args)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def refresh_img_hash(self, file_name: str | list = None):
        """
        刷新图片的hash，出错时可再次上传至IPFS
        """
        if file_name is None:
            files = self.get_new_files_list()
        elif isinstance(file_name, str):
            files = [file_name]
        elif isinstance(file_name, list):
            files = file_name
        else:
            raise ValueError(f'参数错误{file_name}')
        for file in files:
            if file.split('.')[-1].lower() in ['png', 'jpg', 'jpeg']:
                file_path = os.path.join(self.img_path, file)
                log.debug(f'重置文件 [{file_path}] hash')
                img_file = Image.open(file_path)
                img_file.save(file_path, quality=96)

    @staticmethod
    def get_name_by_file(file_name: str):
        return '.'.join(file_name.split('.')[:-1])

    def get_new_files_list(self):
        sql = 'SELECT file_name FROM token_uri'
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db_files = [self.get_name_by_file(i[0]) for i in result]
        files = os.listdir(self.img_path)
        new_files = []
        for file in files:
            if self.get_name_by_file(file) not in db_files:
                new_files.append(file)
        return new_files

    def insert_token_uri_to_db(self, file_name, c_id):
        """填充token_uri表"""
        file_path = os.path.join(self.img_path, file_name)
        file_url = os.path.join(self.base_url, 'img/' + file_name)
        json_url = os.path.join(self.base_url, 'json/' + self.get_name_by_file(file_name) + '.json')
        now = self.now
        sql = f'INSERT INTO token_uri (file_name, c_id, file_path, file_url, json_url, created) ' \
              f'VALUES ' \
              f'("{file_name}", "{c_id}", "{file_path}", "{file_url}", "{json_url}", "{now}")'
        log.info(f'数据库存储sql={sql}')
        self.cursor.execute(sql)

    def upload_ipfs(self, file_name):
        file_path = os.path.join(self.img_path, file_name)
        log.debug(f'上传文件{file_path}')
        c_id = self.ipfs.upload(file_path)
        log.debug(f'获取c_id={c_id}')
        self.cid_cache_file.write(f'{c_id},{file_name}\n')
        return c_id

    def make_json(self, file_name):
        file_url = os.path.join(self.base_url, 'img/' + file_name)
        name = self.get_name_by_file(file_name)
        content = f'"attributes":[],"image":"{file_url}","name":"{name}"'
        json_name = os.path.join(self.json_path, name + '.json')
        log.debug(f'创建json文件path={json_name} content={content}')
        with open(json_name, 'w', encoding='utf-8') as f:
            f.write(content)

    def init_mint_file(self):
        new_files = self.get_new_files_list()
        log.info(f'获取铸造文件列表{new_files}')
        for file in new_files:
            try:
                c_id = self.upload_ipfs(file)
                self.make_json(file)
                self.insert_token_uri_to_db(file, c_id)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                log.error(f'初始化文件{file}失败，{e}')

    def get_today_plan_count(self, today=None):
        if today is None:
            today = self.today
        select_sql = f'SELECT count FROM plan WHERE plan_date = "{today}"'
        self.cursor.execute(select_sql)
        result = self.cursor.fetchone()
        return result

    @property
    def current_total_nft(self):
        url = 'https://explorer.straitchain.com/strait/home/totalInfo'
        resp = requests.post(url, headers=settings.headers)
        try:
            total_nft = int(resp.json()['data']['totalNft'])
            log.debug(f'获取当前数字藏品数={total_nft}')
            return total_nft
        except Exception as e:
            log.error(resp.text)
            raise e

    def calc_nft_count(self, current_total_nft, begin_date=datetime.date.today()):
        if current_total_nft >= self.target_count:
            return 0
        days_remaining = (self.end_date - begin_date).days
        if days_remaining >= 1:
            today_count = (self.target_count - current_total_nft) / days_remaining
            if 0 < today_count < 1000:
                today_count_thousand = 1
            else:
                today_count_thousand = round(today_count / 1000)
            default_offset = 8
            if today_count_thousand <= default_offset:
                offset = today_count_thousand - 1
            else:
                offset = default_offset
            count = today_count_thousand + random.randint(-offset, offset)
            return count * 1000
        else:
            return math.ceil((self.target_count - current_total_nft) / 1000) * 1000

    def plan_count(self):
        today = self.today
        count = self.get_today_plan_count(today)
        if count is None:
            current_total_nft = self.current_total_nft
            count = self.calc_nft_count(current_total_nft)
            sql = f'INSERT INTO plan (plan_date, count, created) VALUES ("{str(today)}", {count}, "{self.now}")'
            log.debug(f'创建当天计划 sql={sql}')
            self.commit_sql(sql)
        else:
            count = count[0]
        return count

    def get_valid_token_uri(self):
        sql = 'SELECT t.id, t.file_name FROM token_uri t WHERE id NOT IN (SELECT m.token_uri_id FROM mint_plan m) LIMIT 1'
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def make_plan(self, today=None):
        if today is None:
            today = self.today
        count = self.calc_nft_count(self.current_total_nft)
        sql = f'INSERT INTO plan (plan_date, count, created) VALUES ("{str(today)}", {count}, "{self.now}")'
        log.debug(f'创建当天计划 sql={sql}')
        self.commit_sql(sql)

        mint_count_pool = [i for i in self.mint_count_pool if count >= i]
        random_count_list = []
        while count > 0:

            random_count = random.choice(mint_count_pool)
            if random_count > count:
                random_count_list.append(count)
                break
            else:
                random_count_list.append(random_count)
                count -= random_count
        plan_id_sql = f'SELECT id FROM plan WHERE plan_date = "{today}"'
        self.cursor.execute(plan_id_sql)
        plan_id = self.cursor.fetchone()[0]
        random_planned_execute_time_list = [self.random_planned_execute_time(today).strftime('%Y-%m-%d %H:%M:%S') for _
                                            in random_count_list]
        random_planned_execute_time_list.sort()
        for c, t in zip(random_count_list, random_planned_execute_time_list):
            token_uri_detail = self.get_valid_token_uri()
            if token_uri_detail is None:
                raise Exception('token_uri为空，请及时补充')
            token_uri_id = token_uri_detail[0]
            nft_name = self.get_name_by_file(token_uri_detail[1])
            owner, private_key = self.random_account()
            insert_mint_plan_sql = 'INSERT INTO mint_plan ' \
                                   '(uuid, plan_id, token_uri_id, name, count, owner_address, private_key, planned_execute, created) ' \
                                   'VALUES ' \
                                   f'("{self.uid}", {int(plan_id)}, {int(token_uri_id)}, "{nft_name}", ' \
                                   f'{c}, "{owner}", "{private_key}", "{t}", "{self.now}")'
            log.debug(f'创建铸造计划 sql={insert_mint_plan_sql}')
            self.commit_sql(insert_mint_plan_sql)

    def check_plan_job(self):
        today = datetime.date.today()
        sql = f'SELECT id FROM plan WHERE plan_date = "{today}"'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is None:
            self.make_plan(today)

    def mint(self, mint_plan_id, copy_right='熵链科技（厦门）有限公司', issuer='熵链科技（厦门）有限公司',
             operator='熵链科技（厦门）有限公司', remark='', collect_sn=''):
        select_sql = f'SELECT  m.`name`, m.count, m.owner_address, m.planned_execute, t.c_id, t.json_url FROM mint_plan m INNER JOIN token_uri t ON m.token_uri_id = t.id WHERE m.id = {int(mint_plan_id)}'
        self.cursor.execute(select_sql)
        nft_name, count, owner, planned_execute, c_id, json_url = self.cursor.fetchone()

        contract_address = self.nft.deploy_contract(count, owner)
        update_contract_address_sql = f'UPDATE mint_plan SET contract_address = "{contract_address}", executed = "{self.now}" WHERE id = "{mint_plan_id}"'
        log.info(f'更新contract_address sql={update_contract_address_sql}')
        self.commit_sql(update_contract_address_sql)
        mint_hash = self.nft.mint_data_insert(count, contract_address, nft_name, c_id, json_url, copy_right, issuer,
                                              operator, remark, collect_sn, owner)
        update_mint_hash_sql = f'UPDATE mint_plan SET mint_hash = "{mint_hash}", executed = "{self.now}", state = 1 WHERE id = "{mint_plan_id}"'
        log.info(f'更新mint_hash sql={update_mint_hash_sql}')
        self.commit_sql(update_mint_hash_sql)

    def mint_job(self):
        """铸造任务"""
        select_sql = 'SELECT id, planned_execute FROM mint_plan WHERE state = 0'
        self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        log.debug(f'待铸造计划 {result}')
        if result is None:
            return []
        for plan in result:
            mint_plan_id, planned_execute = plan
            if planned_execute < datetime.datetime.now():
                log.info(f'执行铸造计划id={mint_plan_id}')
                self.mint(int(mint_plan_id))

    def __del__(self):
        self.cid_cache_file.close()
        self.mint_cache_file.close()
        try:
            self.db.close()
        except Exception:
            ...


def check_plan_job():
    log.info('执行创建计划任务')
    million = Million()
    million.check_plan_job()


def mint_job():
    log.info('执行扫描铸造任务')
    million = Million()
    million.mint_job()


def init_file_job():
    log.info('执行初始化铸造文件任务')
    million = Million()
    million.init_mint_file()


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(init_file_job, 'interval', hours=1, start_date='2022-05-11 00:00:00')
    scheduler.add_job(check_plan_job, 'interval', hours=1, start_date='2022-05-11 00:30:00')
    scheduler.add_job(mint_job, 'interval', seconds=2222)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
