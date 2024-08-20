from typing import Union
from fastapi import APIRouter, status, HTTPException, File, UploadFile
from controller import filter, trich_xuat_ten_files
from dataframe import data
from pathlib import Path
from display import renamed_files, data_store
from controller.filter import Hoc_Phan,DanhSachSinhVien
import pandas as pd
router =  APIRouter()

# Import file excel
@router.post('/import-danh-muc-hoc-phan')
async def import_danh_muc_hoc_phan(file: UploadFile = File(...)):
    # Kiểm tra định dạng file
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Please upload an Excel file.")
    
    # Tạo và kết nối đường dẫn lưu trữ file
    display_folder = Path("./display/")
    display_folder.mkdir(exist_ok=True)

    # Thực hiện việc trích xuất và thay đổi tên file
    khoa_number, semester, school_year = trich_xuat_ten_files.extract_info_from_filename(file.filename)

    # Kiểm tra các cặp keyword trong tên file gốc có không
    if not khoa_number or not semester or not school_year:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File name does not contain all required information (KHOA, Semester, School Year).")
    
    # Thay đổi tên mới dựa trên keyword
    new_filename = f"KHOA-{khoa_number}-{semester}-{school_year}{file.filename[file.filename.rfind('.'):]}"
    
    # Lưu trữ vào thư mục display
    new_file_path = display_folder / new_filename

    try:
        with new_file_path.open("wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error saving file: {e}")

    # Thêm thông tin vào từ điển và lưu tệp JSON
    file_key = f"khoa-{khoa_number}-{semester}-{school_year}"
    new_data = {
        "Khoa": f"Khoá {khoa_number}",
        "Hoc_ky": f"Học kỳ {semester[-1]}",
        "Nam_hoc": f"{school_year.replace('-', ' - ')}",
        "Url_hoc_phan": file_key
    }
    
    data_store.add_imported_file(new_data)

    try:
        renamed_files.add_file(file_key, str(new_file_path))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating renamed files dictionary: {e}")

    print(f"File saved as: {new_filename}")
    print(f"Current renamed files dictionary: {renamed_files}")

    # Load dữ liệu từ file Excel
    try:
        df_list = data.load_data(new_file_path)
        if df_list:
            all_data = [df.head().to_dict(orient='records') for df in df_list]
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No data found in the file.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error loading data from file: {e}")

    return {"filename": new_filename, "data": all_data}


@router.get('/danh-muc-hoc-phan/{file_key}')
async def get_danh_muc_hoc_phan(file_key: str):
    try:
        # Lấy đường dẫn file từ từ điển renamed_files
        file_path = renamed_files.get_file_path(file_key)
        if not file_path:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        
        # Đọc dữ liệu từ tất cả các sheet trong file
        df_list = data.load_data(file_path)
        hoc_phan = Hoc_Phan(df_list)
        clean_data = hoc_phan.filter_danh_muc_hoc_phan()
        return {
            "data": clean_data.to_dict(orient='records'),
            "total": len(clean_data),
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.get('/{file_key}/{hoc_phan}')
async def get_danh_muc_hoc_phan(file_key: str,hoc_phan:str):
    try:
        # Lấy đường dẫn file từ từ điển renamed_files
        file_path = renamed_files.get_file_path(file_key)
        if not file_path:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        
        # Đọc dữ liệu từ tất cả các sheet trong file
        df_list = data.load_data(file_path)
        Hoc_phan = Hoc_Phan(df_list)
        clean_data = Hoc_phan.filter_lop_hoc_phan(hoc_phan)
        tenhocphan = clean_data['Lớp học phần'].replace(r'\(\d+\).*', '', regex=True).str.strip().drop_duplicates(keep="first")
        return {
            "data": clean_data.to_dict(orient='records'),
            "total": len(clean_data),
            "hocphan":tenhocphan.to_list(),
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.get('/{file_key}/{lop_hoc_phan}/danh-sach-sinh-vien')
async def get_danh_sach_sinh_vien(file_key: str,lop_hoc_phan:str):
    try:
        file_path = renamed_files.get_file_path(file_key)
        if not file_path:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        df_list =  data.load_data(file_path)
        # Khởi tạo Danh sách sinh viên
        ds = DanhSachSinhVien(df_list)
        clean_data = ds.filter_danh_sach_sinh_vien(lop_hoc_phan)
        clean_data.to_excel("data.xlsx")
        # Lấy tên học phần
        hocphan =  clean_data['Lớp học phần'].unique().tolist()

        total = {"Tổng số sinh viên": clean_data['Tổng số sinh viên'].iloc[0], 
                "Tổng số theo khóa" :clean_data['Tổng số sinh viên'].iloc[1]}
        
        # Lấy danh sách sinh viên từ cột đầu tiên đến cột Khóa 
        filter_data = clean_data.iloc[:, 1:11]
        return {
            "data" :filter_data.to_dict(orient="records"),
            "total" :total,
            "status": status.HTTP_200_OK,
            "hocphan": hocphan
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.get('/loc-ten-file')
async def loc_ten_file():
    try:
        return {
            "data" :data_store.imported_files_data,
            "status": status.HTTP_200_OK,
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))