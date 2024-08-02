import json
from pathlib import Path

# Đường dẫn đến tệp lưu trữ thông tin
RENAMED_FILES_PATH = Path("./display/renamed_files.json")

def load_renamed_files():
    """Tải dữ liệu từ tệp JSON, nếu tệp tồn tại và không trống."""
    if RENAMED_FILES_PATH.exists():
        if RENAMED_FILES_PATH.stat().st_size > 0:
            try:
                with open(RENAMED_FILES_PATH, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return {}
            except Exception as e:
                print(f"Error loading renamed files: {e}")
                return {}
    return {}

# Từ điển lưu trữ thông tin các tệp đã đổi tên
renamed_files = load_renamed_files()

def save_renamed_files():
    """Lưu từ điển renamed_files vào tệp JSON."""
    try:
        with open(RENAMED_FILES_PATH, 'w') as f:
            json.dump(renamed_files, f, indent=4)  # Thêm indent để dễ đọc
        print(f"Renamed files saved: {renamed_files}")
    except Exception as e:
        print(f"Error saving renamed files: {e}")

def add_file(file_key: str, file_path: str):
    """Thêm tệp mới vào từ điển renamed_files và lưu lại."""
    renamed_files[file_key] = file_path
    save_renamed_files()

def get_file_path(file_key: str) -> str:
    """Lấy đường dẫn tệp từ từ điển renamed_files."""
    return renamed_files.get(file_key)

def file_exists(file_key: str) -> bool:
    """Kiểm tra xem tệp có tồn tại trong renamed_files không."""
    return file_key in renamed_files
