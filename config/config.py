import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config.logger import logger

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
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",

    }


def setup_driver() -> webdriver.Chrome:
    try:
        logger.debug("Ініціалізація Chrome WebDriver")
        options = Options()
        options.add_argument(f"user-agent={get_random_headers()}")
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logger.critical("Помилка ініціалізації WebDriver: %s", str(e), exc_info=True)
        raise


JOB_SEARCH_DOU_UA = "https://jobs.dou.ua/vacancies/?category=Python"
JOB_SEARCH_WORK_UA = "https://www.work.ua/jobs-it-python/"

CSV_OUTPUT_PATH = "data/processed/output.csv"
