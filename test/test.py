import pandas as pd

# Đọc dữ liệu từ tệp Excel
path = './data/DS SV KHOA 21_HKII NH 2023-2024.xlsx'
xls = pd.ExcelFile(path)
# data =xls.parse(sheet_name="16. Kien truc&GT IoT")
# Initialize an empty list to store DataFrames
dataframes = []

# # Loop through sheet names and read each sheet into a DataFrame
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)
    dataframes.append(df)
# Concatenate DataFrames vertically
merged_df = pd.concat(dataframes, ignore_index=True)

print(merged_df.shape)
# # Now `merged_df` contains data from all worksheets
# sheets_cannot_parse = []

# for sheet_name in xls.sheet_names:
#     try:
#         xls.parse(sheet_name)
#     except Exception as e:
#         sheets_cannot_parse.append(sheet_name)

# print("Các sheet không thể parse được:")
# for sheet_name in sheets_cannot_parse:
#     print(sheet_name)