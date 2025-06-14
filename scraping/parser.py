
from config.config import EXCHANGE_RATE
from models.models import JobDetail
from bs4 import BeautifulSoup
from config.technologies import technologies_dict, soft_skills_dict
from utils.cleaning import clean_fields
from utils.save import extract_technologies_by_category, extract_experience_by_dou_ua, extract_experience_by_work_ua, \
    convertation_salary_to_usd, is_salary_valid


@clean_fields
def parse_dou_ua_previews(link: str, html: str) -> JobDetail:
    soup = BeautifulSoup(html, "html.parser")

    title_elem = soup.find("h1", class_="g-h2")
    company_elem = soup.select_one("div.l-n > a")
    location_elem = soup.find("span", class_="place bi bi-geo-alt-fill")
    salary_elem = soup.find("span", class_="salary")
    description_elem = soup.find("div", class_="b-typo vacancy-section")
    date_elem = soup.find("div", class_="date")
    description = description_elem.get_text().strip() if description_elem else ""
    matched_techs = extract_technologies_by_category(description)
    matched_exp = extract_experience_by_dou_ua(description)

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

    salary_elem = (
            soup.select_one("li.text-indent > span.strong-500") or
            soup.select_one("li.text-indent > span.text-default-7")
    )
    salary_text = salary_elem.get_text(strip=True) if salary_elem else None

    if is_salary_valid(salary_text):
        converted_salary = convertation_salary_to_usd(salary_text, EXCHANGE_RATE)
    else:
        converted_salary = None

    experience_elem = soup.select_one('li:has(span[title="Умови й вимоги"])')
    experience = experience_elem.get_text() if experience_elem else ""
    matched_exp = extract_experience_by_work_ua(experience)

    date_elem = soup.select_one("ul.list-unstyled > li.no-style")
    tech_list_elem = soup.select_one("div.mt-2xl > ul.flex")
    tag_tech_and_soft_elem = [li.get_text(strip=True).lower() for li in tech_list_elem.select("li")] if tech_list_elem else []
    description = " ".join(tag_tech_and_soft_elem)
    extracted = extract_technologies_by_category(description)

    return JobDetail(
        title=title_elem.get_text(" ", strip=True) if title_elem else None,
        company=company_elem.get_text(strip=True) if company_elem else None,
        location=location_elem.next_sibling.strip() if location_elem else None,
        salary=converted_salary,
        experience=matched_exp,
        date=date_elem.get_text(strip=True) if date_elem else None,
        link=link,
        technologies=extracted
    )
