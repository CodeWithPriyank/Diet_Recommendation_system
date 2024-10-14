FROM python:3.10.8

RUN mkdir -p app/backend

COPY backend/requirements.txt app/backend/requirements.txt
COPY data/ app/data/
COPY backend app/backend/

WORKDIR /app/backend

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]