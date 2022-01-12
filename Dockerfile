FROM python:3.8.12

WORKDIR /app

 # ToDO: copy only necessary folders/files
COPY /api /app/api
COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9072"]
