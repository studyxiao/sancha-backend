from wtforms import StringField, TextAreaField, BooleanField
from wtforms import SelectField as _SelectField
from wtforms.validators import DataRequired, Length, Optional
from haw.form import BaseForm
from haw.exception import ParameterException

from app.model.article import Source, Category


class SelectField(_SelectField):
    def __init__(self,
                 label=None,
                 validators=None,
                 coerce=str,
                 choices=None,
                 validate_choice=True,
                 model=None,
                 model_label_name=('id', 'name'),
                 **kwargs):
        """ 增加:
        model 参数，用于从数据表中动态获取 choiche;
        model_label_name 用于确定显示数值与名称的列名，如('id', 'name')
        """
        self.model = model
        self.model_label_name = model_label_name
        if self.model is not None:
            # 配置choice
            items = [(getattr(item, self.model_label_name[0]),
                      getattr(item, self.model_label_name[1]))
                     for item in self.model.query.filter_by().all()]
            choices = items
        super().__init__(label, validators, coerce, choices, validate_choice,
                         **kwargs)

    def iter_choice(self):
        if self.model is not None:
            # 配置choice
            items = [(getattr(item, self.model_label_name[0]),
                      getattr(item.name, self.model_label_name[1]))
                     for item in self.model.query.filter_by().all()]
            self.choices = items
        super().iter_choices()


class CreateArticle(BaseForm):
    """ 创建文章 """
    title = StringField(validators=[
        DataRequired(message='请输入文章标题'),
        Length(min=1, max=200, message='标题在1到200字符之间')
    ])
    content = TextAreaField(validators=[DataRequired(message='请输入内容')])
    summary = StringField()
    cover = StringField()
    publish = SelectField(choices=[(0, '对所有人可见'), (1, '登录可见'), (2, '仅自己可见')],
                          coerce=int)
    is_draft = BooleanField(default=False)

    cate_id = SelectField(coerce=int, model=Category)
    source_id = SelectField(coerce=int, model=Source)


class UpdateArticle(CreateArticle):
    pass


class CreateCate(BaseForm):
    name = StringField(validators=[
        DataRequired(message='请输入分类标题'),
        Length(min=1, max=200, message='标题在1到200字符之间')
    ])
    info = StringField(validators=[Optional()])

    def validate_name(self, field):
        cate = Category.get(name=field.data)
        if cate:
            raise ParameterException(msg='分类已存在')


class UpdateCate(CreateCate):
    def validate_name(self, field):
        pass


class CreateSource(BaseForm):
    name = StringField(validators=[
        DataRequired(message='请输入来源名称'),
        Length(min=1, max=200, message='名称在1到200字符之间')
    ])
    info = StringField(validators=[Optional()])

    def validate_name(self, field):
        cate = Source.get(name=field.data)
        if cate:
            raise ParameterException(msg='来源已存在')


class UpdateSource(CreateSource):
    def validate_name(self, field):
        pass
