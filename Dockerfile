# Dockerfile for Chatbot
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chatbot/ ./chatbot/
COPY . .

EXPOSE 5001

CMD ["python", "chatbot/app.py"]