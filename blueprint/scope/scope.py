#encoding=utf-8
from flask import request
from blueprint.scope import scope_blue
from dao.dao import proxy_table_manager
from dao.proxy import VALID_SUCCESS


# 添加scope
@scope_blue.route('/add_scope', methods=["POST"])
def add_scope():
    scopes = request.form.get('scopes')
    list(map(lambda x: proxy_table_manager.add_scope(x), scopes))


# 删除scope
@scope_blue.route('/delete_scope', methods=["POST"])
def delete_scope():
    scopes = request.form.get('scopes')
    list(map(lambda x: proxy_table_manager.delete_scope(x), scopes))


# 查询scope下的proxy
@scope_blue.route('/get_proxy', methods=["GET"])
def get_proxy():
    scope = request.args.get('scope', 'www.baidu.com')
    page_size = request.args.get('size', 10)
    off = request.args.get('off', 0)
    time_use = request.args.get('time_use', '0.5')
    all = proxy_table_manager.get_proxy_count(scope=scope, status=VALID_SUCCESS, time_use=time_use)
    proxies = proxy_table_manager.get_proxy(scope=scope, status=VALID_SUCCESS, off=off,
                                            page_size=page_size, time_use=time_use)
    return {'all': all, 'proxies': proxies}
