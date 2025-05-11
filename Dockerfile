FROM python:3.12-slim

WORKDIR /code
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/cache' \
    PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=5

RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir poetry==1.8.3

COPY pyproject.toml poetry.lock* /code/
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /code

CMD ["uvicorn", "app.asgi:app", "--host", "0.0.0.0", "--port", "8000"]
