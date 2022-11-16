from python:3.11-buster

run apt update && apt upgrade -y && apt install -y g++ postgresql-client
run curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
copy . /rna_type_model

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /rna_type_model
RUN PATH="$PATH:/root/.local/bin" poetry config virtualenvs.create false
RUN PATH="$PATH:/root/.local/bin" poetry install
