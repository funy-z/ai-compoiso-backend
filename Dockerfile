FROM python:3.12
WORKDIR /app
COPY . /app
# 安装依赖
RUN python -m venv .venv
RUN /app/.venv/bin/pip install --upgrade pip
RUN /app/.venv/bin/pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
