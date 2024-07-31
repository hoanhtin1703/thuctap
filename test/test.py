import pandas as pd
import re
# Đọc dữ liệu từ tệp Excel
path = './data/DS SV KHOA 21_HKII NH 2023-2024.xlsx'
df = pd.read_excel(path)
# Lọc các hàng chứa từ khóa "Automat và Ngôn ngữ hình thức (9)"
keyword = "Automat và Ngôn ngữ hình thức (9)"
df_filtered = df.loc[df['Lớp học phần'].str.contains(re.escape(keyword))]
# Assign values to the 'Khóa' column using .loc
df_filtered['Khóa'] = df_filtered['Mã sinh viên'].str[:4]
# Giả sử DataFrame của bạn có tên là 'df_filtered'
result_df = df_filtered.groupby('Khóa')['Mã sinh viên'].count().reset_index(name='số_lượng')
# Tính tổng số lượng sinh viên cho mỗi khóa
result_df.loc[0, 'Tổng số sinh viên'] = result_df['số_lượng'].sum()
# Hiển thị DataFrame kết quả
df_filtered.sort_values(by='Mã sinh viên', inplace=True,ascending=True)
with pd.ExcelWriter('Danh sách lớp '+ keyword+'.xlsx') as writer:
    df_filtered.to_excel(writer, sheet_name='Danh_sach_sinh_vien', index=False)
    result_df.to_excel(writer, sheet_name='Thong_ke', index=False)
print(result_df)


# Hiển thị Series kết quả

