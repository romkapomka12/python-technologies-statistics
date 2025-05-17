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
        fieldnames = ["date", "title", "company", "location", "description", "link"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for vacancy in vacancies:
            writer.writerow(asdict(vacancy))

    print(f"Дані збережено у файл: {output_path}")