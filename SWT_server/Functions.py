from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


@app.route("/weixin/", methods = ["GET", "POST"])

def verify_signature(request):
    my_signature = request.args.get('signature')  # 获取携带的signature参数
    # print('signature:{0}'.format(my_signature))

    my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
    # print('timestamp:{0}'.format(my_timestamp))

    my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
    # print('nonce:{0}'.format(my_nonce))

    my_echostr = request.args.get('echostr')  # 获取携带的echostr参数
    # print('echostr:{0}'.format(my_echostr))

    token = 'wxswt'  # 一定要跟刚刚填写的token一致

    # 进行字典排序
    data = [token, my_timestamp, my_nonce]
    data.sort()

    # 拼接成字符串
    temp = ''.join(data)

    # 进行sha1加密
    mysignature = hashlib.sha1(temp.encode('utf8')).hexdigest()

    # 加密后的字符串可与signature对比，标识该请求来源于微信
    if my_signature == mysignature:
        return True, my_echostr
    else:
        return False, 'Unverified signature!'

def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        cor, msg = verify_signature(request)
        return msg

    if request.method == "POST":
        cor, msg = verify_signature(request)
        if cor:
            openid = request.args.get('openid')
            print('openid={0}'.format(openid))
            print(request.data['runes'][0])

            pass



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
