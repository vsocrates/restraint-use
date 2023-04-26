import pandas as pd

data = pd.read_csv("/Users/vsocrates/Downloads/prelim_notes(1).tsv", sep="\t")
print(data.shape)
print(data.columns)
data_subsample = data.sample(n=10, random_state=412)
data_subsample.to_csv("/Users/vsocrates/Downloads/prelim_notes_subset.csv", index=False)
