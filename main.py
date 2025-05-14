from scraping.scraper import Scraper
from scraping.parser import JobParser

def main():
    print("Завантаження головної сторінки...")
    scraper = Scraper()
    html = scraper.single_page()

    print("Парсинг сторінки...")
    parser = JobParser(html)

    total = parser.get_total_vacancies()
    print(f"Загальна кількість вакансій: {total}")

    job_links = parser.get_job_links()
    print(f"Знайдено {len(job_links)} вакансій на першій сторінці.")
    print("Приклади посилань:")
    for link in job_links:
        print(f" - {link}")

if __name__ == "__main__":
    main()
