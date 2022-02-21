FROM python:3.10.2-slim

WORKDIR /app

COPY /api /app/api
COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9072"]
