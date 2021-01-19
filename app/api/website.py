from flask import jsonify

from haw.auth import user_logined
from haw.exception import ParameterException, NotFound, Success
from haw.request import RequestParser

from . import bp
from app.validator.website import CreateTheme, CreateCate, CreateWebsite
from app.validator.website import UpdateTheme, UpdateCate, UpdateWebsite
from app.validator.website import CreateCateWebsite, UpdateCateWebsite
# from app.model.website import Theme, Cate, CateWebsite, Website
from app.model.website import Theme, Cate, CateWebsite, Website


@bp.route('website/theme', methods=['GET'])
def get_themes():
    """ 获得所有主题，未分页 """
    parser = RequestParser(Theme)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    themes = Theme.find_by_page(query_fields, by_fields, start, count)
    return jsonify(themes)


@bp.route('website/theme', methods=['POST'])
def create_theme():
    form = CreateTheme().validate_for_api()
    Theme.create(**form.data)
    return Success(msg='创建成功')


@bp.route('website/theme/<int:id>', methods=['PUT'])
def update_theme(id):
    form = UpdateTheme().validate_for_api()
    Theme.update(id, **form.data)
    return Success(msg='修改成功')


@bp.route('website/theme/<int:id>', methods=['DELETE'])
def delete_theme(id):
    Theme.delete(id)
    return Success(msg='删除成功')


@bp.route('/website/cate', methods=['GET'])
def get_cate():
    parser = RequestParser(Cate)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    cates = Cate.find_by_page(query_fields, by_fields, start, count)
    return jsonify(cates)


@bp.route('/website/theme/<int:id>/cate', methods=['GET'])
def get_cate_by_theme_id(id):
    """ 主题下分类 """
    result = Cate.query.filter_by(theme_id=id).all()
    return jsonify(result)


@bp.route('website/cate', methods=['POST'])
def create_cate():
    form = CreateCate().validate_for_api()
    theme = Theme.get(id=form.theme_id.data)
    if not theme:
        raise ParameterException(msg='主题不存在')
    cate = Cate.get(theme_id=theme.id, name=form.name.data)
    if cate:
        raise ParameterException(msg='该分组下分类已经存在')
    Cate.create(**form.data)
    return Success(msg='创建成功')


@bp.route('/website/cate/<int:id>', methods=['PUT'])
def update_cate(id):
    form = UpdateCate().validate_for_api()
    exited = Cate.get(Cate.id != id,
                      name=form.name.data,
                      theme_id=form.theme_id.data)
    if exited:
        raise ParameterException(msg='目标主题下已经有此分类，修改失败')
    Cate.update(id, **form.data)
    return Success(msg='修改成功')


@bp.route('/website/cate/<int:id>', methods=['DELETE'])
def delete_cate(id):
    """ 删除分类及分类下的所有数据 """
    cate = Cate.get(id=id)
    if cate is None:
        return NotFound(msg='不存在，删除失败')
    items = CateWebsite.find(cate_id=id)
    for item in items:
        item._delete()
    cate._delete()
    return Success(msg='删除成功')


@bp.route('/website', methods=['GET'])
def get_websites():
    """ 获得所有网址 """
    themes = Theme.find(by=[Theme.sort, Theme.create_time])
    for theme in themes:
        cates = Cate.find(query=[Cate.theme_id == theme.id],
                          by=[Cate.sort, Cate.create_time])
        for cate in cates:
            websites = CateWebsite.find(
                query=[CateWebsite.cate_id == cate.id],
                by=[CateWebsite.sort, CateWebsite.create_time])
            cate.add_fields(websites=websites)
        theme.add_fields(cates=cates)
    return jsonify(themes)


@bp.route('cate/<int:id>/website', methods=['GET'])
def get_websites_by_cate(id):
    parser = RequestParser(CateWebsite)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    query_fields.append(CateWebsite.cate_id == id)
    by_fields = [CateWebsite.sort, CateWebsite.create_time] + by_fields
    cate_website = CateWebsite.find_by_page(query_fields, by_fields, start,
                                            count)
    return jsonify(cate_website)
    # result = CateWebsite.find(query=[CateWebsite.cate_id == id],
    #                           by=[CateWebsite.sort, CateWebsite.create_time])
    # return jsonify(result)


@bp.route('/website', methods=['POST'])
def create_website():
    """ 创建分类下网址
    1. 通过url判断是否已经存在
        存在，获得实例，不存在创建
    2. 分类是否存在
        不存在直接抛出异常
    3. 分类下是否有本网址
        有抛出异常
    4. 创建新的数据
     """
    form = CreateCateWebsite().validate_for_api()
    website = Website.get(url=form.url.data)
    if website is None:
        # 创建新的website数据
        website = Website.create(
            **{
                'name': form.name.data,
                'info': form.info.data,
                'url': form.url.data,
                'icon': form.icon.data,
                'tags': form.tags.data
            })
    cate = Cate.get(id=form.cate_id.data)
    if cate is None:
        raise ParameterException(msg='分类不存在')
    exited = CateWebsite.get(website_id=website.id, cate_id=cate.id)
    if exited:
        raise ParameterException(msg='已经存在')
    data = {
        'website_id': website.id,
        'cate_id': cate.id,
        'info': form.info.data or website.info,
        'sort': form.sort.data or 200,
    }
    CateWebsite.create(**data)
    return Success(msg='创建成功')


@bp.route('/website/<int:id>', methods=['PUT'])
def update_website(id):
    """ 修改 """
    form = UpdateCateWebsite().validate_for_api()
    cate_website = CateWebsite.get(id=id)
    if cate_website is None:
        raise NotFound(msg='不存在')
    if cate_website.cate_id != form.cate_id.data:
        # 查找是否有分类
        cate = Cate.get(id=form.cate_id.data)
        if cate is None:
            raise ParameterException(msg='分类不存在')
    website = Website.get(id=cate_website.website_id)
    if website is None:
        raise NotFound(msg='请重新创建，不要修改')
    new_website = {}
    if website.url != form.url.data:
        # 网址发生改变
        new_website['url'] = form.url.data
    if website.name != form.name.data:
        new_website['name'] = form.name.data
    if new_website:
        Website.update(website.id, **new_website)
    CateWebsite.update(cate_website.id, **form.data)
    return Success(msg='修改成功')


@bp.route('/website/<int:id>', methods=['DELETE'])
def delete_website(id):
    """ 删除分类下某网址 """
    cate_website = CateWebsite.get(id=id)
    if cate_website is None:
        raise NotFound(msg='不存在')
    CateWebsite.delete(cate_website.id)
    return Success(msg='删除成功')


@bp.route('/website/<int:id>/valid', methods=['POST'])
def set_website_valid(id):
    cate_website = CateWebsite.get(id=id)
    if cate_website is None:
        raise NotFound(msg='不存在')
    if cate_website.status == 0:
        raise ParameterException(msg='已经有效')
    CateWebsite.update(cate_website.id, status=0)  # 有效
    return Success(msg='网址设置为有效')


@bp.route('/website/<int:id>/invalid', methods=['POST'])
def set_website_invalid(id):
    cate_website = CateWebsite.get(id=id)
    if cate_website is None:
        raise NotFound(msg='不存在')
    if cate_website.status == 1:
        raise ParameterException(msg='已经失效')
    cate_website._update({'status': 1})  # 失效
    return Success(msg='网址设置为失效')


@bp.route('/website/<int:id>/favor', methods=['GET'])
def get_website_favor(id):
    """ 获得网址点赞数据 """
    website = CateWebsite.get(id=id)
    if website is None:
        raise NotFound(msg='网址不存在')
    like_num = website.like_num
    like_status = 0
    user = user_logined()
    if user:
        like_status = 1
    return {'id': website.id, 'like_num': like_num, 'like_status': like_status}


@bp.route('admin/web', methods=['GET'])
def get_admin_websites():
    """ 后台获得所有网址 """
    parser = RequestParser(Website)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    websites = Website.find_by_page(query_fields, by_fields, start, count)
    return jsonify(websites)


@bp.route('/admin/web', methods=['POST'])
def create_admin_website():
    """ 后台创建网址 """
    form = CreateWebsite().validate_for_api()
    Website.create(**form.data)
    return Success(msg='创建成功')


@bp.route('/admin/web/<int:id>', methods=['PUT'])
def update_admin_website(id):
    """ 后台修改网址 """
    form = UpdateWebsite().validate_for_api()
    Website.update(id, **form.data)
    return Success(msg='修改成功')


@bp.route('/admin/web/<int:id>', methods=['DELETE'])
def delete_admin_website(id):
    Website.delete(id)
    return Success(msg='删除成功')


@bp.route('admin/theme', methods=['GET'])
def get_admin_themes():
    """ 后台获得所有主题以及主题下的分类 """
    themes = Theme.find()
    for item in themes:
        item.add_fields(children=Cate.find(theme_id=item.id), expand=True)
    return jsonify(themes)
