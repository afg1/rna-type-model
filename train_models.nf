nextflow.enable.dsl = 2

include { fetch_data; group_data; preprocess_data} from './workflow/preprocessing.nf'
include { run_heuristic_labeller; train_label_model; split_4_labelling; merge_heuristic_labels} from './workflow/heuristic_model_training.nf'






workflow {
    Channel.fromPath('./rna_type/preparation/query.sql') \
    | fetch_data \
    | group_data \
    | preprocess_data \
    | set { data }

   data.train | split_4_labelling | run_heuristic_labeller | merge_heuristic_labels | train_label_model | set { label_model }

}
