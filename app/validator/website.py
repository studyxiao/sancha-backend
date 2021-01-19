from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length

from haw.form import BaseForm


class CreateWebsite(BaseForm):
    name = StringField(
        validators=[DataRequired(
            message='指定名称'), Length(max=100)])
    info = StringField(validators=[Length(max=200)])
    url = StringField(
        validators=[DataRequired(
            message='指定网址'), Length(max=255)])
    icon = StringField(validators=[Length(max=255)])
    tags = StringField(validators=[Length(max=255)])

    sort = IntegerField(default=200)


class UpdateWebsite(CreateWebsite):
    pass


class CreateCateWebsite(CreateWebsite):
    cate_id = IntegerField(validators=[DataRequired(message='指定分类')])


class UpdateCateWebsite(CreateCateWebsite):
    pass


class CreateTheme(BaseForm):
    name = StringField(
        validators=[DataRequired(
            message='指定名称'), Length(max=100)])
    info = StringField(validators=[Length(max=200)])
    icon = StringField(validators=[Length(max=255)])
    sort = IntegerField(default=200)


class UpdateTheme(CreateTheme):
    pass


class CreateCate(BaseForm):
    name = StringField(
        validators=[DataRequired(
            message='指定名称'), Length(max=100)])
    info = StringField(validators=[Length(max=200)])
    icon = StringField(validators=[Length(max=255)])
    theme_id = IntegerField(validators=[DataRequired(message='指定分类')])
    sort = IntegerField(default=200)


class UpdateCate(CreateCate):
    pass
