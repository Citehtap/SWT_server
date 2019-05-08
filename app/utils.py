import hashlib

access_token = '21_rQuKH0pAav_gA61g7_gPxtMe5q3l3OmSgtR5mHhTKQvehpqMXgaCkfL9abSXl7E2K6mj8LYsDgzIccm0reG6wc0xerCCoUCoMTcEhK1hMMx7FHvIsRPPd3fzhMmFVrQjiUd6w56WVEt7zKW2BTTeAEAHZZ'


def verify_signature(req):
    my_signature = req.args.get('signature')  # 获取携带的signature参数
    # print('signature:{0}'.format(my_signature))

    my_timestamp = req.args.get('timestamp')  # 获取携带的timestamp参数
    # print('timestamp:{0}'.format(my_timestamp))

    my_nonce = req.args.get('nonce')  # 获取携带的nonce参数
    # print('nonce:{0}'.format(my_nonce))

    my_echostr = req.args.get('echostr')  # 获取携带的echostr参数
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



