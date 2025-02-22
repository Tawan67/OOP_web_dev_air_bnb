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
        self.count += 1
        pass

    def update(self):
        pass
    pass


class Payment:
    def __init__(self, period, pay_med, id):
        self.__status = False
        self.__periods = period
        self.__pay_med = pay_med
        self.__pay_id = id
        pass

    def pay_time(self):
        pass
    pass


class Period:
    def __init__(self, price, date):
        self.__status = False
        self.__price = price
        self.__date = date
        pass

    def update_status(self):
        new_status = not (self.__status)
        self.__status = new_status
    pass

    def get_price(self):
        return self.__price

    def check_date(self, date_check):
        if self.__date == date_check:
            return True
        return False


class PaymentMethod:
    def __init__(self, bank, user, balance):
        self.__bank_acc = bank
        self.__owner = user
        self.__ballance = balance
        pass
    pass


def pay(self, pray_tang):
    pass


class Bank(PaymentMethod):
    def __init__(self, bank, user, balance):
        super().__init__(bank, user, balance)
    pass


class Card(PaymentMethod):
    def __init__(self, bank, user, balance, id, password):
        super().__init__(bank, user, balance)
        self.__card_id = id
        self.__card_password = password
    pass


class Credit(Card):
    def __init__(self, bank, user, balance, id, password, point=0):
        super().__init__(bank, user, balance, id, password)
        self.__credit_point = point
    pass


class Debit(Card):
    def __init__(self, bank, user, balance, id, password):
        super().__init__(bank, user, balance, id, password)
    pass


class Caledar:
    def __init__(self, month, year):
        self.__month = month
        self.__year = year
        self.__booked_date = []
        pass

    def get_calendar(self):
        pass

    def update_date(self, date):
        pass
    pass
