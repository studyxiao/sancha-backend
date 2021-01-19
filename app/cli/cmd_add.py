import click

from flask import current_app
from flask.cli import with_appcontext

from haw import manager


@click.group()
def add():
    """ 向数据库添加初始数据 """
    pass


@add.command()
@with_appcontext
def admin_user():
    """ 创建超级管理员
    :return: 用户实例
    """
    app_config = current_app.config
    exist = manager.user_model.get(email=app_config['SUPER_ADMIN_EMAIL'])
    if exist:
        # 已经创建
        return None
    params = {
        'email': app_config['SUPER_ADMIN_EMAIL'],
        'name': app_config['SUPER_ADMIN_NAME'],
        'password': app_config['SUPER_ADMIN_PASSWORD'],
        'is_valid': True,
        'group_id': 0
    }

    return manager.user_model.create(**params)


@add.command()
@with_appcontext
def groups():
    """ 创建默认用户组 """
    names = ['管理员', '普通用户']
    for name in names:
        exist = manager.group_model.get(name=name)
        if exist:
            continue
        manager.group_model.create(name=name)
    return '创建成功'


@add.command()
@with_appcontext
def sources():
    """ 创建文章来源 """
    from app.model.article import Source
    names = ['原创', '转载', '翻译']
    for name in names:
        exist = Source.get(name=name)
        if exist:
            continue
        Source.create(name=name)
    return True


@add.command()
@with_appcontext
def categories():
    """ 创建文章分类 """
    from app.model.article import Category
    names = ['默认分类']
    for name in names:
        exist = Category.get(name=name)
        if exist:
            continue
        Category.create(name=name)


@add.command()
@click.pass_context
@with_appcontext
def all(ctx):
    """ 生成所有 """
    ctx.invoke(admin_user)
    ctx.invoke(groups)
    ctx.invoke(sources)
    ctx.invoke(categories)
    return None
