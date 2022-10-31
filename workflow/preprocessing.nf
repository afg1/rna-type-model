

process fetch_data
{
    input:
        path(data_fetch_query)

    output:
        path('complete_data.parquet')

    script:
    """
    psql -f $data_fetch_query "$PGDATABASE" > complete_data.csv
    convert_data complete_data.csv complete_data.parquet
    """
}

process group_data
{
    input:
        path(ungrouped_parquet)

    output:
        path("grouped_data.parquet")

    script:
    """
    group_data $ungrouped_parquet upi grouped_data.parquet
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
    load_and_split_data $grouped_data --rng 20221021
    """
}
