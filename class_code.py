class ControlSystem:

    pass


class User:
    count_id = 0

    def __init__(self, id, name, phone_num, age):
        self.__user_id = id
        self.__user_name = name
        self.__user_phone_num = phone_num
        self.__user_age = age
        self.count_id += 1
    pass


class Member(User):
    def __init__(self, id, name, phone_num, age, payment_med=None):
        super().__init__(id, name, phone_num, age)
        self.__pay_med = payment_med
    pass


class Host(User):
    def __init__(self, id, name, phone_num, age, payment_med):
        super().__init__(id, name, phone_num, age)
        self.__pay_med = payment_med

    pass


class Booking:
    pass


class Payment:
    pass


class PaymentMethod:
    pass


class Bank(PaymentMethod):
    pass


class Card(PaymentMethod):
    pass


class Credit(Card):
    pass


class Debit(Card):
    pass


class Accomadation:
    pass


class Caledar:
    pass
