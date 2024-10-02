FROM python:3.12
WORKDIR /app
COPY . /app
RUN python pip_requirements.py
RUN pip install --no-cache-dir -r pip_requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
