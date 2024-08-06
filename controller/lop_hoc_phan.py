import pandas as pd
import re
import numpy as np
class Hoc_Phan:
    def __init__(self, df_list):
        self.df_list = df_list
    def filter_danh_muc_hoc_phan(self):
        """Filter and combine data from all DataFrames."""
        combined_df = pd.DataFrame()
        for df in self.df_list:
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
class DanhSachSinhVien(Hoc_Phan):
    def filter_lop_hoc_phan(self, keyword=None):
        self_df = self.df_list
        combined_df = pd.DataFrame()
        for df in self_df:
            if 'Lớp học phần' in df.columns:
                filtered_df = df[df['Lớp học phần'].str.contains(re.escape(keyword))]
                if not filtered_df.empty:  # Kiểm tra nếu DataFrame không rỗng
                    combined_df = pd.concat([combined_df, filtered_df])
        
        combined_df.drop_duplicates(inplace=True)
        combined_df.reset_index(drop=True, inplace=True)
        combined_df['Khóa'] = combined_df['Mã sinh viên'].str[:4]
        combined_df['Tổng số sinh viên'] = np.nan

        # Tính tổng số sinh viên cho từng lớp học phần
        for lop_hoc_phan in combined_df['Lớp học phần'].unique():
            idx = combined_df[combined_df['Lớp học phần'] == lop_hoc_phan].index[0]
            total_students = combined_df[combined_df['Lớp học phần'] == lop_hoc_phan]['Mã sinh viên'].nunique()
            combined_df.at[idx, 'Tổng số sinh viên'] = total_students

        # Tính tổng số sinh viên theo khóa cho từng lớp học phần và chèn vào hàng thứ 2
        for lop_hoc_phan in combined_df['Lớp học phần'].unique():
            idx = combined_df[combined_df['Lớp học phần'] == lop_hoc_phan].index[0]
            total_students_by_khoa = combined_df[combined_df['Lớp học phần'] == lop_hoc_phan].groupby('Khóa')['Mã sinh viên'].nunique().reset_index()
            total_students_by_khoa.columns = ['Khóa', 'Tổng số sinh viên']
            total_students_str = '; '.join(total_students_by_khoa.apply(lambda x: f"{x['Khóa']} - {x['Tổng số sinh viên']}", axis=1))
            combined_df.at[idx + 1, 'Tổng số sinh viên'] = total_students_str
        return combined_df
    def filter_hoc_phan_con(self, keyword=None, secondary_keyword=None):
        combined_df = self.filter_lop_hoc_phan(keyword)
        df_filtered = combined_df[combined_df['Lớp học phần'].str.contains(re.escape(secondary_keyword))]
        df_filtered.reset_index(drop=True, inplace=True)
        return df_filtered
    
