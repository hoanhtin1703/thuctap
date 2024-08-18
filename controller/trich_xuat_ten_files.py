import pandas as pd
import re

def extract_info_from_filename(filename: str):
    """Trích xuất số KHOA, học kỳ và năm học từ tên tệp."""
    # Trích xuất số KHOA
    khoa_match = re.search(r'KHOA\s*(\d+)', filename, re.IGNORECASE)
    khoa_number = khoa_match.group(1) if khoa_match else None
    
    # Trích xuất học kỳ
    hki_match = re.search(r'HKI', filename, re.IGNORECASE)
    hkii_match = re.search(r'HKII', filename, re.IGNORECASE)
    semester = "hk2" if hki_match else "hk1" if hkii_match else None
    
    # Trích xuất năm học
    year_match = re.search(r'(\d{4})[-\s]*(\d{4})', filename)
    if year_match:
        start_year = year_match.group(1)[2:]
        end_year = year_match.group(2)[2:]
        school_year = f"{start_year}-{end_year}"
    else:
        school_year = None
    
    return khoa_number, semester, school_year