#encoding=utf-8
import threading
import time

from comm.log import logger
from dao.proxy import NEED_VALID, NEED_VALID_SPEED, VALID_FAILED
from dao.dao import proxy_table_manager
import socket
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class VerifyAnoymous:
    def __init__(self):
        self.t = threading.Thread(target=self.run)
        self.t.setDaemon(True)
        self.t.run()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        self.ip = s.getsockname()[0]

    def run(self):
        logger.info(f'启动校验高匿线程')
        while True:
            scopes = proxy_table_manager.get_all_scope()
            proxies = proxy_table_manager.get_proxy_count(scopes[0], status=NEED_VALID)
            if len(proxies) > 0:
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = {executor.submit(self.verfiy, p): p for p in proxies}
                    result = list(map(lambda x: x.result(), as_completed(futures)))
                    scopes = proxy_table_manager.get_all_scope()
                    for proxy, status, message in result:
                        list(map(lambda x: proxy_table_manager.update_status(x,
                            proxy=proxy, message=message, status=status), scopes))
            time.sleep(30)

    # 校验代理高匿
    def verfiy(self, proxy):
        p = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        status = VALID_FAILED
        try:
            r = requests.get(f'http://{self.ip}/verify/anonymous', proxies=p, timeout=5)
            r = r.json()
            if r.get('is_anonymous', False):
                logger.info(f'代理{proxy}是高匿')
                status, message = NEED_VALID_SPEED, '待验证速度'
            else:
                logger.info(f'代理{proxy}不是高匿')
                message = f'代理{proxy}不是高匿'
        except BaseException as e:
            logger.error(f'验证代理{proxy}高匿性失败: {e}')
            message = f'验证代理{proxy}高匿性失败: {e}'

        return proxy, status, message


verify_anoymous = VerifyAnoymous()
