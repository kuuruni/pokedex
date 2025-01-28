FROM python:3.13.1-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./database ./database
COPY ./main.py .

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "main.py"]