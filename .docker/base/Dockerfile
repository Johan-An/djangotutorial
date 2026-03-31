# 基础镜像：Python 3.10
FROM python:3.10.20-slim-bookworm

# 维护者信息
LABEL maintainer="GaoZhao An <angaozhao@163.com>"
LABEL description="Django 基础运行环境（Python3.10 + uWSGI + 系统工具）"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
ENV VENV_PATH=/opt/venv

# 安装依赖 + Nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libssl-dev libpcre3-dev default-libmysqlclient-dev curl vim nginx \
    pkg-config procps && apt-get clean && rm -rf /var/lib/apt/lists/*

# 虚拟环境
RUN python -m venv $VENV_PATH
RUN $VENV_PATH/bin/pip install --upgrade pip uwsgi

# 创建uwsgi日志目录并赋予可写权限
RUN mkdir -p /var/log/uwsgi && chown -R www-data:www-data /var/log/uwsgi


# 覆盖 Nginx 配置
RUN rm -rf /etc/nginx/sites-enabled/default
COPY nginx/default.conf /etc/nginx/sites-enabled/default.conf

# 工作目录
WORKDIR /app

# 复制启动脚本
COPY start.sh /opt/start.sh
RUN chmod +x /opt/start.sh

# 入口
CMD ["/opt/start.sh"]
