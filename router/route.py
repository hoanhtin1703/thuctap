from fastapi import APIRouter, status, HTTPException
from controller import lop_hoc_phan, danh_sach_sinh_vien
from data import data
from pydantic import BaseModel

danh_sach = danh_sach_sinh_vien.Danh_sach_sinh_vien
dataframe = data.load_data()
class Item(BaseModel):
    keyword: str
    
router = APIRouter()
@router.get('/danh-muc-hoc-phan')
async def get_danh_muc_hoc_phan():
    try:
        clean_data = lop_hoc_phan.filter_danh_muc_hoc_phan(dataframe)
        unique_courses = clean_data['Lớp học phần'].str.replace(r'\(\d+\).*', '', regex=True).str.strip().drop_duplicates(keep='first').reset_index(drop=True)
        return {
            "data": clean_data.to_dict(orient='records'),
            "hoc_phan": unique_courses,
            "total": len(clean_data),
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.get('/danh-sach-sinh-vien')
async def get_danh_sach_sinh_vien(item: Item):
    try:
        ds = danh_sach(dataframe, item.keyword)
        clean_data = ds.get_danh_sach_sinh_vien()
        return {
            "data": clean_data.to_dict(orient='records'),
            "total": len(clean_data),
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post('/xuat-excel-hoc-phan')
async def xuat_excel_hoc_phan(item: Item):
    try:
        ds = danh_sach(dataframe, item.keyword)
        result = ds.xuat_file_excel()
        return {
            "result": result,
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
