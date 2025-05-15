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

    job_previews = parser.get_job_previews()
    print(f"Знайдено {len(job_previews)} вакансій на першій сторінці.")
    print("Приклади посилань:")
    for job in job_previews:
        print(f"{job['date']} | {job['title']} | {job['location']}")

    parser.save_to_file(job_previews)

if __name__ == "__main__":
    main()
