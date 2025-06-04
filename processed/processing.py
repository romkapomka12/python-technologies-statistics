import os
import random
import time
from typing import List, Any, Tuple, Callable
from tqdm import tqdm

from config.config import get_random_headers, setup_driver
from config.logger import logger
from processed.cache import load_vacancy_from_cache, save_vacancy_to_cache
from models.models import JobDetail



class VacancyProcessor:
    def __init__(self):
        self.driver = setup_driver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def collect_metadata(self, scraper_cls, url: str, site_name: str) -> Tuple[List[str], int, int]:

        logger.info(f"\n{'=' * 50}")
        logger.info(f"🌐 Старт обробки {site_name}")

        scraper = scraper_cls(url, self.driver)

        logger.info("📄 Завантаження сторінок...")
        html_pages = scraper.get_all_pages_html()

        num_pages = len(html_pages)
        logger.info(f"🔢 Отримано {num_pages} сторінок")

        logger.info("🔗 Збір посилань...")
        links = scraper.get_all_links(html_pages)

        num_links = len(links)
        logger.info(f"🔗 Знайдено {num_links} посилань")

        return links, num_pages, num_links

    def process_vacancies(
            self,
            links: list[str],
            parser_vacancy_func: Callable[[str, str], JobDetail],
            site_name: str) -> list[JobDetail]:

        logger.info(f"Початок обробки {len(links)} вакансій з {site_name}")
        vacancies = []
        success_count = 0
        with tqdm(total=len(links), desc=f"Обробка {site_name}", unit="vac") as pbar:
            for i, link in enumerate(links, 1):
                try:
                    logger.info("Обробка %d/%d: %s", i, len(links), link)
                    cached_data = load_vacancy_from_cache(link)
                    if cached_data is not None:
                        vacancy = JobDetail(**cached_data)
                        logger.info(f"Завантажено з кешу: {link}")
                    else:
                        headers = get_random_headers()
                        self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})
                        logger.info(f"Використовується User-Agent: {headers['User-Agent']}")

                        self.driver.get(link)
                        time.sleep(random.uniform(0.5, 0.8))
                        html = self.driver.page_source
                        vacancy = parser_vacancy_func(link, html)
                        if vacancy:
                            save_vacancy_to_cache(link, vacancy)
                            logger.info(f"\nЗбережено в кеш: {link}")
                    if vacancy:
                        vacancies.append(vacancy)
                        success_count += 1
                    else:
                        logger.warning(f"Порожній результат для {link}")

                    pbar.set_postfix_str(f"Остання: {link[:30]}...")
                    pbar.update(1)
                except Exception as e:
                    logger.error(f"Помилка у {link}: {str(e)}")
                    pbar.update(1)
                    continue
        logger.info(f"Завершено {site_name}: {len(vacancies)}/{len(links)} успішних")
        return vacancies


def collect_vacancies_from_site(
        scraper_cls,
        url: str,
        parser_vacancy_func,
        site_name: str,

) -> List[Any]:
    with VacancyProcessor() as processor:
        try:
            links, _, _ = processor.collect_metadata(scraper_cls, url, site_name)
            return processor.process_vacancies(
                links=links,
                parser_vacancy_func=parser_vacancy_func,
                site_name=site_name
            )
        except Exception as e:
            logger.error(f"Помилка при зборі вакансій з {site_name}: {e}", exc_info=True)
            return []
