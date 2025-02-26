import math
from datetime import datetime
from dateutil.relativedelta import relativedelta  # to add a mount in period


class ControlSystem:
    def __init__(self):
        self.__booking_list = []
        self.__member_list = []
        self.__host_list = []
        self.__accommodation_list = []
        self.__paymentmethod = None

    @property
    def get_booking_list(self):
        return self.__booking_list

    @property
    def get_member_list(self):
        return self.__member_list

    @property
    def get_host_list(self):
        return self.__host_list

    @property
    def get_accommodation_list(self):
        return self.__accommodation_list

    def update_payment_method(self, input1):
        self.__paymentmethod = input1
        return "Success"

    def search_accom_by_id(self, accom_id):  # 1
        for i in self.__accommodation_list:
            if i.get_id == accom_id:
                return i
        return "Not Found"
        pass

    def create_booking(self, date, guest_amount, accom_id, price, menber_id):
        member = self.search_member_by_id(menber_id)
        accom = self.search_accom_by_id(accom_id)
        booking_item = Booking(accom=accom, date=date,
                               guess=guest_amount, member=member, amount=price)
        self.add_booking(booking_item)
        pass

    def create_account(self, name: str, email: str, password: str, phone: str, age: int):
        acount = Member(name=name, email=email,
                        password=password, phone_num=phone, age=age)
        self.add_member(acount)
        pass

    def cal_price_in_accom(self, accom_id, guest, start_date, end_date):
        accom = self.search_accom_by_id(accom_id=accom_id)
        price = accom.cal_price(guest, start_date, end_date)
        return price

        pass  # call func in Accomodation to cal total price

    def search_user_to_check(self, user_name, phone, email, password, age):
        for member in self.__member_list:
            if member.get_phone_num == phone and member.get_user_nane == user_name and member.get_email == email:
                return "You have an Account, Wanna Login?"
        try:
            self.create_account(name=user_name, email=email,
                                password=password, age=age)
            return "Success"
        except:
            return "Sign up Fail"
        pass  # search for check if user want to sign up

    def search_coupon_by_user_id(self, user_id):
        user = self.search_member_by_id(user_id)
        coupons = user.get_coupons
        result = self.show_coupon(coupons)
        return result

    def show_coupon(self, coupons):
        result = []
        for cou in coupons:
            if cou.check_expirat():
                result.append(cou.get_info())
        return result
        # for show all coupon on UI
        pass

    def create_payment(self, price, period, paymed, booking_id):
        booking_item = self.search_booking_by_id(booking_id=booking_id)
        payment = booking_item.create_payment(price, period, paymed)
        result = self.update_booking_pay(payment)
        return result
        pass  # call Booking to create

    def create_payment_med(self, details):
        details = "".join(i for i in details if i != '"')
        bank_id, user, balance, password = details.split(",")
        balance = int(balance)
        user = self.search_member_by_id(user)
        pay_med = Debit(bank_id, user, balance, password)
        return pay_med
        # key use
        # cal member to create and put on Booking after create
        pass

    def update_booking_payment(self, booking_id, payment):
        booking = self.search_booking_by_id(booking_id=booking_id)
        result = booking.update_payment(payment)
        # to put payment and pay_med into Booking
        pass

    def update_booking_pay_med(self, booking_id, paymed):
        booking = self.search_booking_by_id(booking_id=booking_id)
        result = booking.update_pay_med(paymed)
        return result
        pass
# update

    def search_member_by_id(self, id):
        for member in self.get_member_list:
            if user_id == member.get_user_id:
                return member
        return "cant find"

    def search_booking_by_user(self, user):
        if not isinstance(user, User):
            return "Error"
        all_booking = []
        for booking in self.get_booking_list:
            if user == booking.get_member:
                all_booking.append(booking)
        return all_booking

    def search_booking_by_id(self, booking_id):
        for booking in self.get_booking_list:
            if booking_id == booking.get_booking_id:
                return booking
        return "cant find"

    def search_host_by_accom(self, accom):
        if not isinstance(accom, Accommodation):
            return "Error"
        for host in self.get_host_list:
            for acc_in_host in host.get_accommodation:
                if accom == acc_in_host:
                    return host
        return "Cant find"

    def add_booking(self, booking):
        if not isinstance(booking, Booking):
            return "Error"
        else:
            self.__booking_list.append(booking)
            return "Success"

    def add_member(self, member):
        if not isinstance(member, User):
            return "Error"
        else:
            self.__member_list.append(member)
            return "Success"

    def add_host(self, host):
        if not isinstance(host, User):
            return "Error"
        else:
            self.__host_list.append(host)
            return "Success"

    def add_accommodation(self, accommodation):
        if not isinstance(accommodation, Accommodation):
            return "Error"
        else:
            self.__accommodation_list.append(accommodation)
            return "Success"


class User:
    count_id = 1

    def __init__(self, name, email, password):
        self.__user_id = User.count_id
        self.__user_name = name
        self.__email = email
        self.__password = password
        User.count_id += 1

    @property
    def get_user_id(self):
        return self.__user_id

    @property
    def get_user_name(self):
        return self.__user_name

    @property
    def get_email(self):
        return self.__email


class Member(User):
    def __init__(self, name, email, password, phone_num, age):
        super().__init__(name, email, password)
        self.__phone_num = phone_num
        self.__age = age
        self.__pay_med = None
        self.__my_coupons = []

    def update_payment_method(self, input1):
        self.__pay_med = input1
        return "Success"

    def add_coupon(self, input1):
        self.__my_coupons.append(input1)
        return "Success"

    def use_coupon(self, input1):
        pass

    @property
    def get_coupons(self):
        return self.__my_coupons

    @property
    def get_phone_num(self):
        return self.__phone_num

    @property
    def get_age(self):
        return self.__age

    @property
    def get_pay_med(self):
        return self.__pay_med


class Host(User):
    def __init__(self, name, email, password, phone_num, age):
        super().__init__(name, email, password)
        self.__phone_num = phone_num
        self.__age = age
        self.__pay_med = None
        self.__my_accommodation = []

    def update_payment_method(self, input1):
        self.__pay_med = input1
        return "Success"

    def add_accommodation(self, input1):
        if not isinstance(input1, Accommodation):
            return "Error"
        self.__my_accommodation.append(input1)
        return "Success"

    @property
    def get_phone_num(self):
        return self.__phone_num

    @property
    def get_age(self):
        return self.__age

    @property
    def get_accommodation(self):
        return self.__my_accommodation


class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def approve_accom(self, accom):
        pass


class Accommodation:
    count_id = 1

    def __init__(self, name, info, address):
        self.__info = info
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__status = False
        self.__accom_pics = []
        self.__booked_date = []
        Accommodation.count_id += 1

    def add_booked_date(self, booked_date) -> str:
        if not isinstance(booked_date, BookedDate):
            return "Error"
        self.__booked_date.append(booked_date)
        return "Success"

    def add_accom_pics(self, pic) -> str:
        self.__accom_pics.append(pic)
        return "Success"

    def update_status(self) -> str:
        self.__status = True
        return "Success"

    def del_booked_date(self, target):
        if not isinstance(target, BookedDate):
            return "Error"
        self.__booked_date.remove(target)
        return "Success"

    def cal_price(self, guest, start_date, end_date):
        pass

    @property
    def get_info(self):
        return self.__info

    @property
    def get_id(self):
        return self.__id

    @property
    def get_acc_name(self):
        return self.__accom_name

    @property
    def get_address(self):
        return self.__address

    @property
    def get_accom_pics(self):
        return self.__accom_pics

    @property
    def get_booked_date(self):
        return self.__booked_date


class House(Accommodation):
    def __init__(self, name, info, address, price):
        super().__init__(name, info, address)
        self.__price = price
        self.__my_calendar = []

    @property
    def get_price(self):
        return self.__price
# daaa


class Hotel(Accommodation):
    def __init__(self, name, address, info):
        super().__init__(name, address, info)
        self.__rooms = []

    def add_room(self, room):
        if not isinstance(room, Room):
            return "Error"
        else:
            self.__rooms.append(room)
            return "Success"


class Room:
    def __init__(self, room_id, room_floor, price):
        self.__room_id = room_id
        self.__room_floor = room_floor
        self.__price_per_day = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price_per_day


class House(Accommodation):
    def __init__(self, name, address, info, price):
        super().__init__(name, address, info)
        self.__price = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price


class Review:
    def __init__(self, rating: int, user: User, message):
        self.__rating = rating
        self.__user = user
        self.__message = message
        pass

    def get_info(self):
        pass


class Booking:
    count = 0

    def __init__(self, accom, booked_date, date, guess, member):
        self.__booking_id = Booking.count
        self.__accommodation = accom
        # self.__date = date วันที่ทำรายการจอง
        self.__booked_date = booked_date
        self.__date = date
        self.__amount = 0  # ราคาที่ต้องจ่าย
        self.__guess_amount = guess
        self.__booking_status = "Waiting"
        # self.__member = member เก็บ Member ทั้งก้อน
        self.__member = member
        # self.__payment เก็บ payment ทั้งก้อน
        # self.__pay_med เก็บ pay_med ทั้งก้อน
        self.__payment = None
        self.__pay_med = None
        Booking.count += 1

    @property
    def get_member(self):
        return self.__member

    @property
    def get_booking_id(self):
        return self.__booking_id

    @property
    def get_accommodation(self):
        return self.__accommodation

    @property
    def get_date(self):
        return self.__date

    @property
    def get_booked_date(self):
        return self.__booked_date

    @property
    def get_amount(self):
        return self.__amount

    @property
    def get_guess_amount(self):
        return self.__guess_amount

    @property
    def get_booking_status(self):
        return self.__booking_status

    @property
    def get_payment(self):
        return self.__payment

    @property
    def get_pay_med(self):
        return self.__pay_med

    def update_booking_status(self, input1):
        if not isinstance(input1, str):
            return "Wrong input"

        self.__booking_status = input1
        return "Succees"

    def update_payment(self, payment: 'Payment'):
        self.__payment = payment
        return "Success"
        pass

    def update_pay_med(self, pay_med: 'PaymentMethod'):
        self.__pay_med = pay_med
        return "Success"
        pass

    def create_payment(self, price, period, paymed):
        payment = Payment(period=period, pay_med=paymed, price=price)
        return payment


class BookedDate:
    def __init__(self, checkindate, checkoutdate):
        self.__checkindate = checkindate
        self.__checkoutdate = checkoutdate

    def get_checkindate(self):
        return self.__checkindate

    def get_checkoutdate(self):
        return self.__checkoutdate


class Payment:
    '''
        self.__status = False =====
        self.__periods = period =====  ก้อนหลายๆ ที่ต้องจ่าย
        self.__pay_med = pay_med ===== ช่องทางการจ่าย
        self.__pay_id = id ===== ไอดีไว้หา Payment
    '''
    count = 1

    def __init__(self, period, pay_med, price):
        self.__status = False
        self.__period_list = []
        self.__pay_med = pay_med
        self.__pay_id = Payment.count
        self.__interest = 5/100
        Payment.count += 1
        total = self.cal_interest(price, period)
        self.create_period(total, period)
        pass

    def cal_interest(self, price, period):
        total_price = price*pow((1+((self.__interest/12)*period)), period)
        total_price = math.ceil(total_price)
        return total_price
        pass

    def pay_time(self):

        pass

    def create_period(self, price, period):
        price_per_time = math.ceil(price/period)
        start_date = datetime.now()
        for p in range(period):
            new_date = start_date + relativedelta(months=p)
            pay_part = Period(price=price_per_time, date=start_date)
            self.__period_list.append(pay_part)
        return "Success"
        pass
    '''
        self.__status = False ===== ก้อนนี้จ่ายยัง
        self.__price = price ===== เงินที่ต้องจ่ายต่อรอบ
        self.__date = date ===== วันที่ต้องหักเงิน
    '''


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
    def __init__(self, bank_id, user, balance):
        self.__bank_id = bank_id
        self.__owner = user
        self.__balance = balance

    def pay(self, pray_tang):
        pass

    def get_bank_id(self):
        return self.__bank_id


"""
class Bank(PaymentMethod):
    def __init__(self, bank, user, balance):
        super().__init__(bank, user, balance)
    pass
"""


class Card(PaymentMethod):
    def __init__(self, bank_id, user, balance, password):
        super().__init__(bank_id, user, balance)
        self.__card_password = password
    pass


class Credit(Card):
    def __init__(self, bank_id, user, balance, password):
        super().__init__(bank_id, user, balance, password)
        self.__credit_point = 0
    pass


class Debit(Card):
    def __init__(self, bank_id, user, balance, password):
        super().__init__(bank_id, user, balance, password)
    pass


class Coupon:
    def __init__(self, coupon_id, coupon_name, percent_discount, expiration_date):
        self.__id = coupon_id
        self.__name = coupon_name
        self.__discount = percent_discount
        self.__expiration = expiration_date
        pass

    def get_info(self):
        id = self.__id
        name = self.__name
        result = {id: name}
        return result

    def check_expirat(self):

        if self.__expiration > datetime.now():
            return True
        return False


controlsystem = ControlSystem()

a = Member("Kant", "Kant@gmail.com", "1234", "123456789", 18)
b = Member("Hat", "Hat@gmail.com", "5678", "316420154", 19)
c = Member("Bat", "Bat@gmail.com", "1594", "754819624", 20)

d = Host("MMMMM", "MMMMM@gmail.com", "1234", "545678951", 50)

home1 = House("bannnn", "55 kokk road", "ee", 500)
home2 = House("sweethome", "407 kokk road", "ee", 1500)
home3 = House("whatislove", "330 kokk road", "eee", 20000)

controlpaymentmethod = Debit("1", controlsystem, 5000000, "54321")
controlsystem.update_payment_method(controlpaymentmethod)


print(a.get_user_id, a.get_email, a.get_phone_num, a.get_age)
print(b.get_user_id, b.get_email, b.get_phone_num, b.get_age)
print(c.get_user_id, c.get_email, c.get_phone_num, c.get_age)
print(d.get_user_id, d.get_email, d.get_phone_num, d.get_age)
print()
print(home1.get_id, home1.get_acc_name, home1.get_address, home1.get_price)
print(home2.get_id, home2.get_acc_name, home2.get_address, home2.get_price)
print(home3.get_id, home3.get_acc_name, home3.get_address, home3.get_price)

print("End")
