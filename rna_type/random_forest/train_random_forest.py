from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
import polars as pl
from rna_type.labelling.labels import RNATypeCoarse
import numpy as np

from rna_type.utils.ontology_tests import is_child_of


def rna_2_coarse_label(typ):

    rRNA_agreement = [is_child_of("SO:0000252", t) for t in typ]
    tRNA_agreement = [is_child_of("SO:0000253", t) for t in typ]

    other_aggreement = [not r and not t for r, t in zip(rRNA_agreement, tRNA_agreement)]
    if any(rRNA_agreement):
        return RNATypeCoarse.rRNA  ## == 1
    elif any(tRNA_agreement):
        return RNATypeCoarse.tRNA  ## == 0
    else:
        return RNATypeCoarse.other  ## == 2
    #     rrna_prob = sum([int(a) for a in rRNA_agreement])/len(rRNA_agreement)
    #     trna_prob = sum([int(a) for a in tRNA_agreement])/len(tRNA_agreement)
    #     other_prob = sum([int(a) for a in other_aggreement])/len(other_aggreement)

    #     probs = [rrna_prob, trna_prob, other_prob]
    #     types = [RNATypeCoarse.rRNA, RNATypeCoarse.tRNA, RNATypeCoarse.other]
    #     return types[np.argmax(probs)]


## load and wrangle the training data - this has the heuristic labels in it
df_train = pl.read_parquet("LF_labelled_train_data.parquet")
df_train = df_train.drop(
    [
        "ac_rna_type",
        "r2dt_model_rna_type",
        "rfam_model_rna_type",
        "rna_type",
        "__index_level_0__",
    ]
)
df_train = df_train.explode(
    [
        "dbid",
        "ac_taxid",
        "overlap_count",
        "sequence_coverage",
        "model_taxid",
        "sequence_stop",
        "score",
    ]
)
df_train = df_train.fill_nan(None)
df_train = df_train.drop_nulls()

## Load and wrangle the test data. This has to be ungrouped, then have the rna type converted to the coarse labelling scheme
## I'm using rna_type which is what was shown on the website as 'ground truth'. It isn't, but I can potentially slice it so
## we only test against trusted dbs or something

# df_test = pl.read_parquet("LF_labelled_test_data.parquet")
# df_test = df_test.with_column( pl.col("rna_type").apply(rna_2_coarse_label ).alias("website_label"))
# df_test = df_test.drop(["ac_rna_type", "r2dt_model_rna_type", "rfam_model_rna_type", "rna_type", "__index_level_0__"])
# print(df_test)
# df_test = df_test.explode(["dbid", "ac_taxid", "overlap_count", "sequence_coverage", "model_taxid", "sequence_stop", "score"])
# df_test = df_test.fill_nan(None)
# df_test = df_test.drop_nulls()
# print(df_test)

# df_test.write_parquet("test_data_ready.parquet")


clf = RandomForestClassifier(n_estimators=50)
clf.fit(df_train.drop(["label", "upi"]).to_pandas(), df_train["label"])

joblib.dump(clf, "coarse_random_forest.joblib")
