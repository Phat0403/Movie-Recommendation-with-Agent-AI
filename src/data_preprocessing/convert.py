import pandas as pd
import numpy as np

def remove_end_line(x):
    if isinstance(x, str):
        x = x.replace("\n", "")
        x = x.replace("\r", "")
        x = x.replace("\t", "")
        x = x.replace("\f", "")
        x = x.replace("\v", "")
        x = x.replace("\b", "")
        x = x.replace("\a", "")
    return x

df = pd.read_csv("../backend/data/movies_2020_new.csv", sep=",", encoding="utf-8")

df["description"] = df["description"].apply(remove_end_line)

df.to_csv("../backend/data/movies_2020_new.csv", sep=",", encoding="utf-8", index=False)