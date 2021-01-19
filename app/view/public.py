from flask import send_from_directory, current_app
from . import bp


@bp.route('/image/<path:filename>', methods=['GET'])
def get_image(filename):
    """ 获得图片 """
    _file = send_from_directory('../upload/', filename)
    return _file


# @bp.route('/image/app', methods=['GET'])
# def get_app():
#     return current_app.root_path
