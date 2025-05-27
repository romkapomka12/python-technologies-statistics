import hashlib
import json
import os
from dataclasses import asdict

from config.logger import logger
from models.models import JobDetail

CACHE_DIR = "data/processed/cache_vacancies"


def _get_cache_path(link: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    hashed = hashlib.md5(link.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hashed}.json")


def load_vacancy_from_cache(link: str) -> dict:
    path = _get_cache_path(link)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_vacancy_to_cache(link: str, vacancy: JobDetail):
    path = _get_cache_path(link)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(vacancy), f, ensure_ascii=False, indent=2)

