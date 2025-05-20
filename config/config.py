import random

TECHNOLOGIES = [
    "Python", "Django", "Flask", "PostgreSQL", "Docker", "AWS",
    "JavaScript", "React", "FastAPI", "Git", "Linux", "Celery"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0",
]


def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS)
    }


JOB_SEARCH_URL = "https://jobs.dou.ua/vacancies/?category=Python"

CSV_OUTPUT_PATH = "data/processed/output.csv"
