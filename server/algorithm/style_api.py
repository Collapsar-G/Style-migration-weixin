import os
from PIL import Image
import time
import numpy as np
import cv2
from algorithm.test import using_model
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import cv2
import requests
import simplejson
import time
import base64
from flask import Blueprint, render_template

style = Blueprint('style', __name__)


# os.system("python test.py  --content  %s  --style %s --alpha %f"  % (content, style,alpha))
# def Style(content_path,style_path,alpha=1.0):
def Style_no(content, style, alpha):
    return using_model(content, style, alpha)


def Style_is(content, style, alpha, preserve_color):
    return using_model(content, style, alpha, preserve_color)


def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str


def tojson(index, result):
    return {
        'alpha' + index: str(result)
    }


@style.route('/style_qlssh_no/', methods=['post'])  # 青山绿水图不保留原色 接口
def style_glssh_no():
    if not request.data:  # 检测是否有数据
        return 'fail'
    data = request.data.decode('utf-8')
    # 获取到POST过来的数据，
    data_json = simplejson.loads(data)
    # 把区获取到的数据转为JSON格式。
    img_str = data_json['comment_img']
    alpha = data_json['alpha']
    img_decode_ = img_str.encode('ascii')  # ascii编码
    img_decode = base64.b64decode(img_decode_)  # base64解码
    img_np = np.frombuffer(img_decode, np.uint8)  # 从byte数据读取为np.array形式
    img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)  # 转为OpenCV形式
    a = time.time()
    # 显示图像
    path = 'algorithm/using/' + str(a) + '.jpg'
    cv2.imwrite(path, img)
    print(path)
    data = []

    result = Style_no(path, 'algorithm/input/style_in/qlssh.jpg', alpha=alpha)
    print(result)
    img_str = getByte(result)
    data.append(tojson(str(alpha), str(img_str)))

    return simplejson.dumps(data, ensure_ascii=False)


@style.route('/style_qlssh_is/', methods=['post'])  # 青山绿水图保留原色 接口
def style_glssh_is():
    if not request.data:  # 检测是否有数据
        return 'fail'
    data = request.data.decode('utf-8')
    # 获取到POST过来的数据，
    data_json = simplejson.loads(data)
    # 把区获取到的数据转为JSON格式。
    img_str = data_json['comment_img']
    alpha = data_json['alpha']
    img_decode_ = img_str.encode('ascii')  # ascii编码
    img_decode = base64.b64decode(img_decode_)  # base64解码
    img_np = np.frombuffer(img_decode, np.uint8)  # 从byte数据读取为np.array形式
    img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)  # 转为OpenCV形式
    a = time.time()
    # 显示图像
    path = 'algorithm/using/' + str(a) + '.jpg'
    cv2.imwrite(path, img)
    print(path)
    data = []
   
    result = Style_is(path, 'algorithm/input/style_in/qlssh.jpg', alpha, True)
    print(result)
    img_str = getByte(result)
    data.append(tojson(str(alpha), str(img_str)))

    return simplejson.dumps(data, ensure_ascii=False)


# 
# if __name__ == '__main__':
#     app.run(host='0.0.0.0',
#             port=3268,
#             debug=True)

if __name__ == '__main__':
    # content = './input/content/brad_pitt.jpg'
    content = 'C:/Users/20180/Desktop/golden_gate.jpg'
    times = time.time()

    style = 'C:/Users/20180/desktop/qjss.png'
    alpha = 1.0

    # img = cv2.imread(content)
    # img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
    # cv2.imwrite("./output/" + str(times) + '.jpg',img)
    # result = Style_("./output/" + str(times) + '.jpg', style, alpha)
    result = Style_(content, style, alpha)
    img_result = cv2.imread(str(result))
    cv2.imshow('image', img_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
