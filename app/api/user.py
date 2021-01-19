from flask import jsonify, current_app, request
from flask_jwt_extended import get_current_user, verify_fresh_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from haw.exception import NotFound, Success, ParameterException
from haw.exception import RefreshException
from haw import manager
from haw.utils import generate_token, load_token, random_filename
from haw.task import send_valid_mail, send_forget_pwd_mail
from haw.auth import get_tokens, login_required
from haw.file import Uploader

from . import bp
from app.validator.user import NewUser, ForgetPassword, LoginForm
from app.validator.user import ResetPassword, ChangePassword, UpdateUser
from app.validator.public import Image


@bp.route('/user/<int:id>', methods=['GET'])
def get_user_info(id):
    """ 获得用户信息 """
    user = manager.user_model.get(id=id)
    if user is None:
        raise NotFound(msg='用户不存在')
    return jsonify(user)


@bp.route('/user/register', methods=['POST'])
def register():
    """ 用户注册 """
    return NotFound(msg='暂时不支持注册')
    form = NewUser().validate_for_api()
    form.data['avatar'] = 'upload/default/avatar.png'
    user = manager.user_model.create(**form.data)
    token = generate_token({'id': user.id})
    send_valid_mail(form.email.data, token, form.name.data)
    return Success(msg='创建成功，请前往邮箱激活账户')


@bp.route('user/valid/<token>', methods=['GET'])
def valid_user(token):
    """ 验证邮箱，激活账户 """
    is_valid = manager.user_model.confirm(token)
    if is_valid:
        return Success(msg='激活成功')
    return ParameterException(msg='链接已失效')


@bp.route('user/resend-mail', methods=['POST'])
def resend_mail():
    """ 重新发送激活链接 """
    form = ForgetPassword().validate_for_api()
    one = manager.user_model.get(email=form.email.data)
    if not one:
        raise ParameterException(msg='邮箱不正确')
    if one.is_valid:
        raise ParameterException(msg='邮箱已激活，勿重复操作')
    token = generate_token({'id': one.id})
    send_valid_mail(one.email, token, one.name)
    return Success(msg='已重新发送激活链接，一小时内有效')


@bp.route('user/login', methods=['POST'])
def login():
    """ 登录，配置中默认2小时后失效 """
    form = LoginForm().validate_for_api()
    user = manager.user_model.verify(form.email.data, form.password.data)
    if not user.is_valid:
        raise ParameterException(msg='请激活邮箱后登录')
    access_token, refresh_token = get_tokens(user)
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })


@bp.route('user/access', methods=['GET'])
@login_required
def get_access():
    current_user = get_current_user()
    if current_user.is_admin:
        # TODO 权限判断
        return jsonify({'access': ['article']})
    return jsonify({'access': []})


@bp.route('user/info', methods=['GET'])
@login_required
def get_information():
    """ 获得自己的信息 """
    current_user = get_current_user()
    if current_user.is_admin:
        current_user.add_fields(access=['article'])
    else:
        # TODO
        current_user.add_fields(access=[])
    return jsonify(current_user)


@bp.route('user/forget', methods=['POST'])
def forget_password_request():
    """ 发送重置密码链接邮箱 """
    form = ForgetPassword().validate_for_api()
    one = manager.user_model.get(email=form.email.data)
    if not one:
        raise NotFound(msg='用户不存在')
    token = one.generate_token()
    send_forget_pwd_mail(
        one.email,
        token,
    )
    return Success(msg='邮件已发送，注意查收')


@bp.route('user/reset/<token>', methods=['POST'])
def forget_password(token):
    """ 重置密码 """
    form = ResetPassword().validate_for_api()
    data = load_token(token)
    if data is None:
        return ParameterException(msg='token 失效')
    user = manager.user_model.get(id=data.get('id'))
    if not user:
        return NotFound(msg='用户不存在')
    user.reset_password(form.password.data)
    return Success(msg='密码重置成功')


@bp.route('user/change-pwd', methods=['POST'])
@login_required
def change_password():
    """ 修改密码 """
    form = ChangePassword().validate_for_api()
    current_user = get_current_user()
    current_user.change_password(form.old_password.data,
                                 form.new_password.data)
    return Success(msg='修改密码成功')


@bp.route('user/<int:uid>', methods=['GET'])
def get_other_info(uid):
    """ 获得某个用户信息 """
    one = manager.user_model.get(id=uid)
    if not one:
        raise ParameterException(msg='用户不存在')
    if not one.is_valid:
        raise ParameterException(msg='用户未激活')
    return jsonify(one)


@bp.route('/user/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    """ 修改个人信息，不包括头像和背景图 """
    current_user = get_current_user()
    if id != current_user.id:
        raise ParameterException(msg='只能修改自己的信息')
    form = UpdateUser().validate_for_api()
    user = manager.user_model.get(id=id)
    if user is None:
        raise NotFound(msg='用户不存在')
    user = user.update(user.id, **form.data)
    return jsonify(user)


@bp.route('/user/avatar/<int:id>', methods=['PUT'])
@login_required
def update_user_avatar(id):
    """ 修改用户头像 """
    current_user = get_current_user()
    if id != current_user.id:
        raise ParameterException(msg='只能修改自己的头像')
    form = Image().validate_for_api()
    uploader = Uploader(form.image.data)
    res = uploader.upload()
    current_user.set_avatar(res[0]['url'])
    return jsonify(res)


@bp.route('/user/bg/<int:id>', methods=['PUT'])
@login_required
def update_user_bg(id):
    current_user = get_current_user()
    if id != current_user.id:
        raise ParameterException(msg='只能修改自己的主页背景')
    files = request.files
    uploader = Uploader(files)
    res = uploader.upload()
    current_user.set_bg(res[0]['url'])
    return jsonify(res)


@bp.route('/user/refresh')
def get_refresh_token():
    """ 重新获得 token """
    try:
        verify_fresh_jwt_in_request()
    except Exception:
        raise RefreshException()
    identity = get_jwt_identity()
    if not identity:
        return NotFound(msg='refresh_token不正确')
    access_token, refresh_token = get_tokens(identity)
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })
