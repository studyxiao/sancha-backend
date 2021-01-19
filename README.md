# Flask 快速开发模板

Flask + MySQL + Redis + Celery + gunicorn

使用 docker 将多个 app 组合起来，方便项目开发。

第三方库：
查看 `requirements` 文件夹

wsgi.py 为入口文件

# 使用

## 安装

```bash
git clone git@gitee.com:studyxiao/flax.git project_name
```

## 配置

1. 在 `requirements` 中填写依赖。

2. 设置根目录下 `.env` 文件中变量（`.env.example` 为示例文件），重新设置 `app/config.py`。

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

## TODO

- 上传文件位置
  自动生成文件夹，
  命名规范
  upload 文件夹位置上传和获取不在同一位置 bug

前端 url 规范，统一设置位置
