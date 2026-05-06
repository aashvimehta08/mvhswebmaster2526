# Dockerfile for Chatbot
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

EXPOSE 5001

# Run the migrated Flask backend
CMD ["python", "chatbot/app.py"]