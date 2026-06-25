FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.sh

# Запускаем через entrypoint
CMD ["./entrypoint.sh"]
