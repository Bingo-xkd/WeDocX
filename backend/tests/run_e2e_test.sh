#!/bin/bash
# 一键端到端测试脚本（适用于Linux/macOS，Windows请参考README手动执行各步骤）
# 需在项目根目录下运行

set -e

# 1. 激活conda环境
source ~/miniforge3/etc/profile.d/conda.sh || source ~/anaconda3/etc/profile.d/conda.sh
conda activate WeDocX

echo "[1/5] 启动 Redis 服务（请确保本地已安装并配置好Redis，或手动启动）"
echo "    Windows用户请手动启动Redis服务"

# 2. 启动Celery worker（后台）
echo "[2/5] 启动 Celery worker..."
cd backend
nohup celery -A app.celery_app.celery_app worker --loglevel=info > ../output/celery_worker.log 2>&1 &
CELERY_PID=$!
sleep 3

# 3. 启动FastAPI服务（后台）
echo "[3/5] 启动 FastAPI (Uvicorn) 服务..."
nohup uvicorn main:app --reload > ../output/uvicorn.log 2>&1 &
UVICORN_PID=$!
sleep 3

# 4. 执行端到端自动化测试
echo "[4/5] 执行端到端自动化测试..."
pytest backend/tests/test_e2e_process_url.py

# 5. 清理后台进程
echo "[5/5] 清理后台服务进程..."
kill $CELERY_PID $UVICORN_PID || true
cd ..

echo "端到端测试流程已完成。请检查终端输出和目标邮箱收件情况。" 