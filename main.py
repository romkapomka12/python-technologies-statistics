# import requests
from datetime import datetime

from scraping.scraper import Scraper
from scraping.parser import JobDetail, JobParser, parse_job_previews, save_to_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("Завантаження всієї інформації (через Selenium)...")
    scraper = Scraper()
    html = scraper.all_pages()

    print("Парсинг всіх сторінок...")
    parser = JobParser(html)
    links = parser.get_job_links()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    start_time = datetime.now()
    vacancies = []
    for i, link in enumerate(links):
        try:
            print(f"➡️ {i + 1}. Обробка: {link}")
            driver.get(link)
            html = driver.page_source
            vacancy = parse_job_previews(link, html)
            vacancies.append(vacancy)
        except Exception as e:
            print(f"Помилка при парсингу: {e}")

    total = parser.get_total_vacancies()
    print(f"Загальна кількість вакансій: {total}")

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"⏱ Тривалість виконання: {duration}")

    job_previews = parser.get_job_links()
    print(f"Знайдено {len(job_previews)} вакансій.")

    save_to_file(vacancies)


if __name__ == "__main__":
    main()
