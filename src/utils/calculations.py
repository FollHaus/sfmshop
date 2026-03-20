def calculate_order_total(price: float, discount_rate: float) -> float:
    """
    Расчет цены со скиндкой
    :param price: Цена товара.
    :param discount_rate: Размер скидки (от 0.0 до 1.0).
    :return: Новая цена c учётом скидки.
    """
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Неверный размер скидки.")
    return round(price * (1 - discount_rate), 2)


def get_discount_by_total(total: float) -> float:
    """
    Расчёт размера скидки.
    :param total: Общая цена заказа.
    :return: Размер скидки.
    """
    if total <= 0:
        return 0

    if total >= 10_000:
        return 0.15
    elif total >= 5000:
        return 0.10
    else:
        return 0.05
