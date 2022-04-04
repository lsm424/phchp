#encoding=utf-8
from flask import request
from blueprint.verify import verify_blue
from comm.log import logger


# 判断是否高匿
@verify_blue.route('/anonymous')
def anonymous():
    via = request.headers.get('VIA', '')
    x_forward_for = request.headers.get('X_FORWARD_FOR', '')
    ret = True if not via and not x_forward_for else False
    logger.info(f'verify anonymous, via: {via}, x_forward_for: {x_forward_for}, result: {ret}')
    return {'is_anonymous': ret}
