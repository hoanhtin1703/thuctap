import pandas as pd
from json import loads, dumps
from typing import Union
from fastapi import FastAPI,status,HTTPException

# ??  Cấu trúc code 
# TODO: Khởi tạo DataFrame 
#  ** Tạo đường dẫn truy xuất file
#  ** Đọc dữ liệu từ file excel và trả về DataFrame
# TODO: TODO: Xây dựng hàm để lọc dữ liệu từ DataFame
#  ** Logic code : Sử dụng các hàm thư viện để lọc từ pandas 
#  ** Trả về là một DataFrame đã xử lý xong logic
# TODO : Khởi tạo Request từ Fast API 
# ** Xây dựng các Request  ( GET,POST,PUT,DELETE)
# ** Xử lý các ngoại lệ 
# ** Response là một dictionary của DataFrame 



# TODO: Khởi tạo DataFrame 
def data():
    # ** Tạo đường dẫn truy xuất file
    path = 'Lớp học phần-HK2-Năm học_ 2023-2024.xlsx'
    # ** Đọc dữ liệu từ file excel và trả về DataFrame
    df = pd.read_excel(path)
    return df
# TODO: Xây dựng hàm để lọc dữ liệu từ DataFame
def list_danh_muc_hoc_phan(df):
    df = df[['Lớp học phần']]
    df.rename(columns={'Lớp học phần': 'Học phần'}, inplace=True)
    df['Học phần'] = df['Học phần'].str.replace(r'\(\d+\).*', '', regex=True).str.strip()
    df['total'] = df.groupby('Học phần')['Học phần'].transform('count')
    df.drop_duplicates(subset='Học phần', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
app = FastAPI()
# ** Xây dựng các Request  ( GET,POST,PUT,DELETE)
@app.get("/")
async def read_root():
    return "hello - Fast APi"
@app.get("/danh-muc-hoc-phan")
async def read_danh_muc_hoc_phan():
    #  ** Xử lý các ngoại lệ
    try:
        clean_data = list_danh_muc_hoc_phan(data())
        # ** Response là một dictionary của DataFrame
        return {
            "data": clean_data.to_dict(orient="records"),
            "total": len(clean_data),
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
