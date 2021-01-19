from sqlalchemy import Column, String, Integer, Boolean

from haw.model import BaseModel
from haw import manager


class Comment(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, comment='用户ID')
    content = Column(String(200), comment='评论内容')
    status = Column(Boolean, default=True, comment='是否显示')

    @property
    def user(self):
        user = manager.user_model.get(id=self.user_id)
        if user is None:
            return None
        return {'id': user.id, 'name': user.name, 'avatar': user.avatar}
