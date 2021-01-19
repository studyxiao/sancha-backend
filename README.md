# 三查导航服务端源码

## 技术栈

Flask + MySQL + Redis + Celery + gunicorn

使用 docker 将多个 app 组合起来，方便项目开发。

## 使用到的第三方库

查看 `requirements` 文件夹

## 项目说明

https://showdoc.studyxiao.cn/web/#/1?page_id=2

# 如何使用

wsgi.py 为入口文件

## 安装

```bash
git clone https://github.com/studyxiao/sancha-backend.git
```

## 配置

1. 设置根目录下 `.env` 文件中变量（`.env.example` 为示例文件），重新设置 `app/config.py`。

## 启动

```bash
docker-compose -f ./docker-compose.yml up -d

# 数据库更新
docker exec -it [container_name] /bin/bash
flask db init
flask db migrate
flask db upgrade
```

访问 `localhost:8000`

## 停止

```bash
docker-compose down
```

## 部署反向代理

参考 `docker/nginx` 下配置文件

# 未完成

- 测试
