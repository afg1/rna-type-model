

process fetch_data
{
    input:
        path(data_fetch_query)

    output:
        path('complete_data.csv')

    script:
    """
    psql -f $data_fetch_query "$PGDATABASE" > complete_data.csv
    """
}

process convert_data
{
    input:
        path(raw_data)
    output:
        path('complete_data.parquet')

    script:
    """
    rtype prepare convert $raw_data complete_data.parquet
    """
}

process group_data
{
    memory '32.G'
    cpus 5


    input:
        path(ungrouped_parquet)

    output:
        path("grouped_data.parquet")

    script:
    """
    rtype preprocess group-data $ungrouped_parquet upi grouped_data.parquet
    """
}


process preprocess_data
{
    input:
        path(grouped_data)

    output:
        path('train_data.parquet'), emit: train
        path('test_data.parquet'), emit: test

    script:
    """
    wget "https://raw.githubusercontent.com/The-Sequence-Ontology/SO-Ontologies/master/Ontology_Files/so-simple.obo"
    rtype preprocess split-train-test $grouped_data --rng_seed 20221021
    """
}
