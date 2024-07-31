from typing import Union
from fastapi import APIRouter, status, HTTPException
from controller import lop_hoc_phan
from dataframe import data
router =  APIRouter()
@router.get('/danh-muc-hoc-phan')
async def get_danh_muc_hoc_phan():
    try:
        clean_data = lop_hoc_phan.filter_danh_muc_hoc_phan(data.load_data())
        unique_courses = clean_data['Lớp học phần'].str.replace(r'\(\d+\).*', '', regex=True).str.strip().drop_duplicates(keep='first').reset_index(drop=True)
        return {
            "data": clean_data.to_dict(orient='records'),
            "hoc_phan": unique_courses,
            "total": len(clean_data),
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))