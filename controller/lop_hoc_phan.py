
def filter_danh_muc_hoc_phan(df):
    df = df[['Lớp học phần', 'GVHD']]
    df.drop_duplicates(subset=['Lớp học phần'], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df