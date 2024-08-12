import pandas as pd
import re
import numpy as np
from controller import url_friendly
class Hoc_Phan:
    def __init__(self, df_list):
        self.df_list = df_list
    def filter_danh_muc_hoc_phan(self):
        """Filter and combine data from all DataFrames."""
        combined_df = pd.DataFrame()
        for df in self.df_list:
            # Lọc và xử lý dữ liệu từ mỗi sheet
            if 'Lớp học phần' in df.columns:
                filtered_df = df[['Lớp học phần']].copy()
                filtered_df['Lớp học phần'] = filtered_df['Lớp học phần'].replace(r'\(\d+\).*', '', regex=True).str.strip()
                filtered_df.drop_duplicates(subset=['Lớp học phần'], keep='first', inplace=True)
                combined_df = pd.concat([combined_df, filtered_df], ignore_index=True)

        # Xóa các bản ghi trùng lặp cuối cùng
        combined_df.drop_duplicates(subset=['Lớp học phần'], keep='first', inplace=True)
        combined_df.reset_index(drop=True, inplace=True)
        combined_df['sku'] = combined_df['Lớp học phần'].apply(url_friendly.clean_hoc_phan_name)
        return combined_df
    def filter_lop_hoc_phan(self,keyword):
        """Filter and combine data from all DataFrames."""
        combined_df = pd.DataFrame()
        for df in self.df_list:
            # Lọc và xử lý dữ liệu từ mỗi sheet
            if 'Lớp học phần' in df.columns and 'GVHD' in df.columns:
                filtered_df = df[['Lớp học phần',"GVHD"]].copy()
                filtered_df['sku'] = filtered_df['Lớp học phần'].apply(url_friendly.clean_hoc_phan_name)
                filtered_df.drop_duplicates(subset=['Lớp học phần'], keep='first', inplace=True)
                filtered_df = filtered_df.reset_index(drop=True)
                combined_df = pd.concat([combined_df, filtered_df], ignore_index=True)
        # Xóa các bản ghi trùng lặp cuối cùng
        combined_df.drop_duplicates(subset=['Lớp học phần'], keep='first', inplace=True)
        combined_df.reset_index(drop=True, inplace=True)
        filtered_by_hoc_phan = combined_df[combined_df['sku'].str.contains(re.escape(keyword))]
        return filtered_by_hoc_phan
class DanhSachSinhVien(Hoc_Phan):
    def filter_danh_sach_sinh_vien(self, keyword=None):
        combined_df = pd.DataFrame()
        lop_hoc_phan_clean = url_friendly.clean_lop_hoc_phan_name(keyword)
        for df in self.df_list:
            if 'Lớp học phần' in df.columns:
                df['Họ và Tên'] = df['Họ và tên'] + ' ' + df['Unnamed: 3']
                col_index = df.columns.get_loc('Họ và tên')
                
                # Xóa hai cột cũ
                df.drop(columns=['Họ và tên', 'Unnamed: 3'], inplace=True)
                
                # Chèn cột mới vào đúng vị trí của cột "Họ và tên" ban đầu
                cols = df.columns.tolist()
                cols.insert(col_index, 'Họ và Tên')
                df = df[cols]
                df['sku'] = df['Lớp học phần'].apply(url_friendly.clean_lop_hoc_phan_name)
                filtered_df = df[df['sku'].str.contains(re.escape(lop_hoc_phan_clean))]
                if not filtered_df.empty:  # Kiểm tra nếu DataFrame không rỗng
                    combined_df = pd.concat([combined_df, filtered_df])
        
        combined_df['Khóa'] = combined_df['Mã sinh viên'].str[:4]
        combined_df['Tổng số sinh viên'] = np.nan
        combined_df.drop_duplicates(inplace=True)
        combined_df.reset_index(drop=True, inplace=True)

        for lop_hoc_phan in combined_df['Lớp học phần'].unique():
            # Tính tổng số sinh viên cho từng lớp học phần
            idx = combined_df[combined_df['Lớp học phần'] == lop_hoc_phan].index[0]
            total_students = combined_df[combined_df['Lớp học phần'] == lop_hoc_phan]['Mã sinh viên'].nunique()
            combined_df.at[idx, 'Tổng số sinh viên'] = total_students


            # Tính tổng số sinh viên theo khóa cho từng lớp học phần
            total_students_by_khoa = combined_df[combined_df['Lớp học phần'] == lop_hoc_phan].groupby('Khóa')['Mã sinh viên'].nunique().reset_index()
            total_students_by_khoa.columns = ['Khóa', 'Tổng số sinh viên']
            total_students_khoa = '; '.join(total_students_by_khoa.apply(lambda x: f"{x['Khóa']} - {x['Tổng số sinh viên']}", axis=1))
            combined_df.at[idx + 1, 'Tổng số sinh viên'] = total_students_khoa

        return combined_df
