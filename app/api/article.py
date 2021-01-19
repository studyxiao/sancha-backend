from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_current_user
from flask_jwt_extended import jwt_optional
from haw.request import RequestParser
from haw.auth import login_required, group_required
from haw import route_meta
from haw.exception import Success, NotFound, AuthFailed
from haw.exception import ParameterException
from haw.db import db

from . import bp
from app.model.article import Article, Category, Source
from app.validator.article import CreateArticle, UpdateArticle
from app.validator.article import UpdateCate, CreateCate
from app.validator.article import UpdateSource, CreateSource


@bp.route('/article')
@jwt_optional
def get_articles():
    """ 获得文章列表，根据传入条件即可获得不同结果 """
    # 如果登录会获得用户，
    current_user = get_jwt_identity()
    parser = RequestParser(Article)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    print(query_fields)
    print(by_fields)
    if by_fields == []:
        by_fields.append(Article.create_time.desc())
    if current_user:
        # 已登录
        articles = Article.get_articles_with_protect(current_user['uid'],
                                                     query_fields, by_fields,
                                                     start, count)
        return jsonify(articles)
    else:
        # 未登录
        articles = Article.get_articles_without_protect(
            query_fields, by_fields, start, count)
        return jsonify(articles)


@bp.route('/article/<int:id>', methods=['GET'])
@jwt_optional
def get_article_detail(id):
    user = get_jwt_identity()
    if user:
        # 登录用户
        article = Article.get_detail_with_protect(id, user['uid'])
        return jsonify(article)
    # 未登录
    article = Article.get_detail_without_protect(id)
    return jsonify(article)


@bp.route('/article/self', methods=['GET'])
@login_required
def get_self_articles():
    current_user = get_current_user()
    articles = Article.get_self_articles(current_user.id)
    return jsonify(articles)


@bp.route('/article', methods=['POST'])
@route_meta(auth='创建文章')
@group_required
def create_article():
    """ 创建文章，只有管理员和超级管理员可以写作 """
    # current_user = get_current_user()
    form = CreateArticle().validate_for_api()
    data = form.data
    data.update({'user_id': 1})
    # data = form.data.update({'user_id': current_user.id})
    Article.create(**data)
    # article = Article(**data)
    # db.session.add(article)
    return Success(msg='创建成功')


@bp.route('/article/<int:id>', methods=['PUT'])
@route_meta(auth='修改文章')
@group_required
def update_article(id):
    current_user = get_current_user()
    article = Article.published().get(id)
    if article is None:
        raise NotFound(msg='文章不存在')
    if article.user_id != current_user.id:
        raise AuthFailed('没有权限')
    form = UpdateArticle().validate_for_api()
    Article.update(article.id, **form.data)
    return Success(msg='修改成功')


@bp.route('/article/<int:id>', methods=['DELETE'])
@route_meta(auth='删除文章')
@group_required
def delete_article(id):
    """ 用户删除文章接口 """
    current_user = get_current_user()
    article = Article.get(id=id)
    if article is None:
        raise NotFound(msg='文章不存在')
    if article.user_id != current_user.id:
        raise AuthFailed(msg='没有权限')
    Article.delete(article.id)
    return Success(msg='删除成功')


@bp.route('/article/cate', methods=['GET'])
def get_article_cate():
    """ 获得文章分类信息 """
    cates = Category.get_all()
    return jsonify(cates)


@bp.route('article/source', methods=['GET'])
def get_article_source():
    """ 获得文章来源信息：目前是原创、转载、翻译 """
    sources = Source.get_all()
    return jsonify(sources)


@bp.route('/category', methods=['GET'])
def get_category():
    """ 获得分页分类 """
    parser = RequestParser(Category)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    cates = Category.find_by_page(query_fields, by_fields, start, count)
    return jsonify(cates)


@bp.route('/category', methods=['POST'])
@route_meta(auth='创建分类')
@group_required
def create_category():
    """ 创建分类，只有管理员和超级管理员可以写作 """
    # current_user = get_current_user()
    form = CreateCate().validate_for_api()
    # data = form.data.update({'user_id': current_user.id})
    Category.create(**form.data)
    return Success(msg='创建成功')


@bp.route('/category/<int:id>', methods=['PUT'])
@route_meta(auth='修改分类')
@group_required
def update_category(id):
    form = UpdateCate().validate_for_api()
    exit = Category.get(Category.id != id, name=form.name.data)
    if exit:
        raise ParameterException(msg='分类已存在')
    Category.update(id, **form.data)
    return Success(msg='修改成功')


@bp.route('/category/<int:id>', methods=['DELETE'])
@route_meta(auth='删除分类')
@group_required
def delete_category(id):
    # TODO 管理员权限
    Category.delete(id)
    return Success(msg='删除成功')


@bp.route('/source', methods=['GET'])
def get_source():
    """ 获得分页来源 """
    parser = RequestParser(Source)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    sources = Source.find_by_page(query_fields, by_fields, start, count)
    return jsonify(sources)


@bp.route('/source', methods=['POST'])
@route_meta(auth='创建来源')
@group_required
def create_source():
    """ 创建分类，只有管理员和超级管理员可以写作 """
    # current_user = get_current_user()
    form = CreateSource().validate_for_api()
    # data = form.data.update({'user_id': current_user.id})
    Source.create(**form.data)
    return Success(msg='创建成功')


@bp.route('/source/<int:id>', methods=['PUT'])
@route_meta(auth='修改来源')
@group_required
def update_source(id):
    form = UpdateSource().validate_for_api()
    exit = Source.get(Source.id != id, name=form.name.data)
    if exit:
        raise ParameterException(msg='来源已存在')
    Source.update(id, **form.data)
    return Success(msg='修改成功')


@bp.route('/source/<int:id>', methods=['DELETE'])
@route_meta(auth='删除来源')
@group_required
def delete_source(id):
    # TODO 管理员权限
    Source.delete(id)
    return Success(msg='删除成功')
