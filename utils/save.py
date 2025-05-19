import csv
import os
from dataclasses import asdict

from models.models import JobDetail


def save_to_file(vacancies: list[JobDetail]):
    output_path = os.path.abspath(r"G:\projects\scryping\python-technologies-statistics\data\processed\output.csv")
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["date", "title", "company", "location", "description", "link", "technologies"]
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
