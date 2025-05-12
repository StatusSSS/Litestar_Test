FROM python:3.12-slim

WORKDIR /code


ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=5


RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


COPY . /code

CMD ["uvicorn", "app.asgi:app", "--host", "0.0.0.0", "--port", "8000"]