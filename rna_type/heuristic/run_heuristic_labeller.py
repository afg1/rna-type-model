#!/usr/bin/env python
import click
from snorkel.labeling import PandasLFApplier, LFAnalysis
from snorkel.labeling.apply.dask import PandasParallelLFApplier
import polars as pl
import numpy as np


@click.command()
@click.argument("train_data")
@click.argument("output")
@click.option("--parallel", default=False)
def run_heuristic_labeller(train_data, output, parallel):
    from ..labelling.coarse_labelling_functions import (
        length_based,
        score_based,
        accession_based,
        coverage_based,
        taxonomy_based_rfam,
        passthrough,
        is_lncRNA,
        is_miRNA,
    )

    lfs = [
        accession_based,
        score_based,
        taxonomy_based_rfam,
        length_based,
        coverage_based,
        passthrough,
        is_lncRNA,
        is_miRNA,
    ]

    print("Loaded label functions, preparing to apply")
    if parallel:
        print("Building parallel applier...")
        applier = PandasParallelLFApplier(lfs)
    else:
        print("Building single-thread applier...")
        applier = PandasLFApplier(lfs)

    print("Reading parquet")
    df = pl.read_parquet(train_data)
    df = df.sort(pl.col("dbid").arr.lengths())

    print("Starting Applier...")
    chunk_size = 100_000_000
    L_train = None
    for offset in range(0, df.height):
        print(offset)
        df_slice = df.slice(offset * chunk_size, chunk_size)
        L_train_slice = applier.apply(df_slice.to_pandas())
        if offset == 0:
            L_train = L_train_slice
        else:
            L_train = np.vstack((L_train, L_train_slice))

    print(L_train.shape, df.height)

    # L_train = applier.apply(df)

    print("Done, saving output")
    np.save(output, L_train)

    ## Evaluate label model
    print("Label function evaluation details: ")
    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())


if __name__ == "__main__":
    run_heuristic_labeller()
