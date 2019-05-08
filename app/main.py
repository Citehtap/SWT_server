# coding:utf-8
from utils import *
from flask import Flask, render_template, request,redirect, url_for, send_from_directory, make_response
import time
import json
import os
import xml.etree.cElementTree as ET

app = Flask(__name__)
UPLOAD_FOLDER = '../../data'
ALLOWED_EXTENSIONS = set(['json'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/download/<openid>')
def download(openid):
    filename = str(openid) + '.json'
    try:
        f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8')
        t = json.load(f)
        f.close()
        return str(t).replace("'", '"')
    except:
        return 'error'


@app.route('/upload/<openid>', methods=['POST', 'GET'])
def upload(openid=None):
    filename = str(openid) + '.json'
    if request.method == 'POST':
        f = request.files['file']
        # basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('upload', openid=openid))
    return render_template('upload.html', openid=openid)


@app.route("/weixin/", methods = ["GET", "POST"])
def weixin():
    cor, msg = verify_signature(request)
    if cor:
        openid = request.args.get('openid')
        xml = ET.fromstring(request.data)
        toUser = xml.find('ToUserName').text
        fromUser = xml.find('FromUserName').text
        msgType = xml.find("MsgType").text

        if msgType == 'text':
            text = 'url: 118.25.157.231/upload/' + str(openid)
            reply = '''<xml>
                                    <ToUserName><![CDATA[%s]]></ToUserName>
                                    <FromUserName><![CDATA[%s]]></FromUserName>
                                    <CreateTime>%s</CreateTime>
                                    <MsgType><![CDATA[text]]></MsgType>
                                    <Content><![CDATA[%s]]></Content>
                                    </xml>'''
            response = make_response(reply % (fromUser, toUser, str(int(time.time())), text))
            response.headers['content-type'] = 'application/xml'
            return response


    return 0
    # if request.method == "GET":  # 判断请求方式是GET请求
    #     cor, msg = verify_signature(request)
    #     return msg
    #
    # if request.method == "POST":
    #     cor, msg = verify_signature(request)
    #     if cor:
    #         openid = request.args.get('openid')
    #         print('openid={0}'.format(openid))
    #         print(request.get_data().decode())
    #         pass
    #         return msg
    #     else:
    #         return 'error'


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=80, debug=True)
