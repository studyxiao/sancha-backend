from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy import UniqueConstraint

from haw.model import BaseModel


class Website(BaseModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, comment='网站名称')
    info = Column(String(200), comment='介绍')
    url = Column(String(255), nullable=False, comment='网址')
    icon = Column(String(255), comment='图标', default='upload/default/icon.png')
    tags = Column(String(255), comment='标签，使用,隔开')


class Theme(BaseModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, comment='主题名称')
    info = Column(String(200), comment='介绍')
    icon = Column(String(255), comment='图标', default='upload/default/icon.png')
    sort = Column(SmallInteger, default=100, comment='排序')


class Cate(BaseModel):
    """ 文章下为分类命名为 Category """
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, comment='主题名称')
    info = Column(String(200), comment='介绍')
    icon = Column(String(255), comment='图标', default='upload/default/icon.png')
    sort = Column(SmallInteger, default=200, comment='排序')
    theme_id = Column(Integer, nullable=False, comment='主题ID')

    __table_args__ = (UniqueConstraint('name', 'theme_id'),
                      )  # 联合唯一，在主题下只能有唯一分类名，不同主题下可有相同分类名称


class CateWebsite(BaseModel):
    """ 分类下网址，每个分类下仅可有唯一网址，但不同分类下可以有相同网址，且网址引用的 Website 表中数据。 """
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, comment='网址ID')
    cate_id = Column(Integer, comment='分类ID')
    like_num = Column(Integer, default=0, comment='喜欢数')
    info = Column(String(200), comment='介绍')
    sort = Column(SmallInteger, default=200, comment='排序')
    status = Column(SmallInteger, default=0, comment='是否有效，0-有效，1-无效')
    __table_args__ = (UniqueConstraint('website_id', 'cate_id'), )

    @property
    def name(self):
        website = Website.get(id=self.website_id)
        if website:
            return website.name
        return ''

    @property
    def url(self):
        website = Website.get(id=self.website_id)
        if website:
            return website.url
        return ''

    @property
    def icon(self):
        website = Website.get(id=self.website_id)
        if website:
            return website.icon
        return ''
