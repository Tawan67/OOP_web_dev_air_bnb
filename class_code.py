class ControlSystem:

    pass


class User:
    count_id = 0

    def __init__(self, id, name, phone_num, age, payment_med):
        self.__user_id = id
        self.__user_name = name
        self.__user_phone_num = phone_num
        self.__user_age = age
        self.__user_payment_methhod = payment_med
    pass


class Member(User):
    pass


class Host(User):
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
