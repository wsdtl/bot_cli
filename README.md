# 项目指令备忘

## Django 创建项目

```sh
django-admin startproject 项目名 创建写入文件夹
```

## Django 创建应用

```sh
python manage.py startapp tests
```

## Django 数据库迁移

```sh
python manage.py makemigrations
python manage.py migrate
```

## Django 创建超级用户

```sh
python manage.py createsuperuser
```

## Django 迁移静态文件

```sh
python manage.py collectstatic
```

## 导出虚拟环境配置

```sh
pip list --format=freeze >requirement.txt
```
