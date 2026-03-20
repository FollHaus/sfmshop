from src.models.user import User
from src.models.order import Order
from src.models.product import Product
from src.models.payment import CardPayment, PayPalPayment
from src.models.exceptions import ValidationError, InvalidOrderError


def process_order_system():
    user = User("Ivan", "ivan@ivan.com")

    product1 = Product("Notebook", 50000, 2)
    product2 = Product("Mouse", 1500, 3)

    order = Order('1', 999999, user, [product1, product2])

    print(order)

    total = order.calculate_total()
    print("Общая стоимость заказа:", total)

    payments = [
        CardPayment(1111, "1234 3333 4444 9987"),
        PayPalPayment(2022, "ivan@paypal.com")
    ]

    for payment in payments:
        print(payment.process_payment())

    sort_products = sorted([product1, product2])
    for product in sort_products:
        print(product)

    try:
        product1.set_price(-1000)
    except ValidationError as e:
        print("Ошибка валидации:", e)

    try:
        user.set_email("invalid-email")
    except ValidationError as e:
        print("Ошибка валидации:", e)

    try:
        order.check_cart(Product("Toster", 1200, 3))
    except KeyError as e:
        print("Ошибка в заказе:", e)

    try:
        order2 = Order('2', 999999, user, [])
    except InvalidOrderError as e:
        print("Ошибка создания заказа", e)


if __name__ == "__main__":
    process_order_system()
