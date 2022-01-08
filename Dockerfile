FROM python:3.8.12

WORKDIR /code

 # ToDO: copy only necessary folders/files
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9072"]
