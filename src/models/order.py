from src.models.exceptions import InvalidOrderError, ValidationError
from src.models.product import Product
from src.models.user import User


class Order:
    def __init__(self, order_id: str, total: float, user: User, products: list[Product]):
        self.user: User = user
        self.order_id: str = order_id
        self.total: float = total
        self.products: list[Product] = products

        if not self.products:
            raise InvalidOrderError("Заказ невалиден: пустой список товаров")

    def calculate_total(self) -> float:
        """Подсчет суммы заказа."""
        orders_sum: float = 0.0

        for product in self.products:
            orders_sum += product.get_total_price()

        return orders_sum

    def add_product(self, product: Product):
        try:
            if not isinstance(product, Product):
                raise ValidationError("Неверный тип данных продукта")

            if product not in self.products:
                self.products.append(product)
                print(f"Товар \'{product.name}\' в корзину.")

        except ValidationError as e:
            print(f"Ошибка валидации:", e)

    def check_cart(self, product: Product):
        """Проверка наличия товара в корзине."""
        try:
            if product not in self.products:
                raise KeyError("Товар не найден")
        except KeyError as e:
            print("Ошибка при создании заказа:", e)
            self.add_product(product)

    def __str__(self):
        return f"Заказ #{self.order_id} на сумму {self.total} руб. (Пользователь: {self.user.name})"
