from flask import jsonify

from haw.exception import NotFound, Success, ParameterException
from haw import manager
from haw.request import RequestParser
from haw.manager import get_ep_infos, route_meta, find_auth_module

from . import bp
from app.validator.admin import CreateGroup, UpdateGroup
from app.validator.user import NewUser
from app.validator.admin import UpdateUser


@bp.route('/admin/group', methods=['GET'])
@route_meta(auth='获得权限信息')
def get_admin_group():
    """ 获得用户组信息 """
    parser = RequestParser(manager.group_model)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    themes = manager.group_model.find_by_page(query_fields, by_fields, start,
                                              count)
    return jsonify(themes)


@bp.route('/admin/authority', methods=['GET'])
def get_authority():
    """ 获得所有权限 """
    infos = get_ep_infos()
    return jsonify(infos)


@bp.route('/groups', methods=['GET'])
def get_admin_groups():
    """ 查询说有用户组及其权限 """
    parser = RequestParser(manager.group_model)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    groups = manager.group_model.find_by_page(query_fields, by_fields, start,
                                              count)
    for group in groups['data']:
        auths = manager.auth_model.find(group_id=group.id)
        auths = [auth.auth for auth in auths]
        group.add_fields(auths=auths)
    return jsonify(groups)


@bp.route('/group/all', methods=['GET'])
def get_all_group():
    groups = manager.group_model.find()
    return jsonify(groups)


@bp.route('group/<int:gid>', methods=['GET'])
def get_group(gid):
    group = manager.group_model.get(id=gid)
    if group is None:
        raise NotFound(msg='分组不存在')
    auths = manager.auth_model.find(group_id=group.id)
    auths = [auth.auth for auth in auths]
    group.add_fields(auths=auths)
    return jsonify(group)


@bp.route('/group', methods=['POST'])
def create_group():
    """ 创建用户组 """
    form = CreateGroup().validate_for_api()
    group = manager.group_model.create(**form.data)
    for auth in form.auths.data:
        meta = find_auth_module(auth)
        if meta:
            manager.auth_model.create(auth=auth, group_id=group.id)
    return Success(msg='创建成功')


@bp.route('/group/<int:gid>', methods=['PUT'])
def update_group(gid):
    """ 修改用户组 """
    form = UpdateGroup().validate_for_api()
    manager.group_model.update(gid, **form.data)
    auths = manager.auth_model.find(group_id=gid)
    auths = [auth.auth for auth in auths]
    for auth in form.auths.data:
        if auth not in auths:
            meta = find_auth_module(auth)
            if meta:
                manager.auth_model.create(auth=auth, group_id=gid)
    return Success(msg='修改成功')


@bp.route('/group/<int:gid>', methods=['DELETE'])
def delete_group(gid):
    """ 删除用户组 """
    manager.group_model.delete(gid)
    auths = manager.auth_model.find(group_id=gid)
    for auth in auths:
        manager.auth_model.delete(auth.id)
    return Success(msg='删除成功')


@bp.route('/admin/users', methods=['GET'])
def get_admin_user():
    parser = RequestParser(manager.user_model)
    start, count = parser.paginate()
    query_fields, by_fields = parser.parse_query_fields()
    users = manager.user_model.find_by_page(query_fields, by_fields, start,
                                            count)
    for user in users['data']:
        group = manager.group_model.get(id=user.group_id)
        if group:
            user.add_fields(group={'id': group.id, 'name': group.name})
        else:
            user.add_fields(group={'id': 0, 'name': '超级管理员'})
    return jsonify(users)


@bp.route('/admin/user', methods=['POST'])
def create_user_by_admin():
    form = NewUser().validate_for_api()
    form.data['avatar'] = 'upload/default/avatar.png'
    {}.setdefault()
    user = manager.user_model.create(**form.data.setdefault('is_valid', True))
    return jsonify(user)


@bp.route('/admin/user/<int:id>', methods=['PUT'])
def update_user_by_admin(id):
    """ 修改用户信息，不包括头像和背景图 """
    form = UpdateUser().validate_for_api()
    user = manager.user_model.get(id=id)
    if user is None:
        raise NotFound(msg='用户不存在')
    same_name = manager.user_model.get(name=form.name.data)
    if same_name and same_name.id != user.id:
        raise ParameterException(msg='用户名已存在')
    user = user.update(user.id, **form.data)
    return jsonify(user)


@bp.route('/admin/user/<int:id>', methods=['DELETE'])
@route_meta(auth='删除文章')
def delete_user_by_admin(id):
    """ 删除用户接口 """
    user = manager.user_model.get(id=id)
    if user is None:
        raise NotFound(msg='用户不存在')
    manager.user_model.delete(user.id)
    return Success(msg='删除成功')
