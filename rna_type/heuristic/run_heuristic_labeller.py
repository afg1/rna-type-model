#!/usr/bin/env python
import click
from snorkel.labeling import PandasLFApplier, LFAnalysis
import polars as pl
import numpy as np

from rna_type.labelling.coarse_labelling_functions import (
    length_based,
    score_based,
    accession_based,
    coverage_based,
    taxonomy_based_r2dt,
    taxonomy_based_rfam,
)
from labelling.labels import RNATypeCoarse


lfs = [
    accession_based,
    score_based,
    taxonomy_based_r2dt,
    taxonomy_based_rfam,
    length_based,
    coverage_based,
]


@click.command()
@click.argument("train_data")
@click.argument("output")
def run_heuristic_labeller(train_data, output):
    applier = PandasLFApplier(lfs)

    # print(df.dtypes)
    df = pl.read_parquet(train_data).to_pandas()

    L_train = applier.apply(df)
    np.save(output, L_train)

    ## Evaluate label model
    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())


if __name__ == "__main__":
    run_heuristic_labeller()
