import csv
import json
import os
import re
from dataclasses import asdict
from config.logger import logger
from config.technologies import technologies_dict, soft_skills_dict
from models.models import JobDetail
from utils.cleaning import clean_input_text


def save_to_file(vacancies: list[JobDetail]):
    output_path = os.path.abspath(r"G:\projects\scryping\python-technologies-statistics\data\processed\output.csv")
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "date",
            "title",
            "company",
            "location",
            "salary",
            "experience",
            "link",
            "technologies"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for vacancy in vacancies:
            row = asdict(vacancy)
            row["technologies"] = json.dumps(row.get("technologies", {"technologies": [], "soft_skills": []}),
                                             ensure_ascii=False)
            row.pop("technologies_by_category", None)
            writer.writerow(row)

    logger.info("Дані успішно збережено у %s", output_path)




def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\(\)\[\]\{\}\.,;:/\\\-_]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_technologies_by_category(
        description: str
) ->   dict[str, list[str]]:

    if not description:
        return {"technologies": [], "soft_skills": []}

    norm_description = normalize_text(description)

    def extract_from_dict(dictionary: dict[str, list[str]]) -> list[str]:
        found_techs = set()
        for category, keywords in dictionary.items():
            for keyword in keywords:
                norm_keyword = normalize_text(keyword)
                if " " in norm_keyword or "/" in norm_keyword or "-" in norm_keyword or "_" in norm_keyword:
                    if norm_keyword in norm_description:
                        found_techs.add(category)
                        break
                else:
                    pattern = r'\b' + re.escape(norm_keyword) + r'\b'
                    if re.search(pattern, norm_description):
                        found_techs.add(category)
                        break

        return sorted(found_techs)

    return {
        "technologies": extract_from_dict(technologies_dict),
        "soft_skills": extract_from_dict(soft_skills_dict)
    }



@clean_input_text
def extract_experience_by_dou_ua(description: str) -> int | None:
    if not description:
        return None

    description = description.lower()
    found_experience = set()

    if re.search(r"\b\d{1,2}(\.\d+)?\s+months?\s+of\s+experience\b", description):
        found_experience.add(1)

    for match in re.finditer(r"\b(\d{1,2}(?:\.\d+)?)\s*(–|-)\s*(\d{1,2}(?:\.\d+)?)\s+years?", description):
        try:
            min_years = float(match.group(1))
            found_experience.add(min_years)
        except ValueError:
            continue

    for match in re.finditer(
            r"\b(\d{1,2}(?:\.\d+)?)\+?\s+years?(?:\s+of)?(?:\s+(?:professional|commercial|hands-on))?\s+("
            r"?:experience|development)?",
            description):
        try:
            found_experience.add(float(match.group(1)))
        except ValueError:
            continue

    for match in re.finditer(r"\b(\d{1,2}(?:\.\d+)?)\+?\s+years\b", description):
        try:
            found_experience.add(float(match.group(1)))
        except ValueError:
            continue

    if not found_experience:
        return None

    return int(min(found_experience) + 0.5)


def extract_experience_by_work_ua(experience: str) -> int | None:
    if not experience:
        return None

    experience_lower = experience.lower()
    found_experience = []

    for word in experience_lower.split():
        cleaned_word = word.strip(",.:+ - ()")
        if cleaned_word.isdigit():
            found_experience.append(cleaned_word)
    return min(found_experience) if found_experience else None


def is_salary_valid(salary: str) -> bool:
    salary_lower = salary.lower()
    currency_signs = ["грн", "₴", "$", "usd"]

    return any(sign in salary_lower for sign in currency_signs)


def convertation_salary_to_usd(salary: str, EXCHANGE_RATE):
    if salary is None:
        return None

    clean_str = salary.strip().lower()
    clean_str = re.sub(r'\s+', '',clean_str).lower()


    if "$" in clean_str or "usd" in clean_str:
        return salary.strip()

    if "грн" in clean_str or "₴" in clean_str:
        numbers = [int(n) for n in re.findall(r'\d+', clean_str)]
        if not numbers:
            return None
        if len(numbers) == 1:
            usd = round(numbers[0] / EXCHANGE_RATE)
            return f"${usd}"
        else:
            min_usd = 50 * round((numbers[0] / EXCHANGE_RATE) / 50)
            max_usd = 50 * round((numbers[1] / EXCHANGE_RATE) / 50)
            return f"${min_usd}-{max_usd}"

    return None
