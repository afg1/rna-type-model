import pandas as pd
import polars as pl
from sklearn.model_selection import train_test_split
import networkx as nx
import obonet
import click
import numpy as np


so = obonet.read_obo("https://raw.githubusercontent.com/The-Sequence-Ontology/SO-Ontologies/master/Ontology_Files/so-simple.obo")

base_so_terms = ["SO:0000655", "SO:0000188", "SO:0000836", "SO:0000673"]


# print(nx.shortest_path(so, "SO:0000647", "SO:0000655") )

@click.command()
@click.argument("db_dump", type=click.File("r"))
def load_and_split(db_dump):
    if db_dump.name.endswith("csv"):
        all_data = pl.read_csv(db_dump.name)
    elif db_dump.name.endswith("parquet"):
        all_data = pl.read_parquet(db_dump.name)
    print(all_data.shape, all_data.height, all_data.columns)

    grouped = all_data.groupby(["upi"]).agg_list()

    train_test = pl.from_numpy((np.random.uniform(size=grouped.height) > 0.75).astype(np.int32), columns=["test"])

    print(train_test.height)

    grouped = grouped.with_column(train_test.select(pl.col("test")).to_series().alias("test") )

    train_data = grouped.filter(pl.col("test") == 0).drop("test")

    test_data = grouped.filter(pl.col("test") == 1).drop("test")

    print(train_data)


    # trustworthy_ids = [4, 8, 16, 18, 20, 24, 37]
    # trustworthy_accessions = all_data.loc[all_data["dbid"].isin(trustworthy_ids)]
    # trustworthy_data = all_data.loc[all_data["upi"].isin(trustworthy_accessions["upi"])]

    # print(trustworthy_data.shape)

    # available_training_data = all_data.drop(all_data[all_data["upi"].isin(trustworthy_accessions['upi']) ].index  )

    # print(available_training_data.shape)

    # ## groupby UPI and aggregate all other values into lists
    # # grouped = available_training_data.groupby("upi").agg(list)    

    # ## Now split the grouped df to train & test

    # train_data, test_data = train_test_split(available_training_data, test_size=0.25, random_state=123345)


    test_data.write_parquet("test_data.parquet")
    train_data.write_parquet("train_data.parquet")





if __name__ == "__main__":
    load_and_split()


