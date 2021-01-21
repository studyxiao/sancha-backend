from wtforms import StringField, IntegerField
from wtforms import FieldList
from wtforms.validators import DataRequired, Optional, NumberRange
from haw.form import BaseForm
from haw import manager


class CreateGroup(BaseForm):
    """ 管理员 """
    name = StringField(validators=[DataRequired(message='请输入分组名称')])
    info = StringField(validators=[Optional()])
    auths = FieldList(
        StringField(validators=[DataRequired(message='请输入auths字段')]))


class UpdateGroup(CreateGroup):
    pass


class DispatchAuths(BaseForm):
    group_id = IntegerField(validators=[
        DataRequired(message='请输入分组id'),
        NumberRange(message='分组id必须大于0', min=1)
    ])
    auths = FieldList(
        StringField(validators=[DataRequired(message='请输入auths字段')]))


class RemoveAuths(BaseForm):
    group_id = IntegerField(validators=[
        DataRequired(message='请输入分组id'),
        NumberRange(message='分组id必须大于0', min=1)
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

    # def validate_name(self, field):
    #     u = manager.user_model.get(name=field.data)
    #     print(dir(self))
    #     print(self.data)
    #     if u and u.id != get_current_user().id:
    #         raise ParameterException(msg='用户名已存在')
