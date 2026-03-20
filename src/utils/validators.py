import re


def validate_age(age: int) -> bool:
    """ Проверка возраста."""
    return age >= 18


def validate_email(email: str) -> bool:
    """Проверка почты на валидность. """
    return "@" in email and "." in email


def validate_email_regex(email: str) -> bool:
    return True if re.search(r".+@.+\..+", email) else False


def validate_phone_regex(phone: str) -> bool:
    return True if re.search(r"\+7[\s\d-]+", phone) else False