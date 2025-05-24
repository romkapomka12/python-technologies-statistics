from models.models import JobDetail
from bs4 import BeautifulSoup
from config.technologies import technologies_list, years_of_experience
from utils.cleaning import clean_fields
from utils.save import extract_technologies_by_category, extract_experience


# class JobParser:
#     def __init__(self, html):
#         self.soup = BeautifulSoup(html, 'html.parser')


@clean_fields
def parse_dou_ua_previews(link: str, html: str) -> JobDetail:
    soup = BeautifulSoup(html, "html.parser")

    title_elem = soup.find("h1", class_="g-h2")
    company_elem = soup.select_one("div.l-n > a")
    location_elem = soup.find("span", class_="place bi bi-geo-alt-fill")
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
        date=date_elem.contents[0].text.strip() if date_elem else None,
        link=link,
        technologies=matched_techs,

    )


@clean_fields
def parse_work_ua_previews(link: str, html: str) -> JobDetail:
    soup = BeautifulSoup(html, "html.parser")

    title_elem = soup.select_one("h1.my-0")
    company_elem = soup.select_one("a span.strong-500")
    location_elem = soup.find('span', title=lambda t: t and "роботи" in t)
    salary_elem = soup.select_one("li.text-indent > span.strong-500")
    experience_elem = soup.select_one('li:has(span[title="Умови й вимоги"])')
    date_elem = soup.select_one("ul.list-unstyled > li.no-style")
    tech_list_elem = soup.select_one("div.mt-2xl > ul.flex")

    return JobDetail(
        title=title_elem.get_text(strip=True) if title_elem else None,
        company=company_elem.get_text(strip=True) if company_elem else None,
        location=location_elem.next_sibling.strip() if location_elem else None,
        salary=salary_elem.get_text(strip=True) if salary_elem else None,
        experience=experience_elem.get_text(strip=True) if experience_elem else None,
        date=date_elem.get_text(strip=True) if date_elem else None,
        link=link,
        technologies=[li.get_text(strip=True) for li in tech_list_elem.select("li")] if tech_list_elem else []
    )
