FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip \
    && pip install poetry==1.8.3

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && poetry cache clear . --all

RUN groupadd -r appuser && useradd -r -g appuser appuser

RUN chown -R appuser:appuser /app

COPY . /app

USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
