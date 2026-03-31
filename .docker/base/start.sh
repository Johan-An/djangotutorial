#!/bin/bash
set -euo pipefail

# 注意 这里不执行数据库迁移，数据库迁移需要在容器启动后手动执行

. /opt/venv/bin/activate

pip install -r /app/requirements.txt

echo "== Starting uWSGI..."
exec /opt/venv/bin/uwsgi --ini /app/uwsgi.ini &

echo "Waiting for Nginx to start..."

echo "== Starting Nginx..."
nginx -g "daemon off;"