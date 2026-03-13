# 使用 Python 3.10 作为基础镜像
FROM python:3.10-alpine3.22

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 删除：RUN apt-get update && apt-get install -y --no-install-recommends \
# 删除：    gcc \
# 删除：    && rm -rf /var/lib/apt/lists/*

# 安装系统依赖（Alpine 使用 apk 包管理器）
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && apk add --no-cache libffi-dev

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 删除虚拟构建依赖（如果不需要运行时保留 gcc）
RUN apk del .build-deps

# 创建静态文件目录（如果 Vue 构建产物存在则会被覆盖）
RUN mkdir -p /app/static/dist

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]