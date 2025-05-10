import os
import random
import string
import hashlib
from datetime import datetime

class Utils:
    # ---------- Работа с файлами ----------
    @staticmethod
    def ensure_dir(path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def get_file_size(file_path: str) -> str:
        if not os.path.isfile(file_path):
            return "Файл не найден"
        size_bytes = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024

    @staticmethod
    def is_valid_file(file_path: str, allowed_extensions: list) -> bool:
        return os.path.isfile(file_path) and file_path.split(".")[-1].lower() in allowed_extensions

    # ---------- Генерация случайных данных ----------
    @staticmethod
    def generate_random_string(length: int = 16) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def generate_token(length: int = 32) -> str:
        return Utils.generate_random_string(length)

    # ---------- Работа с датами ----------
    @staticmethod
    def current_timestamp() -> str:
        return datetime.now().isoformat()

    @staticmethod
    def format_date(date_obj: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
        return date_obj.strftime(format_string)

    @staticmethod
    def parse_date(date_str: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        return datetime.strptime(date_str, format_string)

    # ---------- Хеширование файлов ----------
    @staticmethod
    def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
        if not os.path.isfile(file_path):
            raise FileNotFoundError("Файл не найден")

        hash_func = getattr(hashlib, algorithm, None)
        if not hash_func:
            raise ValueError(f"Алгоритм {algorithm} не поддерживается")

        hash_obj = hash_func()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    @staticmethod
    def save_file_hash(file_path: str, algorithm: str = "sha256"):
        hash_value = Utils.calculate_file_hash(file_path, algorithm)
        hash_file_path = f"{file_path}.hash"
        with open(hash_file_path, "w") as f:
            f.write(f"{algorithm}:{hash_value}")
        return hash_file_path

    @staticmethod
    def verify_file_integrity(file_path: str, expected_hash: str = None, algorithm: str = "sha256") -> bool:
        actual_hash = Utils.calculate_file_hash(file_path, algorithm)
        if expected_hash:
            return actual_hash.lower() == expected_hash.lower()

        # Если хэш не передан, ищем .hash файл
        hash_file_path = f"{file_path}.hash"
        if not os.path.isfile(hash_file_path):
            raise FileNotFoundError(".hash файл не найден")

        with open(hash_file_path, "r") as f:
            content = f.read().strip()
            saved_algorithm, saved_hash = content.split(":")
            if saved_algorithm != algorithm:
                raise ValueError(f"Ожидался алгоритм {saved_algorithm}, но указан {algorithm}")

        return actual_hash.lower() == saved_hash.lower()
