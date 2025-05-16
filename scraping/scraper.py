import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from config.config import JOB_SEARCH_URL


class Scraper(object):
    def __init__(self, url=JOB_SEARCH_URL):
        self.url = url

    def all_pages(self):

        driver = webdriver.Chrome()
        driver.get(self.url)
        time.sleep(1)
        while True:
            try:
                button = driver.find_element(By.CSS_SELECTOR, "div.more-btn a")
                button.click()
                time.sleep(1)
                if not button.is_displayed():
                    break

            except NoSuchElementException:
                print("Кнопка не знайдена. Завершення.")
                break
        html = driver.page_source
        driver.close()
        return html
