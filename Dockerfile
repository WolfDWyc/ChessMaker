FROM python:3.11.8-slim-bullseye

RUN pip install poetry==1.4.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY chessmaker ./chessmaker
RUN touch README.md # our pyproject.toml requires a README.md file to exist

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "chessmaker.clients.pywebio_ui"]
