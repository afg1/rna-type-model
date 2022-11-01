#!/usr/bin/env python

import pandas as pd
import polars as pl
import networkx as nx
import obonet
import click
import numpy as np


so = obonet.read_obo("so-simple.obo")

base_so_terms = ["SO:0000655", "SO:0000188", "SO:0000836", "SO:0000673"]


@click.command()
@click.argument("grouped_data", type=click.File("r"))
@click.option("--rng_seed", type=int)
def load_and_split(grouped_data, rng_seed=1234):
    """
    Load grouped parquet data and split it into train and test sets.

    Try to extract the 'trusted' data and mix it into the train and test datasets equally

    """
    print("Loading pre-grouped data to split for train and test")
    rng = np.random.default_rng(rng_seed)
    print(f"Supplied random seed: {rng_seed}")

    all_data = pl.scan_parquet(grouped_data.name)

    print(all_data.collect())
    trusted_data = all_data.filter(pl.col("contains_trusted")).collect()
    trusted_train_test = pl.from_numpy(
        (rng.random(size=trusted_data.height) > 0.75), columns=["test"]
    )
    trusted_data = trusted_data.with_column(
        trusted_train_test.select(pl.col("test")).to_series().alias("test")
    )

    remaining_data = all_data.filter(pl.col("contains_trusted").is_not()).collect()
    remaining_train_test = pl.from_numpy(
        (rng.random(size=remaining_data.height) > 0.75), columns=["test"]
    )
    remaining_data = remaining_data.with_column(
        remaining_train_test.select(pl.col("test")).to_series().alias("test")
    )

    trusted_data_train = trusted_data.filter(pl.col("test").is_not())
    trusted_data_test = trusted_data.filter(pl.col("test"))

    remaining_data_train = remaining_data.filter(pl.col("test").is_not())
    remaining_data_test = remaining_data.filter(pl.col("test"))

    train_data = trusted_data_train.vstack(remaining_data_train)
    test_data = trusted_data_test.vstack(remaining_data_test)

    print("Data split completed, writing parquet")

    test_data.write_parquet("test_data.parquet")
    train_data.write_parquet("train_data.parquet")

    print("Double check below, the two numbers should be equal")
    print(test_data.height + train_data.height, all_data.collect().height)


if __name__ == "__main__":
    load_and_split()
