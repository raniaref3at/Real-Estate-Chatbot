import pandas as pd
from settings import dataset_url

def load_dataset():
    dataset = pd.read_csv(dataset_url)
    dataset.columns = dataset.columns.str.strip()
    return dataset
