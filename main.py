import time
from datetime import timedelta
from config.config import JOB_SEARCH_WORK_UA, JOB_SEARCH_DOU_UA, setup_driver
from config.logger import logger, setup_logging
from processed.processing import collect_vacancies_from_site
from scraping.scraper import JobsDouScraper, WorkUaScraper
from scraping.parser import parse_dou_ua_previews, parse_work_ua_previews
from utils.save import save_to_file


def main():
    driver = setup_driver()
    start_time = time.time()
    logger.info("\n ЗАГАЛЬНА ІНФОРМАЦІЯ ДО ЗБОРУ ОПИСІВ:")

    dou_vacancies = collect_vacancies_from_site(
        JobsDouScraper, JOB_SEARCH_DOU_UA, parse_dou_ua_previews, "DOU.UA",
    )
    work_vacancies = collect_vacancies_from_site(
        WorkUaScraper, JOB_SEARCH_WORK_UA, parse_work_ua_previews, "Work.ua",
    )

    save_to_file(dou_vacancies + work_vacancies)

    elapsed = timedelta(seconds=round(time.time() - start_time))

    logger.info("Час виконання - %s", elapsed)
    driver.quit()


if __name__ == "__main__":
    setup_logging()
    main()
