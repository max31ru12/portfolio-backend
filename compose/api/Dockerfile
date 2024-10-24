FROM python:3.12-slim

RUN pip install poetry

WORKDIR /portfolio

COPY poetry.lock ./
COPY pyproject.toml ./

RUN poetry install

COPY app ./app

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

EXPOSE 8000
