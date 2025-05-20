from models.models import JobDetail
from bs4 import BeautifulSoup
import re
from config.technologies import technologies_list, years_of_experience
from utils.save import extract_technologies_by_category, extract_experience


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

    def get_job_links(self) -> list[str]:
        links = []
        li_vacancies = (self.soup.find_all(
            "li", class_="l-vacancy") +
                        self.soup.find_all(
                            "li", class_="l-vacancy __hot")
                        )
        for li in li_vacancies:
            a_tag = li.find("a", class_="vt")
            if a_tag and a_tag.get("href"):
                links.append(a_tag["href"])
        return links


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    text = re.sub(r"[\u00A0\u2009\u202F\xa0]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_fields(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, JobDetail):
            for field in [
                'title',
                'company',
                'location',
                'salary',
                'experience',
                'description',
                'date',
                'link',
                'technologies'
            ]:
                if hasattr(result, field):
                    value = getattr(result, field)
                    if isinstance(value, str):
                        setattr(result, field, clean_text(value))
        return result

    return wrapper


@clean_fields
def parse_job_previews(link: str, html: str) -> JobDetail:
    soup = BeautifulSoup(html, "html.parser")

    title_elem = soup.find("h1", class_="g-h2")
    company_elem = soup.select_one("div.l-n > a")
    location_elem = soup.find("div", class_="sh-info")
    salary_elem = soup.find("span", class_="salary")
    description_elem = soup.find("div", class_="b-typo vacancy-section")
    date_elem = soup.find("div", class_="date")

    title = title_elem.get_text() if title_elem else ""
    description = description_elem.get_text() if description_elem else ""
    matched_techs = extract_technologies_by_category(title, description, technologies_list)
    matched_exp = extract_experience(description, years_of_experience)
    return JobDetail(

        title=title_elem.text.strip() if title_elem else None,
        company=company_elem.text.strip() if company_elem else None,
        location=location_elem.text.strip() if location_elem else None,
        salary=salary_elem.text.strip() if salary_elem else None,
        experience=matched_exp,
        description=description_elem.text.strip() if description_elem else None,
        date=date_elem.contents[0].text.strip() if date_elem else None,
        link=link,
        technologies=matched_techs,

    )
