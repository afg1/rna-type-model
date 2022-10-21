from python:3.9-bullseye

run apt install -y g++
run curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -y
copy . /rna_type_model

run pip install polars pandas scikit-learn obonet click numpy snorkel





