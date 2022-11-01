#!/usr/bin/env python
import click
import pandas as pd
import polars as pl
import numpy as np
from rna_type.labelling.labels import RNATypeCoarse
from snorkel.labeling.model import LabelModel
import joblib


@click.command()
@click.argument("train_data")
@click.argument("train_labels")
def train_heuristic_label_model(train_data, train_labels):
    """
    Train a snorkel label model based on the output of the heuristic labelling step

    This should be reasonably accurate, and by definition takes into account the multiple
    opinions about what an entry is.
    """
    L_train = np.load(train_labels)
    df = pl.read_parquet(train_data).to_pandas()

    label_model = LabelModel(cardinality=3, verbose=True)
    label_model.fit(L_train, n_epochs=100, log_freq=10)

    df["label"] = label_model.predict(L=L_train, tie_break_policy="abstain")

    df_train = df[df.label != RNATypeCoarse.abstain]
    df_train.to_parquet("LF_labelled_train_data.parquet")

    joblib.dump(label_model, "heuristic_LM.joblib")


if __name__ == "__main__":
    train_heuristic_label_model()
