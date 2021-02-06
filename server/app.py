import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import cv2
import requests
import simplejson
import time
import base64
# from os_bash import Style_
from algorithm.style_api import style

app = Flask(__name__)
app.register_blueprint(style)


@app.route('/')
def hello_world():
    return '陈阳真帅啊！！！我好爱！！！' 


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=3268,
            debug=True)
