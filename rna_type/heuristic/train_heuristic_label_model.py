import polars as pl
import numpy as np

from rna_type.label_functions.labels import RNATypeCoarse
from snorkel.labeling.model import LabelModel
import joblib


def train_heuristic_label_model(train_data, train_labels, epochs):
    """
    Train a snorkel label model based on the output of the heuristic labelling step

    This should be reasonably accurate, and by definition takes into account the multiple
    opinions about what an entry is.
    """
    L_train = np.load(train_labels)
    df = pl.read_parquet(train_data).to_pandas()

    label_model = LabelModel(cardinality=3, verbose=True)
    label_model.fit(L_train, n_epochs=epochs, log_freq=100)

    # df["label"] = label_model.predict(L=L_train, tie_break_policy="abstain")

    # df_train = df[df.label != RNATypeCoarse.abstain]
    # df_train.to_parquet("LF_labelled_train_data.parquet")

    joblib.dump(label_model, "heuristic_LM.joblib")
