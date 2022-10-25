from python:3.9-bullseye

run run apt update && apt upgrade -y && apt install -y g++ postgresql-client
run curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
copy . /rna_type_model

run pip install polars pandas scikit-learn obonet click numpy snorkel

## Install scripts in path and make executable
## These should cover the preparation and preprocessing
run ln -s /rna_type_model/preparation/convert_data.py /usr/bin/convert_data && chmod +x /rna_type_model/preparation/convert_data.py
run ln -s /rna_type_model/preprocessing/group_data.py /usr/bin/group_data && chmod +x /rna_type_model/preprocessing/group_data.py
run ln -s /rna_type_model/preprocessing/load_and_split_data.py /usr/bin/load_and_split_data && chmod +x /rna_type_model/preprocessing/load_and_split_data.py

run ln -s /rna_type_model/heuristic/run_heuristic_labeller.py /usr/bin/run_heuristic_labeller && chmod +x /rna_type_model/heuristic/run_heuristic_labeller.py
run ln -s /rna_type_model/heuristic/train_heuristic_label_model.py /usr/bin/train_heuristic_label_model && chmod +x /rna_type_model/heuristic/train_heuristic_label_model.py
