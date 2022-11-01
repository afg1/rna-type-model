import joblib
import polars as pl

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt

from labelling.labels import RNATypeCoarse


df_test = pl.read_parquet("test_data_ready.parquet")

trusted = [4, 8, 16, 18, 20, 24, 37]

df_trusted = df_test.filter(pl.col("dbid").is_in(trusted))

clf = joblib.load("coarse_random_forest.joblib")

# print(clf.score(df_test.drop(["website_label", "upi", "label"]).to_pandas(), df_test['label']))

preds = clf.predict(df_trusted.drop(["website_label", "upi", "label"]).to_pandas())

print(accuracy_score(df_trusted["label"], preds))

# print(df_test.groupby('website_label').count().select([pl.col('website_label'), pl.col("count")/float(df_test.height)]))
# print(df_test.groupby('label').count().select([pl.col('label'), pl.col("count")/float(df_test.height)]))

print(int(RNATypeCoarse.rRNA), int(RNATypeCoarse.tRNA), int(RNATypeCoarse.other))


cm = confusion_matrix(df_trusted["label"].to_pandas().values, preds, normalize="all")

ConfusionMatrixDisplay(cm).plot()

plt.show()
