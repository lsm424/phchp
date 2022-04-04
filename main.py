from flask import Flask
from blueprint.scope import scope_blue
from blueprint.verify import verify_blue
from dao.dao import proxy_table_manager
from proxy_producers.producer import proxy_producer
from proxy_verify.verify_speed import verify_speed
from proxy_verify.verify_anonymous import verify_anoymous

app = Flask(__name__)


@app.route('/ping')
def pint():
    return 'pong'


app.register_blueprint(verify_blue)
app.register_blueprint(scope_blue)


if __name__ == '__main__':
    app.run(port=5678)