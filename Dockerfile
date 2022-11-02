from python:3.9-bullseye

run apt update && apt upgrade -y && apt install -y g++ postgresql-client
run curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
copy . /rna_type_model

run pip install polars pandas scikit-learn obonet click numpy snorkel
