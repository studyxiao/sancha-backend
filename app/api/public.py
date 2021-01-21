""" 公用方法，但不一定是公开访问 """
from flask import request, jsonify, send_from_directory
from haw.captcha import Captcha
from haw.auth import login_required
from haw.uploader import Uploader

from . import bp


@bp.route('/public/captcha')
def get_captcha():
    """ 获得验证码，需要前端传入 sid """
    sid = request.args.get('sid')
    captcha = Captcha()
    img, code = captcha.get_code(sid=sid)
    return img


@bp.route('/image', methods=['POST'])
@login_required
def upload_img():
    """ 上传图片，需登录，获得图片用flask内置静态资源url：/upload/<path> """
    files = request.files
    uploader = Uploader(files)
    res = uploader.upload()
    return jsonify(res)
