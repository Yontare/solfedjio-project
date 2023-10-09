FROM python:3.9-alpine

EXPOSE 8000

WORKDIR /code/src/solfedjio-project

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /code

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
