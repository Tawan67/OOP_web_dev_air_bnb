from fasthtml.common import *
from datetime import datetime, timedelta
from calendar import monthrange, weekday

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

    def search_accom_by_id(self, accom_id):
        for i in self.__accommodation_list:
            if i.get_id == accom_id:
                return i
        return "Not Found"


    def create_booking(self, accom, date, guess, member, check_in, check_out):
        # Check availability first
        if not self.check_accom_available(accom.get_id, check_in, check_out):
            return "Error: Accommodation not available for these dates"
        
        # Create the booking
        new_booking = Booking(accom=accom, date=date, guess=guess, member=member, check_in=check_in, check_out=check_out)
        self.add_booking(new_booking)
        
        # Add the booked dates to the accommodation
        # booked_date = BookedDate(check_in, check_out)
        # accom.add_booked_date(booked_date)
        return "Booking created successfully"

    def create_account(self):
        pass

    def cal_price_in_accom(self, accom_id, guest):
        pass  # call func in Accommodation to cal total price

    def search_user_by_id(self, user_id):
        pass  # search for check if user want to sign up

    def search_coupon_by_user_id(self, user_id):
        # for show all coupon on UI
        pass

    def create_payment(self):
        pass  # call Booking to create

    def create_payment_med(self):
        # cal member to create and put on Booking after create
        pass

    def update_booking_pay(self, Booking, Payment, PaymentMethod):
        # to put payment and pay_med into Booking
        pass

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

    def search_booking_by_id(self, booking_id):
        for booking in self.get_booking_list:
            if booking.get_id == booking_id:
                return booking 
            else:
                return "Not Found"
            
    def check_accom_available(self, accom_id, requested_check_in, requested_check_out):
        # Find the accommodation
        accom = self.search_accom_by_id(accom_id)
        if accom == "Not Found":
            return False

        # Check for overlap with existing booked dates
        for booked_date in accom.get_book_dates:
            existing_check_in = booked_date.get_checkindate()
            existing_check_out = booked_date.get_checkoutdate()

            # Overlap condition: if the requested range intersects with an existing range
            if (requested_check_in < existing_check_out) and (requested_check_out > existing_check_in):
                return False  # Not available
        return True  # Available

    def noti_host(self):
        pass

    def search_accom_detail(self, accom_id):
        pass

    def search_accommodation_by_id(self, accom_id):
        pass

    def search_host_by_accom(self, Accom):
        pass

class Accommodation:
    count_id = 1

    def __init__(self, name, address, info):
        self.__id = Accommodation.count_id
        self.__price = 0
        self.__accom_name = name
        self.__address = address
        self.__status = False
        self.__accom_pics = []
        self.__info = info
        self.__book_dates = []
        Accommodation.count_id += 1

    def add_accom_pics(self, pic):
        self.__accom_pics.append(pic)
        return "Success"
    
    def add_booked_date(self, date):
        self.__book_dates.append(date)
        return "Success"

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
    def get_price(self):
        return self.__price
    
    @property
    def get_book_dates(self):
        return self.__book_dates

class Payment:
    def __init__(self, period, pay_med, id):
        self.__status = False
        self.__period_list = period
        self.__pay_med = pay_med
        self.__pay_id = id

    def cal_price():
        pass

    def pay_time(self):
        pass

class PaymentMethod:
    def __init__(self, bank_id, user, balance):
        self.__id = bank_id
        self.__bank_id = bank_id
        self.__owner = user
        self.__balance = balance
        self.__point = 0

    @property
    def get_balance(self):
        return self.__balance
    
    @property
    def get_id(self):
        return self.__id
    
    @property
    def get_point(self):
        return self.__point

    def pay(self, pray_tang):
        self.__balance -= pray_tang
        self.__point += pray_tang/100
class User:
    count_id = 1

    def __init__(self, name, email, password):
        self.__user_id = User.count_id
        self.__user_name = name
        self.__email = email
        self.__password = password
        self.__payment_methods = []  # To store payment methods
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
    
    @property
    def get_payment_method(self):
        return self.__payment_methods

    def add_payment_method(self, payment_method):
        if not isinstance(payment_method, PaymentMethod):
            return "Error: Invalid payment method"
        self.__payment_methods.append(payment_method)
        return "Success"

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

# Define Booking class minimally since it's referenced
class Booking:
    count = 0

    def __init__(self, accom, date, guess, member, check_in, check_out):
        self.__booking_id = Booking.count
        self.__accommodation = accom
        # self.__date = date วันที่ทำรายการจอง
        self.__create_date = date
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
        self.__check_in = check_in
        self.__check_out = check_out
        Booking.count += 1

    @property
    def get_id(self): 
        return self.__booking_id
    
    @property
    def get_payment_method(self):
        return self.__pay_med

    @property
    def get_frequency(self):
        return self.__frequency
    
    @property
    def get_accommodation(self):
        return self.__accommodation

    @property
    def get_check_in(self):
        return self.__check_in
    
    @property
    def get_check_out(self):
        return self.__check_out
    
    @property   
    def get_guess(self):
        return self.__guess_amount
    
    @property
    def get_member(self):
        return self.__member
    
    def set_check_in(self, check_in):
        self.__check_in = check_in
        
    def set_check_out(self, check_out):
        self.__check_out = check_out

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

class House(Accommodation):
    def __init__(self, name, address, info, price):
        super().__init__(name, address, info)
        self.__price = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price

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

class Room(Accommodation):
    def __init__(self, room_id, room_floor, price, hotel_address, hotel_name): 
        super().__init__(
            name=f"Room {room_id}",
            address=f"{hotel_address} - Floor {room_floor}",
            info=f"Room in {hotel_name}"
        )
        self.__room_id = room_id
        self.__room_floor = room_floor
        self.__price_per_day = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price_per_day

class BookedDate:
    def __init__(self, checkindate, checkoutdate):
        self.__checkindate = checkindate
        self.__checkoutdate = checkoutdate

    def get_checkindate(self):
        return self.__checkindate

    def get_checkoutdate(self):
        return self.__checkoutdate

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
