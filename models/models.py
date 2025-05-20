from dataclasses import dataclass, field


@dataclass
class JobDetail:
    date: str
    title: str
    company: str
    location: str
    salary: str
    experience: list[str]
    description: str
    link: str
    technologies: list[str] = field(default_factory=list)
