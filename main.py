from config.config import JOB_SEARCH_WORK_UA, JOB_SEARCH_DOU_UA
from config.logger import logger, setup_logging
from data.processed.processing import collect_vacancies_from_site
from scraping.scraper import JobsDouScraper, WorkUaScraper
from scraping.parser import parse_dou_ua_previews, parse_work_ua_previews
from utils.save import save_to_file


def main():

    logger.info("\n ЗАГАЛЬНА ІНФОРМАЦІЯ ДО ЗБОРУ ОПИСІВ:")

    dou_vacancies = collect_vacancies_from_site(
        JobsDouScraper, JOB_SEARCH_DOU_UA, parse_dou_ua_previews, "DOU.UA"
    )

    work_vacancies = collect_vacancies_from_site(
        WorkUaScraper, JOB_SEARCH_WORK_UA, parse_work_ua_previews, "Work.ua"
    )

    save_to_file(dou_vacancies + work_vacancies)
    logger.info("\n Усі дані успішно зібрано та збережено")


if __name__ == "__main__":
    setup_logging()
    main()
