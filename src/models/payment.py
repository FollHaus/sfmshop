class Payment:
    def __init__(self, amount: float):
        self.amount: float = amount

    def process_payment(self):
        raise NotImplementedError("Метод должен быть переопределен")


class CardPayment(Payment):
    def __init__(self, amount: float, card_number: str):
        super().__init__(amount)
        self.__card_number: str = card_number

    def process_payment(self) -> str:
        return f"Оплата картой **** {self.__card_number[-4:]}: {self.amount} руб."


class PayPalPayment(Payment):
    def __init__(self, amount: float, email: str):
        super().__init__(amount)
        self.email: str = email

    def process_payment(self) -> str:
        return f"Оплата PayPal ({self.email}): {self.amount} руб."
