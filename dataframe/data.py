import pandas as pd
def load_data():
    path = "./dataframe/DS SV KHOA 21_HKII NH 2023-2024.xlsx"
    df = pd.read_excel(path)
    return df
