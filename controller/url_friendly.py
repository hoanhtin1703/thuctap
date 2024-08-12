import re
import unidecode

def clean_hoc_phan_name(lop_hoc_phan):
    # Tách phần chính của tên lớp học phần, loại bỏ các phần bổ sung
    # main_part = lop_hoc_phan.split('(')[0].strip()
    # Chuyển đổi sang chữ thường, loại bỏ dấu tiếng Việt và thay thế dấu cách và dấu gạch ngang thừa
    url_friendly_name = re.sub(r'[\s-]+', '-', unidecode.unidecode(lop_hoc_phan.lower()))
    return url_friendly_name

def clean_lop_hoc_phan_name(name: str) -> str:
    """Clean and convert class section name to URL-friendly format."""
    # Chuyển đổi tên thành chữ thường và loại bỏ dấu
    cleaned_name = unidecode.unidecode(name.lower())
    
    # Thay thế tất cả các ký tự không phải chữ, số hoặc dấu gạch ngang bằng dấu gạch ngang
    cleaned_name = re.sub(r'[_()]', '-', cleaned_name)
    cleaned_name = re.sub(r'[^\w\s]', '-', cleaned_name)  # Thay thế các ký tự đặc biệt bằng dấu gạch ngang
    cleaned_name = re.sub(r'[\s-]+', '-', cleaned_name)   # Thay thế khoảng trắng và nhiều dấu gạch ngang liên tiếp bằng một dấu gạch ngang
    # Loại bỏ dấu gạch ngang ở cuối chuỗi nếu có
    cleaned_name = cleaned_name.rstrip('-')
    
    return cleaned_name
