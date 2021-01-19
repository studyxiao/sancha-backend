from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, EqualTo, Regexp
from wtforms.validators import NumberRange, Optional
from haw.form import BaseForm
from haw.exception import ParameterException
from haw import manager
from flask_jwt_extended import get_current_user


class NewUser(BaseForm):
    name = StringField(validators=[
        DataRequired(message='指定用户名'),
        Regexp(
            r'([A-Za-z0-9]{4,20})|([\u4e00-\u9fa5]{2,10})|([\u4e00-\u9fa5][\w\W]{2})',  # noqa
            message='只能是汉字 字母和数字')
    ])
    # email = StringField(
    #     validators=[DataRequired(message='请输入名称'),
    #                 Email(message='正确邮箱格式')])
    email = StringField(validators=[
        DataRequired(message='请输入名称'),
        Regexp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
               message='邮箱格式不正确')
    ])
    password = StringField(validators=[
        DataRequired(message='请输入密码'),
        length(min=6, max=20, message='密码长度必须在6-20字符之间')
    ])
    password2 = StringField(validators=[
        DataRequired(message='必须输入相同密码'),
        EqualTo('password', message='两次密码输入不一致')
    ])

    def validate_email(self, field):
        u = manager.user_model.get(email=field.data)
        if u:
            raise ParameterException(msg='邮箱已注册')

    def validate_name(self, field):
        u = manager.user_model.get(name=field.data)
        if u:
            raise ParameterException(msg='用户名已存在')


class ForgetPassword(BaseForm):
    email = StringField(validators=[
        DataRequired(message='输入邮箱'),
        Regexp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
               message='邮箱格式不正确')
    ])


class LoginForm(BaseForm):
    email = StringField(validators=[
        DataRequired(message='必须填写邮箱'),
        Regexp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
               message='邮箱格式不正确')
    ])
    password = StringField('密码', validators=[DataRequired(message='密码不可为空')])


class ResetPassword(BaseForm):
    password = StringField(validators=[
        DataRequired(message='必须输入密码'),
        length(6, 20, message='长度必须在6-20之间')
    ])
    password2 = StringField(validators=[
        DataRequired(message='必须输入确认密码'),
        EqualTo('password', message='两次输入不一致')
    ])


class ChangePassword(BaseForm):
    old_password = StringField(validators=[DataRequired(message='必须输入旧密码')])
    new_password = StringField(validators=[DataRequired(message='必须输入新密码')])
    new_password2 = StringField(validators=[
        DataRequired(message='必须输入确认新密码'),
        EqualTo('new_password', message='新密码两次不一致')
    ])


class UpdateUser(BaseForm):
    name = StringField()
    # 非必须
    info = StringField(validators=[Optional()])
    # birthday = StringField(validators=[Optional()])
    gender = IntegerField(
        validators=[NumberRange(min=0, max=2, message='性别选择错误')], default=0)
    location = StringField(validators=[Optional()])
    sign = StringField(validators=[Optional()])

    def validate_name(self, field):
        u = manager.user_model.get(name=field.data)

        if u and u.id != get_current_user().id:
            raise ParameterException(msg='用户名已存在')
