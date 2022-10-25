nextflow.enable.dsl = 2

include { fetch_data; group_data; preprocess_data} from './workflow/preprocessing.nf'
include { run_heuristic_labeller; train_label_model } from './workflow/heuristic_model_training.nf'






workflow {
    Channel.fromPath('./preparation/query.sql') \
    | fetch_data \
    | group_data \
    | preprocess_data \
    | set { data }

    data.train | run_heuristic_labeller | train_label_model | set { label_model }

}
