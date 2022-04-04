#encodingd=utf-8
import datetime
import re
from peewee import *
from dao.proxy import BaseModel, MetaInfo, NEED_VALID, VALID_SUCCESS, db


class ProxyDao:
    def __init__(self):
        self.scope = {}
        tables = list(filter(lambda x: x.endswith("_scope"), db.get_tables()))
        # 配置默认值
        if not tables:
            tables = ['www.baidu.com']
        list(map(lambda x: self.add_scope(x), tables))

    # 创建表
    def add_scope(self, scope):
        if not scope.endswith('_scope'):
            table_name = f'{self.__fix_scope_name(scope)}_scope'
        else:
            table_name = scope
        table = f'''
class {table_name}(BaseModel):
    proxy = CharField()         # 代理地址: ip:port格式
    status = IntegerField()     # 状态： 0：待验证、1：成功、2、失败
    message = CharField()
    suc_cnt = IntegerField(default=0)        # 成功的次数
    fail_cnt = IntegerField(default=0)  # 失败的次数
    time_use = CharField(default="")       # 耗时，单位秒
    update_time = TimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_time = TimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
'''
        exec(table)
        table = MetaInfo()
        table.table = eval(f'{table_name}()')
        table.update_time = eval(f"getattr({table_name}, 'update_time')")
        table.status = eval(f"getattr({table_name}, 'status')")
        table.proxy = eval(f"getattr({table_name}, 'proxy')")
        table.message = eval(f"getattr({table_name}, 'message')")
        table.suc_cnt = eval(f"getattr({table_name}, 'suc_cnt')")
        table.fail_cnt = eval(f"getattr({table_name}, 'fail_cnt')")
        table.time_use = eval(f"getattr({table_name}, 'time_use')")
        table.create_time = eval(f"getattr({table_name}, 'create_time')")
        if not table.table.table_exists():
            table.table.create_table()

        proxies = self.get_proxy('www.baidu.com', status=VALID_SUCCESS)
        self.add_need_valid_proxies(scope, proxies)
        self.scope[scope] = table

    # scope 名称到表名称
    def __fix_scope_name(self, name):
        return re.sub(r'[^a-zA-Z0-9]', '', name)

    def get_all_scope(self):
        return list(self.scope)

    # 插入一条待验证的代理
    def add_need_valid_proxy(self, scope, proxy):
        table = self.scope[scope]
        ret = table.table.select(table.proxy).where(table.proxy == proxy)
        if len(ret) == 0:
            table.create(scope=scope, proxy=proxy, status=NEED_VALID)

    # 批量插入待验证的代理
    def add_need_valid_proxies(self, scope, proxies: list):
        if len(proxies) == 0 or scope not in self.scope:
            return
        proxy_table = self.scope[scope]
        ret = proxy_table.table.select(proxy_table.proxy).\
            where(proxy_table.proxy.in_(proxies))
        proxies = set(proxies) - set(map(lambda x: x.proxy, ret))
        if len(proxies) > 0:
            data = list(map(lambda x: {'proxy': x, 'status': NEED_VALID, 'time_use': '', "message": '待验证'}, proxies))
            proxy_table.insert_many(data).execute()

    # 删除指定域名下的
    def delete_scope(self, scope):
        if scope in self.scope:
            db.drop_tables(self.__fix_scope_name(scope))
            self.scope.pop(scope)

    # 获得指定域名下的有效代理
    def get_proxy(self, scope=None, status=None,  time_use=None, limit=0, off=0, update_time=None):
        if not scope:
            scope = 'www.baidu..com'
        if scope not in self.scope:
            return []
        proxy_table = self.scope[scope]
        params = []
        ret = proxy_table.table.select(proxy_table.proxy)
        if limit:
            ret = ret.limit(limit)
        if off:
            ret = ret.offset(off)
        if status:
            params.append(proxy_table.status == status)
        if time_use:
            params.append(proxy_table.time_use <= time_use)
        if update_time:
            params.append(proxy_table.update_time <= update_time)
        ret = ret.where(*params).order_by(fn.Random())
        return list(map(lambda x: x.proxy, ret))

    # 统计
    def get_proxy_count(self, scope=None, status=None, time_use=None, update_time=None):
        if not scope:
            scope = 'www.baidu..com'
        if scope not in self.scope:
            return 0
        proxy_table = self.scope[scope]
        params = []
        ret = proxy_table.table.select()
        if status:
            params.append(proxy_table.status == status)
        if time_use:
            params.append(proxy_table.time_use <= time_use)
        if update_time:
            params.append(proxy_table.update_time <= update_time)
        ret = ret.where(*params).count()
        return ret

    # 更新状态
    def update_status(self, scope, status, message, proxy):
        if scope not in self.scope:
            return
        proxy_table = self.scope[scope]
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        proxy_table.table.update({proxy_table.status: status, proxy_table.message: message,
                            proxy_table.update_time: cur_time}).where(proxy_table.proxy == proxy).execute()


proxy_table_manager = ProxyDao()
