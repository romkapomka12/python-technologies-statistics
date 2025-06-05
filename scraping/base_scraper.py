from abc import ABC, abstractmethod
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver


class BaseScraper(ABC):
    def __init__(self, driver: WebDriver, url: str):
        self.driver = driver
        self.url = url

    @abstractmethod
    def get_all_pages_html(self):
        pass

    @abstractmethod
    def get_all_links(self, html_pages: list[str]) -> list[str]:
        pass
