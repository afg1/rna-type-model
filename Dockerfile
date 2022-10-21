from python:3.9-alpine

run apk add rust cargo
copy . /rna_type_model

run pip install polars pandas scikit-learn obonet click numpy snorkel





