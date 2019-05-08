# coding:utf-8
from utils import *
from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = '../../data'
ALLOWED_EXTENSIONS = set(['json'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload/<openid>', methods=['POST', 'GET'])
def upload(openid=None):
    filename = str(openid) + '.json'
    if request.method == 'POST':
        f = request.files['file']
        # basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html', openid=openid)


@app.route("/weixin/", methods = ["GET", "POST"])
def weixin():
    if request.method == "GET":  # 判断请求方式是GET请求
        cor, msg = verify_signature(request)
        return msg

    if request.method == "POST":
        cor, msg = verify_signature(request)
        if cor:
            openid = request.args.get('openid')
            print('openid={0}'.format(openid))
            print(request.get_data().decode())
            pass
            return msg
        else:
            return 'error'


if __name__ == '__main__':
    app.run(debug=True)
