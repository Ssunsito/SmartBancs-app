FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer.py .
# El parámetro -u deshabilita el buffer de Python para ver los logs en vivo
CMD ["python", "-u", "consumer.py"]