from src.models.exceptions import ValidationError


class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name: str = name
        self.price: float = price
        self.quantity: int = quantity

        if quantity < 0:
            raise ValidationError("Количество не может быть отрицательным")
        self.quantity = quantity

    def set_price(self, price):
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self.price = price

    def check_stock(self):
        pass

    def update_stock(self, quantity):
        pass

    def get_total_price(self) -> float:
        """Возвращает общую стоимость товара"""
        return self.price * self.quantity

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __str__(self):
        return f"{self.name}, Цена: {self.price}, Количество: {self.quantity}"

    def __repr__(self):
        return f"Product('{self.name}', {self.price}, {self.quantity})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price
