FROM python:3.10-slim

run apt update && apt upgrade -y && apt install -y g++ postgresql-client curl
copy . /rna_type_model

WORKDIR /rna_type_model

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY poetry.lock $RNACENTRAL_IMPORT_PIPELINE/poetry.lock
COPY pyproject.toml $RNACENTRAL_IMPORT_PIPELINE/pyproject.toml
RUN PATH="$PATH:/root/.local/bin" poetry config virtualenvs.create false
RUN PATH="$PATH:/root/.local/bin" poetry install
