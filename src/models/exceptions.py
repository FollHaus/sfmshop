class SFMShopException(Exception):
    """Базовый класс для всех исключений в магазине SFM."""
    pass


class ValidationError(SFMShopException):
    """Исключение для ошибок валидации."""
    pass


class BusinessLogicError(SFMShopException):
    """Исключение для ошибок бизнес-логики."""
    pass


class DatabaseError(SFMShopException):
    """Исключение для ошибок работы с базой данных."""
    pass


class NegativePriceError(ValidationError):
    """Исключение отрицательная цена товара."""
    pass


class InsufficientStockError(BusinessLogicError):
    """Исключение недостаточно товара на складе."""
    pass


class InvalidOrderError(BusinessLogicError):
    """Исключение невалидный заказ."""
    pass
