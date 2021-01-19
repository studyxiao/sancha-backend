from flask_wtf.file import FileField, FileAllowed, FileRequired
from haw.form import BaseForm


class Image(BaseForm):
    image = FileField(validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                    '格式不正确，只能上传 jpg jpeg png gif 格式图片')
    ])
