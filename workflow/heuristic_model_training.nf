process run_heuristic_labeller {
    input:
        path(parquet)

    output:
        path('L_train.npy')
        path('L_test.npy')
        path(parquet)

    script:
    """
    run_heuristic_labeller $parquet
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
