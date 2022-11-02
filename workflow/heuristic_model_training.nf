process run_heuristic_labeller {
    input:
        path(parquet)

    output:
        path('*.gz')
        path(parquet)

    script:
    """
    rtype label heuristic $parquet $parquet.baseName
    """
}

process train_label_model {
    input:
        path(lf_labelled_data)
        path(parquet)

    output:
        path("label_model.joblib")

    """
    run_label_model_training $lf_labelled_data $parquet
    """
}


process split_4_labelling {
    input:
        path(train_data)

    output:
        path("chunks/*")

    script:
    """
    mkdir chunks
    rtype label split $train_data ./chunks --chunks=$params.labelling.chunks
    """
}

process merge_heuristic_labels {
    input:
        path(input_files)
        path(parquet)

    output:
        path("combined.npy.gz")
        path(parquet)

    script:
    """
    rtype label combine combined.npy.gz $input_files
    """
}
