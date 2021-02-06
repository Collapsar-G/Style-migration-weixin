import requests
import simplejson
import base64
import numpy as np
import cv2


# 首先将图片读入
# 由于要发送json，所以需要对byte进行str解码
def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str


if __name__ == '__main__':
    path = './input/content/test6.jpg'
    img_str = getByte(path)
    alpha = 1.0
    # print(img_str)
    # url = 'http://39.105.76.87:3268/style_qlssh_no/'
    # url = 'http://xcx.collapsar.online/style_qlssh_is/'
    url = 'http://localhost:3268/style_qjssh_is/'
    data = {'comment_img': img_str,'alpha': alpha}
    json_mod = simplejson.dumps(data)
    res = requests.post(url=url, data=json_mod)
    # print(res.text)
    data_json = simplejson.loads(res.text)
    print(data_json)
    # 把区获取到的数据转为JSON格式。

    img_str = data_json[0]['alpha' + str(alpha)]
    img_decode_ = img_str.encode('ascii')  # ascii编码
    img_decode = base64.b64decode(img_decode_)  # base64解码
    img_np = np.frombuffer(img_decode, np.uint8)  # 从byte数据读取为np.array形式
    img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)  # 转为OpenCV形式
    cv2.imshow(str(alpha), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
