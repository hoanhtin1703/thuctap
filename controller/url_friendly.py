import re
import unidecode

# def clean_hoc_phan_name(lop_hoc_phan):
#     # Tách phần chính của tên lớp học phần, loại bỏ các phần bổ sung
#     # main_part = lop_hoc_phan.split('(')[0].strip()

#     main_part = re.sub(r'[_()]', '-', lop_hoc_phan)
#     main_part = re.sub(r'[^\w\s]', '-', lop_hoc_phan)
#     # main_part = lop_hoc_phan.split('(')[0].strip()
#     # s = re.sub(r"[()]", "", s)
#     # Chuyển đổi sang chữ thường, loại bỏ dấu tiếng Việt và thay thế dấu cách và dấu gạch ngang thừa
#     url_friendly_name = re.sub(r'[\s_-]+', '-', unidecode.unidecode(main_part.lower()))
#     return url_friendly_name

# def clean_lop_hoc_phan_name(name: str) -> str:
#     """Clean and convert class section name to URL-friendly format."""
#     # Chuyển đổi tên thành chữ thường và loại bỏ dấu
#     cleaned_name = unidecode.unidecode(name.lower())
    
#     # Thay thế tất cả các ký tự không phải chữ, số hoặc dấu gạch ngang bằng dấu gạch ngang
#     cleaned_name = re.sub(r'[_()]', '-', cleaned_name)
#     cleaned_name = re.sub(r'[^\w\s]', '-', cleaned_name)  # Thay thế các ký tự đặc biệt bằng dấu gạch ngang
#     cleaned_name = re.sub(r'[\s_-]+', '-', cleaned_name)   # Thay thế khoảng trắng và nhiều dấu gạch ngang liên tiếp bằng một dấu gạch ngang
#     # Loại bỏ dấu gạch ngang ở cuối chuỗi nếu có
#     cleaned_name = cleaned_name.rstrip('-')
    
#     return cleaned_name
import re
import unidecode

def clean_name(name: str) -> str:
    """Clean and convert class section name to URL-friendly format."""
    cleaned_name = unidecode.unidecode(name.lower())
    cleaned_name = re.sub(r'[^\w\s]', '-', cleaned_name)
    cleaned_name = re.sub(r'[\s_-]+', '-', cleaned_name).strip('-')
    return cleaned_name
