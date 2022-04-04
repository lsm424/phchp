#encoding=utf-8
import requests
import time
import re
# http://www.ip3366.net/free/?page=2

interval = 24 * 60 * 60
last_time = 0

def get_proxy():
    if time.time() - last_time < interval:
        return []

    url = 'http://www.ip3366.net/free/?page=5'
    r = requests.get(url)
    r = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>\s*<td>(\d+)</td>', r.text)
    proxies = list(map(lambda x: f'{x[0]}:{x[1]}', r))
    last_time = time.time()
    return proxies

