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
    def __init__(self, name, address):
        self.__acc_name = name
        self.__address = address
        self.__accom_pic = []
        pass
    pass


class House(Accomadation):
    def __init__(self, name, address, price):
        super().__init__(name, address)
        self.__price = price
        self.__my_calendar = []
    pass


class Hotel(Accomadation):
    def __init__(self, name, address):
        super().__init__(name, address)
        self.__rooms = []

    def add_room(self):
        pass


class Room:
    def __init__(self, id, floor, price):
        self.__room_id = id
        self.__room_floor = floor
        self.__price_per_day = price
        self.__calendar = []
        pass


class Booking:
    count = 0

    def __init__(self, accom, date, amount, guess, member_id, payment, payment_med):
        self.__booking_id = self.count
        self.__accomadation = accom
        self.__date = date
        self.__amount = amount
        self.__guess_amount = guess
        self.__booking_status = False
        self.__member_id = member_id
        self.__payment = payment
        self.__pay_med = payment_med
        pass

    def update(self):
        pass
    pass


class Payment:
    def __init__(self, period, pay_med):
        self.__status = False
        self.__periods = period
        self.pay_med = pay_med
        pass
    pass


class Period:
    def __init__(self):
        pass
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
