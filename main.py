from config.config import JOB_SEARCH_WORK_UA, JOB_SEARCH_DOU_UA
from data.processed.processing import collect_vacancies_from_site, collect_links_metadata
from scraping.scraper import JobsDouScraper, WorkUaScraper
from scraping.parser import parse_dou_ua_previews, parse_work_ua_previews
from utils.save import save_to_file


def main():
    links_dou, pages_dou, count_dou, driver_dou = collect_links_metadata(
        JobsDouScraper, JOB_SEARCH_DOU_UA, "DOU.UA"
    )

    links_work, pages_work, count_work, driver_work = collect_links_metadata(
        WorkUaScraper, JOB_SEARCH_WORK_UA, "Work.ua"
    )

    print("\n📊 ЗАГАЛЬНА ІНФОРМАЦІЯ ДО ЗБОРУ ОПИСІВ:")
    print(f"🔹 DOU.UA — {pages_dou} сторінок, {count_dou} посилань")
    print(f"🔹 Work.ua — {pages_work} сторінок, {count_work} посилань")

    vacancies_dou = collect_vacancies_from_site(
        JobsDouScraper,
        JOB_SEARCH_DOU_UA,
        parse_dou_ua_previews,
        "DOU.UA"
    )

    vacancies_work = collect_vacancies_from_site(
        WorkUaScraper,
        JOB_SEARCH_WORK_UA,
        parse_work_ua_previews,
        "Work.ua"
    )

    all_vacancies = vacancies_dou + vacancies_work
    save_to_file(all_vacancies)

    print(f"\n✅ Усього збережено: {len(all_vacancies)} вакансій")


if __name__ == "__main__":
    main()

