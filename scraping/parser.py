import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import scrapy
import logging
import csv


# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)',
#     handlers=[
#         logging.FileHandler('parser.log'),
#         logging.StreamHandler(sys.stdout),
#     ]
# )

class JobParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_total_vacancies(self) -> int:
        header = self.soup.find("div", class_="b-inner-page-header")
        if not header:
            return 0
        h1 = header.find("h1")
        if not h1:
            return 0
        numbers = re.findall((r'\d+'), h1.text)
        return int(numbers[0] if numbers else 0)

    def get_job_previews(self) -> list:
        vacancies = []
        li_vacancies = self.soup.find_all("li", class_="l-vacancy") + self.soup.find_all("li", class_="l-vacancy __hot")
        for li in li_vacancies:
            vacancy = {}
            date_tag = li.find("div", class_="date")
            vacancy["date"] = date_tag.text.strip()

            title_div = li.find("div", class_="title")
            if title_div:
                a_tag = title_div.find("a", class_="vt")
                vacancy["title"] = a_tag.text.strip()
                vacancy["link"] = a_tag["href"]
                company_tag = title_div.find("a", class_="company")
                vacancy["company"] = company_tag.text.strip()
                city_tag = title_div.find("span", class_="cities")
                vacancy["location"] = city_tag.text.strip()
                vacancies.append(vacancy)
            else:
                vacancy["title"] = vacancy["link"] = vacancy["company"] = vacancy["location"] = ""

        return vacancies

    def save_to_file(self, vacancies: list):
        output_path = os.path.abspath(r"G:\projects\scryping\python-technologies-statistics\data\processed\output.csv")
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["date", "title", "company", "link", "location"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(vacancies)

        print(f"Дані збережено у файл: {output_path}")


class JobDetailParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def extract_full_description(self) -> str:
        desc = self.soup.find("div", class_="vacancy-section")
        return desc.get_text(separator="\n").strip() if desc else ""
