from python:3.9-bullseye

run apt install -y rust cargo g++
copy . /rna_type_model

run pip install polars pandas scikit-learn obonet click numpy snorkel





