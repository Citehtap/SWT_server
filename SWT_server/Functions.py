from flask import Flask
from flask import request
from utils import *

app = Flask(__name__)


@app.route("/weixin/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        cor, msg = verify_signature(request)
        return msg

    if request.method == "POST":
        cor, msg = verify_signature(request)
        if cor:
            openid = request.args.get('openid')
            print('openid={0}'.format(openid))
            print(request.data)
            pass



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
