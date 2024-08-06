from typing import Union
from fastapi import APIRouter, status, HTTPException, File, UploadFile
from controller import lop_hoc_phan, trich_xuat_ten_files
from dataframe import data
from pathlib import Path
from display import renamed_files
from controller.lop_hoc_phan import Hoc_Phan,DanhSachSinhVien

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
    try:
        renamed_files.add_file(file_key, str(new_file_path))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating renamed files dictionary: {e}")

    try:
        df = data.load_data(new_file_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error loading data from file: {e}")

    print(f"File saved as: {new_filename}")
    print(f"Current renamed files dictionary: {renamed_files}")

    return {"filename": new_filename, "data": df.head().to_dict(orient='records')}

@router.get('/danh-muc-hoc-phan-{file_key}')
async def get_danh_muc_hoc_phan(file_key: str):
    try:
        # Lấy đường dẫn file từ từ điển renamed_files
        file_path = renamed_files.get_file_path(file_key)
        if not file_path:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        
        # Đọc dữ liệu từ tất cả các sheet trong file
        df_list = data.load_data(file_path)
        hoc_phan = Hoc_Phan()
        clean_data = hoc_phan.filter_danh_muc_hoc_phan(df_list)
        unique_courses = clean_data['Lớp học phần'].str.replace(r'\(\d+\).*', '', regex=True).str.strip().drop_duplicates(keep='first').reset_index(drop=True)
        
        return {
            "data": clean_data.to_dict(orient='records'),
            "hoc_phan": unique_courses.to_list(),
            "total": len(clean_data),
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.get('/danh-sach-sinh-vien/')
async def get_danh_sach_sinh_vien(khoa: str,hoc_phan:str,lop_hoc_phan):
    try:
        file_path = renamed_files.get_file_path(khoa)
        if not file_path:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        df_list =  data.load_data(file_path)
        # Khởi tạo Danh sách sinh viên
        ds = DanhSachSinhVien(df_list)
        clean_data = ds.filter_hoc_phan_con(hoc_phan,lop_hoc_phan)

        hocphan =  clean_data['Lớp học phần'].unique().tolist()

        total = {"Tổng số sinh viên": clean_data['Tổng số sinh viên'].iloc[0], 
                "Tổng số theo khóa" :clean_data['Tổng số sinh viên'].iloc[1]}
        filter_data = clean_data.iloc[:, 1:10]
        return {
            "data" :filter_data.to_dict(orient="records"),
            "total" :total,
            "status": status.HTTP_200_OK,
            "hocphan": hocphan
        #
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



