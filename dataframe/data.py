import pandas as pd
# def load_data():
#     path = "./dataframe/DS SV KHOA 21_HKII NH 2023-2024.xlsx"
#     df = pd.read_excel(path)
#     return df

def load_data(file_path):
    """Load data from all sheets of the Excel file."""
    # Đọc tất cả các sheet và lưu vào dictionary
    xls = pd.read_excel(file_path, sheet_name=None)
    
    # Lấy danh sách các DataFrame từ dictionary
    df_list = [df for sheet_name, df in xls.items()]
    
    return df_list
