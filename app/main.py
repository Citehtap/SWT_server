# coding:utf-8
from utils import *
from flask import Flask, render_template, request,redirect, url_for, send_from_directory, make_response
import time
import json
import os
import xml.etree.cElementTree as ET
from data.monster_dict import monsters_name_map as mmp

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
        upload_path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        f.save(upload_path)
        data = json.load(open(upload_path, 'r', encoding='utf-8'))
        f.close()

        target = dict()
        target['wizard_name'] = data['wizard_info']['wizard_name']
        target['wizard_id'] = data['wizard_info']['wizard_id']
        target['unit_list'] = data['unit_list']
        target['runes'] = data['runes']
        for rune in target['runes']:
            del rune['wizard_id']
            del rune['occupied_id']
            del rune['upgrade_limit']
            del rune['upgrade_curr']
            del rune['base_value']
            del rune['sell_value']
            eff = [0] * 13
            eff[rune['pri_eff'][0]] += rune['pri_eff'][1]
            eff[rune['prefix_eff'][0]] += rune['prefix_eff'][1]
            for ef in rune['sec_eff']:
                eff[ef[0]] += ef[1] + ef[3]
            rune['eff'] = eff
            del rune['pri_eff']
            del rune['prefix_eff']
            del rune['sec_eff']
            del rune['extra']


        for item in target['unit_list']:
            del item['island_id']
            del item['pos_x']
            del item['pos_y']
            del item['building_id']
            del item['experience']
            del item['exp_gained']
            del item['exp_gain_rate']
            del item['skills']
            try:
                item['monster_name'] = map[item['unit_master_id']]
            except:
                item['monster_name'] = 'UNKNOWN'

            combination = [0]*24
            runes_type = []
            for rune in item['runes']:
                del rune['wizard_id']
                del rune['occupied_id']
                del rune['upgrade_limit']
                del rune['upgrade_curr']
                del rune['base_value']
                del rune['sell_value']
                eff = [0] * 13
                eff[rune['pri_eff'][0]] += rune['pri_eff'][1]
                eff[rune['prefix_eff'][0]] += rune['prefix_eff'][1]
                for ef in rune['sec_eff']:
                    eff[ef[0]] += ef[1] + ef[3]
                rune['eff'] = eff
                del rune['pri_eff']
                del rune['prefix_eff']
                del rune['sec_eff']
                del rune['extra']
                combination[rune['set_id']] += 1
                runes_type.append(rune['set_id'])
                target['runes'].append(rune)
            item['combination'] = combination
            item['runes_type'] = runes_type

        # save json
        filename2 = str(openid) + '-c.json'
        upload_path2 = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        with open(upload_path2, 'w+', encoding='utf-8') as t:
            json.dump(target, t, ensure_ascii=False)
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
            text = 'url: http://118.25.157.231/upload/' + str(openid)
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
    app.run(host='0.0.0.0', port=5000, debug=True)
