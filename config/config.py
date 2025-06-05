import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.logger import logger


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
        logger.info("=" * 50)
        logger.info("Ініціалізація Chrome WebDriver")

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless=new')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')


        is_docker = os.path.exists("/.dockerenv")

        if is_docker:
            logger.info("Запуск у Docker-контейнері")
            chromedriver_path = "/usr/local/bin/chromedriver"
            options.binary_location = "/usr/bin/google-chrome-stable"


            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-setuid-sandbox')
            options.add_argument('--disable-infobars')

            service = Service(executable_path=chromedriver_path)
            logger.info(f"Використовується ChromeDriver: {chromedriver_path}")
        else:
            logger.info("Локальний запуск")
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)
        logger.info("Chrome WebDriver успішно ініціалізовано")
        return driver


    except Exception as e:
        logger.critical("Помилка ініціалізації WebDriver: %s", str(e), exc_info=True)
        raise


JOB_SEARCH_DOU_UA = "https://jobs.dou.ua/vacancies/?category=Python"
JOB_SEARCH_WORK_UA = "https://www.work.ua/jobs-it-python/"

CSV_OUTPUT_PATH = "data/processed/output.csv"

EXCHANGE_RATE: float = 42.5

SOURCE_FOLDERS = {
    "jobs.dou.ua": "dou",
    "www.work.ua": "work",
}
