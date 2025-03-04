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
        self.__balance = None

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

    def search_member_by_id(self, id):
        for member in self.get_member_list:
            if id == member.get_user_id:
                return member, id
        return "cant find"

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

    def check_accom_available(self, booking_id):
        pass

    def noti_host(self):
        pass

    # get accom detail
    def search_accom_detail(self, accom_id):  #####
        accommodation = self.search_accomodation_by_id(accom_id)
        if accommodation == "Not Found":
            return "Accommodation not found"

        host = self.search_host_by_accom(accommodation)
        if host == "Not Found":
            return "Host not found"
        host_name = host.get_user_name
        accom_name = accommodation.get_acc_name
        accom_address = accommodation.get_address
        accom_info = accommodation.get_info
        accom_list_pic = accommodation.get_accom_pics
        # show occupied date of that accom to user
        occupied_dates = []
        for booking in self.__booking_list:
            if booking.get_accommodation == accommodation:
                booking_date = booking.get_booking_date
                occupied_dates.append(
                    (booking_date.get_checkin_date, booking_date.get_checkout_date)
                )

        return (
            accom_name,
            host_name,
            accom_address,
            accom_info,
            accom_list_pic,
            occupied_dates,
        )
        pass

    def search_accomodation_by_id(self, accom_id):
        for accom in self.__accommodation_list:
            if accom.get_id == accom_id:
                return accom
        return "Not Found"

        pass

    # get host name
    def search_host_by_id(self, user_id):
        for host in self.__host_list:
            if host.get_user_id == user_id:
                return host.get_host_name
        pass

    # get my accomodation
    def search_host_by_id_get_accom(self, user_id):
        that_host = None
        for host in self.__host_list:
            if host.get_user_id == user_id:
                that_host = host
                break
        if that_host is None:
            return "Host Not Found"
        my_accom_list = that_host.get_accommodation
        accom_list = [
            {"name": myaccom.get_acc_name, "address ": myaccom.get_address}
            for myaccom in my_accom_list
        ]
        return accom_list

    # get review of my acccom
    def search_host_by_id_get_review(self, user_id):
        that_host = None
        for host in self.__host_list:
            if host.get_user_id == user_id:
                that_host = host
                break
        if that_host is None:
            return "Host Not Found"

        my_accom_list = that_host.get_accommodation
        review_list = []
        for accom in my_accom_list:
            for review in accom.get_reviews:
                review_list.append(
                    {
                        "accommodation": accom.get_acc_name,
                        "rating": review.get_rating,
                        "user": review.get_user.get_user_name,
                        "message": review.get_message,
                    }
                )
        return review_list

    def search_host_by_accom(self, accom):
        if not isinstance(accom, Accommodation):
            return "Error"
        for host in self.get_host_list:
            for acc_in_host in host.get_accommodation:
                if accom == acc_in_host:
                    return host
        return "Not Found"
        pass

    # get total price of House and Hotel
    def find_total_price(self, accom_id, start_date, end_date, guest_amount):
        accommodation = self.search_accomodation_by_id(accom_id)
        if isinstance(accommodation, House):
            total_price = accommodation.get_price_accom(
                start_date, end_date, guest_amount
            )
            return total_price
        elif isinstance(accommodation, Hotel):
            for room in accommodation.get_rooms:
                if room.get_id == accom_id:
                    return room.get_price_accom(start_date, end_date, guest_amount)
        return None

        # if isinstance(accommodation,Hotel):

    def get_calender(self):

        pass


class User:
    count_id = 1

    def __init__(self, name, email, password):
        self.__user_id = User.count_id
        self.__user_name = name
        self.__email = email
        self.__password = password
        User.count_id += 1

    @property
    def user_id(self):
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

    def create_coupon(self):
        pass

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
        self.__my_accommodation = input1
        return "Success"

    def get_my_accommodation(self, Host):
        pass

    @property
    def get_phone_num(self):
        return self.__phone_num

    @property
    def get_age(self):
        return self.__age

    @property
    def get_host_name(self):
        return self.__user_name

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

    def __init__(self, name, address, info, price):
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__info = info
        self.__price = price
        self.__status = False
        self.__accom_pics = []
        self.__reviews = []
        Accommodation.count_id += 1

    def add_accom_pics(self, pic) -> str:
        self.__accom_pics.append(pic)
        return "Success"

    def update_status(self) -> str:
        self.__status = True
        return "Success"

    def add_review(self, review):
        if isinstance(review, Review):
            self.__reviews.append(review)
            return "Success"
        return "Invalid Review"

    def update_calendar(self):
        pass

    def calculate(self, adult, children, pet):
        pass

    def sort_dates_list(self, dates_list):
        pass

    # def get_accom_detail(self,Accommodation):
    #     #get accom_name,address,accom_pic
    #     #return accom_detail,sorted_date

    #     pass

    def get_price_accom(self, start_date, end_date, guest_amount):
        day_between = (end_date - start_date).days
        total_price = (day_between + 1) * self.get_price
        fee = (total_price * 5 / 100) * guest_amount
        total_price = total_price + fee
        return total_price

    def cal_total_price(self):

        pass

    def get_review(self, Accommodation):

        pass

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
    def get_info(self):
        return self.__info

    @property
    def get_reviews(self):
        return self.__reviews

    @property
    def get_price(self):
        return self.__price


class House(Accommodation):
    def __init__(self, name, address, price):
        super().__init__(name, address, "House Info", price)
        self.__price = price
        self.__my_calendar = []

    @property
    def get_price(self):
        return self.__price


class Hotel(Accommodation):
    def __init__(self, name, address):
        super().__init__(name, address, "Hotel Info", 0)
        self.__rooms = []

    def add_room(self, room):
        if not isinstance(room, Room):
            return "Error"
        else:
            self.__rooms.append(room)
            return "Success"

    @property
    def get_rooms(self):
        return self.__rooms


class Room(Accommodation):
    def __init__(self, name, address, room_id, room_floor, price):
        super().__init__(name, address, "Room info", price)
        self.__room_id = room_id
        self.__room_floor = room_floor
        self.__price_per_day = price
        self.__calendar = []

    @property
    def get_room_price(self):
        return self.__price_per_day

    @property
    def get_id(self):
        return self.__room_id

    def get_price_accom(self, start_date, end_date, guest_amount):
        num_days = (end_date - start_date).days
        return num_days * self.__price_per_day


class Review:
    def __init__(self, rating: int, user: User, message):
        self.__rating = rating
        self.__user = user
        self.__message = message
        pass

    def get_info(self):
        return f"Review by {self.__user.get_user_name}: {self.__rating}/5 - {self.__message}"

    @property
    def get_rating(self):
        return self.__rating

    @property
    def get_user(self):
        return self.__user

    @property
    def get_message(self):
        return self.__message


class Booking:
    count = 0

    def __init__(self, accom, date, guess, member):
        self.__booking_id = Booking.count
        self.__accommodation = accom
        # self.__date = date วันที่ทำรายการจอง
        self.__date = date
        self.__amount = 0  # ราคาที่ต้องจ่าย
        self.__guess_amount = guess
        self.__booking_status = False
        # self.__member = member เก็บ Member ทั้งก้อน
        self.__member = member
        # self.__payment เก็บ payment ทั้งก้อน
        # self.__pay_med เก็บ pay_med ทั้งก้อน
        self.__payment = None
        self.__pay_med = None
        self.__frequency = None
        Booking.count += 1

    # for get book date func
    @property
    def get_accommodation(self):
        return self.__accommodation

    @property
    def get_booking_date(self):
        return self.__date

    @property
    def get_payment_method(self):
        return self.__pay_med

    @property
    def get_frequency(self):
        return self.__frequency

    def update_booking_status(self, input1):
        pass

    def update_payment(self, input1):
        pass

    def update_pay_med(self, input1):
        pass

    def verify_booked_date(self):
        pass

    def update_date(self, start_date, end_date):
        pass

    def update_guest(self):
        pass

    def get_amount(self):
        return self.__amount

    def discount_by_coupon(self):
        pass


class Payment:
    """
    self.__status = False =====
    self.__periods = period =====  ก้อนหลายๆ ที่ต้องจ่าย
    self.__pay_med = pay_med ===== ช่องทางการจ่าย
    self.__pay_id = id ===== ไอดีไว้หา Payment
    """

    def __init__(self, period, pay_med, id):
        self.__status = False
        self.__period_list = period
        self.__pay_med = pay_med
        self.__pay_id = id
        pass

    def cal_price():
        pass

    def pay_time(self):
        pass

    """
        self.__status = False ===== ก้อนนี้จ่ายยัง
        self.__price = price ===== เงินที่ต้องจ่ายต่อรอบ
        self.__date = date ===== วันที่ต้องหักเงิน
    """


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


class BookingDate:
    def __init__(self, user, checkin_date, checkout_date):
        self.__user = user
        self.__checkin_date = checkin_date
        self.__checkout_date = checkout_date

    @property
    def get_checkin_date(self):
        return self.__checkin_date

    @property
    def get_checkout_date(self):
        return self.__checkout_date

    def get_bookdate(self):
        pass

    def cal_date_period(self):
        pass

    pass


class Card(PaymentMethod):
    def __init__(self, bank_id, user, balance, password):
        super().__init__(bank_id, user, balance)
        self.__card_password = password
        pass

    def pluspoint(self, point):
        pass


class Credit(Card):
    def __init__(self, bank_id, user, balance, password, point=0):
        super().__init__(bank_id, balance, password)
        self.__credit_point = point

    pass


class Debit(Card):
    def __init__(self, bank_id, user, balance, password):
        super().__init__(bank_id, user, balance, password)

    pass


controlsystem = ControlSystem()

a = Member("Kant", "Kant@gmail.com", "1234", "123456789", 18)
b = Member("Hat", "Hat@gmail.com", "5678", "316420154", 19)
c = Member("Bat", "Bat@gmail.com", "1594", "754819624", 20)

d = Host("MMMMM", "MMMMM@gmail.com", "1234", "545678951", 50)

home1 = House("bannnn", "55 kokk road", 500)
home2 = House("sweethome", "407 kokk road", 1500)
home3 = House("whatislove", "330 kokk road", 20000)

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
