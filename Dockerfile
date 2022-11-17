from python:3.11-bullseye

run apt update && apt install -y -V ca-certificates lsb-release wget
run wget https://apache.jfrog.io/artifactory/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
run apt install -y -V ./apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
run apt update && apt upgrade -y && apt install -y g++ postgresql-client cmake libarrow-dev
run curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
copy . /rna_type_model

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /rna_type_model
RUN PATH="$PATH:/root/.local/bin" poetry config virtualenvs.create false
RUN PATH="$PATH:/root/.local/bin" poetry install
