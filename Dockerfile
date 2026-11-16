# 1. Берем официальный образ Python (как чистый лист)
FROM python:3.10-slim

# 2. Создаем рабочую папку внутри коробки
WORKDIR /app

# 3. Копируем файл с библиотеками и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь остальной код
COPY . .

# 5. Открываем порт 5000 (чтобы сайт был доступен)
EXPOSE 5000

# 6. Команда для запуска
CMD ["python", "app.py"]
