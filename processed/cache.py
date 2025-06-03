from urllib.parse import urlparse
import os
import json
import hashlib
from dataclasses import asdict
from typing import Optional
from config.config import SOURCE_FOLDERS

CACHE_DIR = "data/processed/cache_vacancies/"


def _get_source_folder(url: str) -> str:
    domain = urlparse(url).netloc
    return SOURCE_FOLDERS.get(domain, "unknown")

def _get_cache_path(link: str) -> str:
    source_folder = _get_source_folder(link)
    cache_dir = os.path.join(CACHE_DIR, f"cache_vacancies_by_{source_folder}")
    os.makedirs(cache_dir, exist_ok=True)

    hashed = hashlib.md5(link.encode('utf-8')).hexdigest()
    return os.path.join(cache_dir, f"{hashed}.json")

def load_vacancy_from_cache(link: str) -> Optional[dict]:
    path = _get_cache_path(link)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_vacancy_to_cache(link: str, vacancy):
    path = _get_cache_path(link)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(vacancy), f, ensure_ascii=False, indent=2)


