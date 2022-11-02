#!/usr/bin/env python
import click
from snorkel.labeling import PandasLFApplier, LFAnalysis
from snorkel.labeling.apply.dask import PandasParallelLFApplier
import polars as pl
import numpy as np
import gzip as gz


def run_heuristic_labeller(train_data, output):
    from ..label_functions.coarse_labelling_functions import (
        length_based,
        score_based,
        accession_based,
        coverage_based,
        taxonomy_based_rfam,
        passthrough,
        is_lncRNA,
        is_miRNA,
        make_db_specific_lfs,
    )

    db_specific_lfs = list(make_db_specific_lfs())
    lfs = [
        # accession_based,
        score_based,
        taxonomy_based_rfam,
        length_based,
        coverage_based,
        # passthrough,
        is_lncRNA,
        is_miRNA,
    ]
    lfs.extend(db_specific_lfs)

    print("Loaded label functions, preparing to apply")
    print("Building single-thread applier...")
    applier = PandasLFApplier(lfs)

    print("Reading parquet")
    df = pl.read_parquet(train_data)
    df = df.sort(pl.col("dbid").arr.lengths(), reverse=True)

    print("Starting Applier...")
    L_train = applier.apply(df.to_pandas())

    output_fh = gz.GzipFile(output + ".gz", "w")

    print("Done, saving output")
    np.save(output_fh, L_train)

    ## Evaluate label model
    print("Label function evaluation details: ")
    print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
