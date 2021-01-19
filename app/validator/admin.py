from wtforms import StringField, IntegerField
from wtforms import FieldList
from wtforms.validators import DataRequired, Optional, NumberRange
from haw.form import BaseForm


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
