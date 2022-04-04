#encoding=utf-8
import datetime
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from comm.log import logger
from dao.dao import proxy_table_manager
from dao.proxy import VALID_SUCCESS, VALID_FAILED, NEED_VALID_SPEED


class VerifySpeed:
    def __init__(self):
        self.t = threading.Thread(target=self.run)
        self.t.setDaemon(True)
        self.t.run()

    def run(self):
        while True:
            scopes = proxy_table_manager.get_all_scope()
            for scope in scopes:
                self.get_proxy_to_verify(scope, VALID_SUCCESS)
                self.get_proxy_to_verify(scope, NEED_VALID_SPEED)

    def get_proxy_to_verify(self, scope, status):
        update_time = None
        if status == VALID_SUCCESS:
            update_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
        cnt = proxy_table_manager.get_proxy_count(scope, status=status, update_time=update_time)
        if cnt > 0:
            page_size = 20
            for i in range(cnt)[::page_size]:
                proxies = proxy_table_manager.get_proxy(scope, status=status, update_time=update_time,
                                                        off=i, page_size=page_size)
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = {executor.submit(self.verify_speed, scope, p): p for p in proxies}
                    result = list(map(lambda x: x.result(), as_completed(futures)))
                    scopes = proxy_table_manager.get_all_scope()
                    for proxy, status, message in result:
                        list(map(lambda x: proxy_table_manager.update_status(x,
                                                                             proxy=proxy, message=message,
                                                                             status=status), scopes))

    def verify_speed(self, scope, proxy):
        url = f'https://{scope}'
        p = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        time_use = []
        message = '测速失败'
        for i in range(10):
            try:
                start = time.time()
                requests.get(url, proxies=p, timeout=3)
                time_use.append(time.time() - start)
                logger.error(f'scope {scope}, 代理测速成功： {time_use}')
            except BaseException as e:
                logger.error(f'scope {scope}, 代理测速失败: {e}')
                message = f'代理测速失败: {e}'
            time.sleep(0.05)

        if len(time_use) == 0:
            time_use = ''
            status, message = VALID_FAILED, message
        else:
            time_use = str(sum(time_use) / len(time_use))
            status, message = VALID_SUCCESS, '验证成功'
        return scope, status, message, time_use


verify_speed = VerifySpeed()
