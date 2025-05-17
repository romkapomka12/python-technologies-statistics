from dataclasses import dataclass


@dataclass
class JobDetail:
    date: str
    title: str
    company: str
    location: str
    description: str
    link: str
