import pandas as pd
import re
class Danh_sach_sinh_vien():
    def __init__(self,df,keyword):
        self.df = df
        self.keyword = keyword
    def get_danh_sach_sinh_vien(self):
        df_filtered = self.df.loc[self.df['Lớp học phần'].str.contains(re.escape(self.keyword))]
        return df_filtered
    def xuat_file_excel(self):
        df_filtered = self.get_danh_sach_sinh_vien()
        df_filtered['Khóa'] = df_filtered['Mã sinh viên'].str[:4]
        result_df = df_filtered.groupby('Khóa')['Mã sinh viên'].count().reset_index(name='số_lượng')
        result_df.loc[0, 'Tổng số sinh viên'] = result_df['số_lượng'].sum()
        df_filtered.sort_values(by='Mã sinh viên', inplace=True,ascending=True)
        with pd.ExcelWriter('Danh sách lớp '+ self.keyword+'.xlsx') as writer:
            df_filtered.to_excel(writer, sheet_name='Danh_sach_sinh_vien', index=False)
            result_df.to_excel(writer, sheet_name='Thong_ke', index=False)
        return "Xuất file excel thành công"