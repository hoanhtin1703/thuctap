import pandas as pd
# def load_data():
#     path = "./dataframe/DS SV KHOA 21_HKII NH 2023-2024.xlsx"
#     df = pd.read_excel(path)
#     return df

def load_data(file_path):
    df = pd.read_excel(file_path)
    return df
