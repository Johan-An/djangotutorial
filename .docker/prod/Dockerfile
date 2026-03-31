FROM django-base:3.10

# 维护者信息
LABEL maintainer="GaoZhao An <angaozhao@163.com>"
LABEL description="Django 项目生产环境"

WORKDIR /app

USER root

COPY requirements.txt /app/requirements.txt
# 安装依赖
RUN $VENV_PATH/bin/pip install -r requirements.txt

COPY ./ /app/
COPY ./.env.prod /app/.env

# 静态文件收集
RUN $VENV_PATH/bin/python manage.py collectstatic --noinput

CMD ["/opt/start.sh"]