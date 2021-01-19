from sqlalchemy import Column, String, Integer
from sqlalchemy import Text, SmallInteger

from haw.model import BaseModel
from haw.db import db
from haw.exception import NotFound, AuthFailed


class Source(BaseModel):
    """ 来源 """
    id = Column(Integer, primary_key=True)
    name = Column(String(64), comment='原创，转载，翻译')
    info = Column(String(200), comment='介绍')
    count = Column(Integer, default=0, comment='数量')

    @classmethod
    def get_all(cls):
        """ 获得所有来源信息
        return: [{'name': '原创', 'id': 0, 'count': 0}]
        """
        sources = cls.find(by=[cls.create_time])
        result = [{
            'id': item.id,
            'name': item.name,
            'count': item.count
        } for item in sources]
        return result


class Category(BaseModel):
    """ 分类 parent_id 保留字段 """
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, comment='分类名称')
    info = Column(String(255), comment='简介')
    order = Column(Integer, default=200, comment='排序')
    parent_id = Column(Integer, comment='父级目录')

    @classmethod
    def get_all(cls):
        """ 获得所有分类信息
        按照【order、create_time】进行排序
        """
        cates = cls.find(by=[cls.order, cls.create_time])
        return cates


class Tag(BaseModel):
    """ 标签 """
    id = Column(Integer, primary_key=True)
    name = Column(String(64), comment='标签名称')
    count = Column(Integer, default=0, comment='标签下文章数')


class Article(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='作者id')
    title = Column(String(255), nullable=False, comment='文章标题')
    content = Column(Text, comment='内容')
    content_html = Column(Text, comment='HTML格式内容')
    summary = Column(String(255), comment='摘要')
    cover = Column(String(255),
                   comment='头图',
                   default="upload/default/cover.png")
    cate_id = Column(Integer, comment='分类id')
    source_id = Column(Integer, comment='来源id')
    status = Column(SmallInteger, default=0, comment='超级管理员操作，0-正常，1-隐藏，2-推荐')
    publish = Column(SmallInteger,
                     default=0,
                     comment='可见度，0-对所有人可见，1-登录可见，2-仅作者可见')
    is_draft = Column(SmallInteger,
                      default=0,
                      comment='存为草稿？0-不是，1-是，草稿不会在前端出现，仅在我的草稿中可见')
    hits = Column(Integer, default=0, comment='点击数')
    tag_ids = Column(String(255), comment='标签id，多个使用,隔开，如："1, 2, 4"')

    @property
    def user(self):
        from haw.model import User
        user = User.get(id=self.user_id)
        return {'name': user.name, 'avatar': user.avatar}

    @property
    def cate(self):
        cate = Category.get(id=self.cate_id)
        return cate

    @property
    def source(self):
        source = Source.get(id=self.source_id)
        return source

    @classmethod
    def published(cls):
        """ 获得已发表文章
        排除：
        1. 拉黑（隐藏） status!=1
        2. 已删除       create_time != None（直接使用 filter_by()方法即可）
        3. 草稿         is_draft==False
        return: query
        """
        published_articles = cls.query.filter(
            cls.status != 1, cls.is_draft == False).filter_by()  # noqa
        return published_articles

    @classmethod
    def get_articles_with_protect(cls,
                                  uid,
                                  query_fields,
                                  by_fields,
                                  start=0,
                                  count=10):
        """ 获得包含受保护的所有文章，包括：登录可见、仅自己可见。
        query_fields: 查询条件数组
        by_fields: 排序条件数组 """
        query = cls.published().filter((cls.publish < 2)
                                       | (cls.user_id == uid))
        by_fields = [cls.status] + by_fields
        result = cls.find_by_page(query_fields, by_fields, start, count, query)
        return result

    @classmethod
    def get_articles_without_protect(cls,
                                     query_fields,
                                     by_fields,
                                     start=0,
                                     count=10):
        """ 仅获得未受保护文章 """
        query = cls.published().filter(cls.publish == 0)
        result = cls.find_by_page(query_fields, by_fields, start, count, query)
        return result

    @classmethod
    def get_detail_with_protect(cls, id, uid):
        """ 获得受保护文章详情 """
        article = cls.get(id=id)
        if article is None:
            raise NotFound(msg='文章不存在')
        if article.status == 1 or article.is_draft:
            raise NotFound(msg='文章不存在')
        if article.publish == 2 and article.user_id != uid:
            raise AuthFailed(msg='无权访问')
        return article

    @classmethod
    def get_detail_without_protect(cls, id):
        """ 获得未受保护的文章详情 """
        article = cls.get(id=id)
        if article.status == 1 or article.is_draft or article.publish != 0:
            raise NotFound(msg='文章不存在或无权访问')
        return article

    @classmethod
    def get_self_articles(cls,
                          uid,
                          query_fields,
                          by_fields,
                          start=0,
                          count=10):
        """ 获得自己的文章 """
        query = cls.published().filter(cls.user_id == uid)
        result = cls.find_by_page(query_fields, by_fields, start, count, query)
        return result

    @staticmethod
    def before_insert(mapper, connection, target):
        def _format(_html):
            return

        # 添加摘要
        if target.summary is None or target.summary.strip() == '':
            # summary 为空时，自动生成，截取内容的前200字符
            if target.content is not None:
                target.summary = target.content[:200]
        # 分类、标签等计数

    @staticmethod
    def on_change_content(target, value, oldvalue, initiator):
        # 添加摘要
        if target.summary is None or target.summary.strip() == '':
            # summary 为空时，自动生成，截取内容的前200字符
            if target.content is not None:
                target.summary = target.content[:200]
        # 分类、标签等计数


db.event.listen(Article, 'before_insert', Article.before_insert)
db.event.listen(Article.content, 'set', Article.on_change_content)
