from src.models.exceptions import ValidationError


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self._email = email

    def set_email(self, email: str):
        if "@" not in email:
            raise ValidationError("Неверный формат email")
        self._email = email

    def get_email(self):
        return self._email if self._email else "Email не указан"

    def get_info(self) -> str:
        """Возвращает информацию о пользователе"""
        return f"Пользователь: {self.name}, Email: {self._email}"
