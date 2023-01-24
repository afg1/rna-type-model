from continuumio/miniconda3:latest



run apt update && apt upgrade -y && apt install -y g++ postgresql-client
run curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
copy . /rna_type_model

WORKDIR /rna_type_model

RUN conda env update -f env.yaml
RUN pip install obonet
