FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock* /app/

RUN pip3 install --user --upgrade  poetry==1.8.3

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi  \
    && echo yes | python3 -m poetry cache clear . --all

RUN useradd -m appuser
USER appuser



COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]