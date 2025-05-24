import random
import re
import time
from abc import ABC
from typing import Optional, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import JOB_SEARCH_WORK_UA, JOB_SEARCH_DOU_UA
from models.models import JobDetail
from scraping.base_scraper import BaseScraper
from selenium.webdriver import Chrome as WebDriver

from bs4 import BeautifulSoup
from typing import List


class WorkUaScraper(BaseScraper):
    def __init__(self, url: str = JOB_SEARCH_WORK_UA, driver: WebDriver = None):
        if driver is None:
            driver = webdriver.Chrome()
        super().__init__(driver, url)

    def get_num_pages(self) -> int:
        self.driver.get(self.url)
        try:
            pagination = self.driver.find_element(By.CSS_SELECTOR, "ul.pagination.hidden-xs")
            page_links = pagination.find_elements(By.CSS_SELECTOR, "li:not(.no-style) > a")
            if not page_links:
                return 1
            last_page_link = page_links[-1]
            last_page_href = last_page_link.get_attribute("href")
            last_page_number = int(last_page_href.split('=')[-1])
            return last_page_number
        except Exception as e:
            print(f"Помилка при отриманні кількості сторінок: {e}")
            return 1

    def get_all_pages_html(self) -> list[str]:
        html_pages = []
        num_pages = self.get_num_pages()
        for page in range(1, num_pages + 1):
            url = f"{self.url}?page={page}"
            self.driver.get(url)
            html_pages.append(self.driver.page_source)
        return html_pages

    def get_all_links(self, html_pages: list[str]) -> list[str]:
        links = set()
        for html in html_pages:
            page_soup = BeautifulSoup(html, "html.parser")
            div_vacancies = page_soup.find_all("div", class_="card")

            for div in div_vacancies:
                div_tag = div.find("h2", class_="my-0")
                if div_tag:
                    a_tag = div.find("a")
                    if a_tag and a_tag.get("href"):
                        full_url = "https://www.work.ua" + a_tag["href"]
                        links.add(full_url)
        return list(links)


class JobsDouScraper(BaseScraper):
    def __init__(self, url: str = JOB_SEARCH_DOU_UA, driver: WebDriver = None):
        if driver is None:
            driver = webdriver.Chrome()
        super().__init__(driver, url)
        self.soup: Optional[BeautifulSoup] = None

    def get_num_pages(self) -> int:
        self.driver.get(self.url)
        try:
            header = self.driver.find_element(By.CSS_SELECTOR, "div.b-inner-page-header")
            if not header:
                return 0
            h1 = header.find_element(By.CSS_SELECTOR, "h1")
            if not h1:
                return 0
            numbers = re.findall((r'\d+'), h1.text)
            return int(numbers[0] if numbers else 0)
        except Exception as e:
            print(f"Не вдалося визначити кількість сторінок: {e}")

    def get_all_pages_html(self) -> List[str]:
        html_pages = []
        self.driver.get(self.url)
        html_pages.append(self.driver.page_source)
        while True:
            try:
                button = self.driver.find_element(By.CSS_SELECTOR, "div.more-btn a")

                if not button.is_displayed():
                    break
                button.click()
                time.sleep(random.uniform(2, 3))
                html_pages.append(self.driver.page_source)

            except NoSuchElementException:
                print("Кнопка не знайдена. Завершення.")
                break

        return html_pages

    def get_all_links(self, html_pages: List[str]) -> List[str]:
        links = set()

        for html in html_pages:
            try:
                page_soup = BeautifulSoup(html, "html.parser")
                a_tags = page_soup.select("li.l-vacancy a.vt")

                for a_tag in a_tags:
                    href = a_tag.get("href")
                    if href:
                        links.add(href.strip())

            except Exception as e:
                print(f"Помилка при парсингу сторінки: {str(e)}")
                continue

        return list(links)

