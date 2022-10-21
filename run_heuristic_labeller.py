from snorkel.labeling.model import LabelModel
from snorkel.labeling import PandasLFApplier, LFAnalysis
import pandas as pd
import polars as pl
import numpy as np
from labelling.labels import RNATypeCoarse

from labelling.coarse_labelling_functions import (
    length_based,
    score_based,
    accession_based,
    coverage_based,
    taxonomy_based_r2dt,
    taxonomy_based_rfam,
)
from labelling.labels import RNATypeCoarse

from sklearn.metrics import confusion_matrix

import os


lfs = [
    accession_based,
    score_based,
    taxonomy_based_r2dt,
    taxonomy_based_rfam,
    length_based,
    coverage_based,
]  # score_based, taxonomy_based, length_based, coverage_based

applier = PandasLFApplier(lfs)

# print(df.dtypes)
df = pl.read_parquet("train_data.parquet").to_pandas()
df_test = pl.read_parquet("test_data.parquet").to_pandas()
if not os.path.exists("L_train.npy"):
    L_train = applier.apply(df)
    L_test = applier.apply(df_test)

    np.save("L_train.npy", L_train)
    np.save("L_test.npy", L_test)
else:
    L_train = np.load("L_train.npy")
    L_test = np.load("L_test.npy")


## Evaluate label model

print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())


# exit()

label_model = LabelModel(cardinality=3, verbose=True)
label_model.fit(L_train, n_epochs=100, log_freq=10)

df["label"] = label_model.predict(L=L_train, tie_break_policy="abstain")

df_train = df[df.label != RNATypeCoarse.abstain]
df_train.to_parquet("LF_labelled_train_data.parquet")


df_test["label"] = label_model.predict(L=L_test, tie_break_policy="abstain")
df_test = df_test[df_test.label != RNATypeCoarse.abstain]
df_test.to_parquet("LF_labelled_test_data.parquet")
