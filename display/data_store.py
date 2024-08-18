import json
from pathlib import Path

# Đường dẫn đến tệp lưu trữ thông tin
IMPORTED_FILES_PATH = Path("./display/imported_files_data.json")

def load_imported_files():
    """Tải dữ liệu từ tệp JSON, nếu tệp tồn tại và không trống."""
    if IMPORTED_FILES_PATH.exists():
        if IMPORTED_FILES_PATH.stat().st_size > 0:
            try:
                with open(IMPORTED_FILES_PATH, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return []
            except Exception as e:
                print(f"Error loading imported files data: {e}")
                return []
    return []

# Từ điển lưu trữ thông tin các tệp đã nhập
imported_files_data = load_imported_files()

def save_imported_files():
    """Lưu danh sách imported_files_data vào tệp JSON."""
    try:
        with open(IMPORTED_FILES_PATH, 'w') as f:
            json.dump(imported_files_data, f, indent=4)  # Thêm indent để dễ đọc
        print(f"Imported files data saved: {imported_files_data}")
    except Exception as e:
        print(f"Error saving imported files data: {e}")

def add_imported_file(file_data: dict):
    """Thêm tệp mới vào danh sách imported_files_data và lưu lại."""
    imported_files_data.append(file_data)
    save_imported_files()

def get_imported_files() -> list:
    """Lấy danh sách tệp từ imported_files_data."""
    return imported_files_data
