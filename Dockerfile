from python:3.9-alpine

copy . /rna_type_model

run pip install polars pandas scikit-learn obonet click numpy snorkel





