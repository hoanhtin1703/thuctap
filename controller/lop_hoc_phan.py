import pandas as pd

def filter_danh_muc_hoc_phan(df_list):
    """Filter and combine data from all DataFrames."""
    combined_df = pd.DataFrame()
    
    for df in df_list:
        # Lọc và xử lý dữ liệu từ mỗi sheet
        if 'Lớp học phần' in df.columns and 'GVHD' in df.columns:
            filtered_df = df[['Lớp học phần', 'GVHD']]
            filtered_df.drop_duplicates(subset=['Lớp học phần'], keep='first', inplace=True)
            filtered_df.reset_index(drop=True, inplace=True)
            combined_df = pd.concat([combined_df, filtered_df])
    
    # Xóa các bản ghi trùng lặp cuối cùng
    combined_df.drop_duplicates(subset=['Lớp học phần'], keep='first', inplace=True)
    combined_df.reset_index(drop=True, inplace=True)
    
    return combined_df
