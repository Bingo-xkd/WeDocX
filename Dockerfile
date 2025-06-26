# 基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 默认暴露端口
EXPOSE 8000

# 启动命令（可被docker-compose覆盖）
CMD ["uvicorn", "backend/main:app", "--host", "0.0.0.0", "--port", "8000"] 