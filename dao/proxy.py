#encoding=utf-8
import os

from peewee import *
import re
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


'''
 create table if not exists proxies(
    scope varchar(50) not null default '' comment '所属域',
    proxy varchar(50) not null default '' comment '代理地址: ip:port格式',
    status int(10) not null default 0 comment '状态： 0：待验证、1：成功、2、失败',
    time_use varchar(50) not null defualt '' comment '耗时，单位秒',
    update_time  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
 )
'''
path = os.path.join('./proxy.db')
db = SqliteDatabase(path)
db.connect()


# 代理表
class BaseModel(Model):
    # proxy = CharField()         # 代理地址: ip:port格式
    # status = IntegerField()     # 状态： 0：待验证、1：成功、2、失败
    # message = CharField()
    # suc_cnt = IntegerField(default=0)        # 成功的次数
    # fail_cnt = IntegerField(default=0)  # 失败的次数
    # time_use = CharField(default="")       # 耗时，单位秒
    # update_time = TimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    # create_tIme = TimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = db
        # primary_key = CompositeKey('proxy')


class MetaInfo:
    def __init__(self):
        self.proxy = None
        self.status = None
        self.message = None
        self.suc_cnt = None
        self.fail_cnt = None
        self.time_use = None
        self.update_time = None
        self.create_time = None
        self.table = None


NEED_VALID = 0
NEED_VALID_SPEED = 1
VALID_SUCCESS = 2
VALID_FAILED = 3
