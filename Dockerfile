FROM python:3.9.13
WORKDIR /app
COPY . .
CMD ["python", "main.py"]