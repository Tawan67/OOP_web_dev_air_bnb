class ControlSystem:

    pass


class User:
    count_id = 0

    def __init__(self, id, name, email, password):
        self.__user_id = id
        self.__user_name = name
        self.__email = email
        self.__password = password
        self.count_id += 1
    pass


class Member(User):
    def __init__(self, id, name, email, password, phone_num, age):
        super().__init__(id, name, email, password)
        self.__phone_num = phone_num
        self.__age = age
        self.__pay_med = None
        self.__my_coupon = []
    pass


class Host(User):
    def __init__(self, id, name, email, password, phone_num, age):
        super().__init__(id, name, email, password)
        self.__phone_num = phone_num
        self.__age = age
        self.__pay_med = None
        self.__my_acomadation = []
    pass


class Accomadation:
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


class Caledar:
    pass
