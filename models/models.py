from dataclasses import dataclass, field


@dataclass
class JobDetail:
    date: str
    title: str
    company: str
    location: str
    salary: str | None
    experience: int | None
    link: str
    technologies: dict[str, list[str]]
