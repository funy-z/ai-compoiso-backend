FROM python:3.12-slim
WORKDIR /app
COPY . /app
# 安装依赖
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt
EXPOSE 80
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python", "main.py"]
