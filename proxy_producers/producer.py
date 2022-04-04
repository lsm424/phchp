#encoding=utf-8
import threading
import os
import time

from comm.log import logger
from dao.dao import proxy_table_manager


# 代理生产者
class ProxyProducer:
    def __init__(self):
        self.t = []
        producers = list(filter(lambda x: x.ends('_proxy.py') and x not in self.proxies_producers_name,
                                os.listdir()))
        for i in producers:
            t = threading.Thread(target=self.get_proxies, args=(i,))
            t.setDaemon(True)
            t.run()
            self.t.append(t)

    def get_proxies(self, name):
        logger.info(f'启动代理抓取{name}')
        get_proxy_func = __import__(name + '.get_proxy')
        while True:
            scopes = proxy_table_manager.get_all_scope()
            proxies = []
            for proxy in get_proxy_func():
                proxies.append(proxy)
                if len(proxies) > 10:
                    logger.info(f'代理{name}注入ip port：{len(proxies)}个')
                    list(map(lambda x: proxy_table_manager.add_need_valid_proxies(x, proxies), scopes))
                    proxies.clear()
            else:
                if len(proxies) > 0:
                    logger.info(f'代理{name}注入ip port：{len(proxies)}个')
                    list(map(lambda x: proxy_table_manager.add_need_valid_proxies(x, proxies), scopes))

            time.sleep(30)


proxy_producer = ProxyProducer()