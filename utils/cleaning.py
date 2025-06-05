import re
from models.models import JobDetail


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
                        if field == "title":
                            setattr(result, field, clean_title(value))
                        else:
                            setattr(result, field, clean_text(value))
        return result
    return wrapper


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    text = re.sub(r"[\u00A0\u2009\u202F\xa0]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_input_text(func):
    def wrapper(description, *args, **kwargs):
        description = clean_text(description)
        return func(description, *args, **kwargs)
    return wrapper


def clean_title(text: str) -> str:
    if not isinstance(text, str):
        return text

    text = re.sub(r"[\u00A0\u2009\u202F\xa0]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)

    text = re.sub(r"\s+([,.:;])", r"\1", text)
    text = re.sub(r"\s*-\s*", "-", text)

    return text
