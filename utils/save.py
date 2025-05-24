import csv
import os
from dataclasses import asdict
from config.technologies import ignore_experience_list
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
            # "description",
            "link",
            "technologies"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for vacancy in vacancies:
            row = asdict(vacancy)
            row["technologies"] = ", ".join(row.get("technologies", []))
            row.pop("technologies_by_category", None)
            writer.writerow(row)

    print(f"Дані збережено у файл: {output_path}")


def extract_technologies_by_category(title: str, description: str, tech_list: list[str]) -> list[str]:
    if not title and description:
        return []
    description_lower = description.lower()
    title_lower = title.lower()
    return [tech for tech in tech_list if tech.lower() in description_lower and title_lower]


@clean_input_text
def extract_experience(description: str, years_of_experience: list[str]) -> list[str]:
    if not description:
        return []
    description_lower = description.lower()
    found_experience = []

    for exp in years_of_experience:
        if exp in description_lower:
            possition = description_lower.find(exp.lower())
            start_position = max(0, possition - 50)
            preceding_text = description[start_position:possition]

            if any(phrase in preceding_text for phrase in ignore_experience_list):
                continue

            numbers = []
            for word in preceding_text.split():
                cleaned_word = word.strip("+,-")
                if cleaned_word.isdigit():
                    numbers.append(cleaned_word)

            if numbers:
                if len(numbers) >= 2:
                    found_experience.extend([min(numbers), max(numbers)])
                else:
                    found_experience.append(numbers[0])

    return list(set(found_experience)) if found_experience else []
