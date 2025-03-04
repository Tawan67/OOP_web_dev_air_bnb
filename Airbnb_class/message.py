import math
from datetime import datetime
from dateutil.relativedelta import relativedelta  # to add a mount in period
from fasthtml.common import *  # tord


class ControlSystem:
    def __init__(self):
        self.__booking_list = []
        self.__member_list = []
        self.__host_list = []
        self.__accommodation_list = []  # stored hotel, house
        self.__paymentmethod = None
        # self.__balance = None ไม่ควรมี เพราะ ค่านี้ควรอยู่ใน paymed

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

    def add_host(self, host):
        if not isinstance(host, User):
            return "Error"
        else:
            self.__host_list.append(host)  # t
            return "Success"

    def add_accommodation(self, accommodation):  # t
        if not isinstance(accommodation, Accommodation):
            return "Error"
        else:
            self.__accommodation_list.append(accommodation)
            return "Success"

    def update_payment_method(self, input1):  # tdkko
        self.__paymentmethod = input1
        return "Success"

    # def search_member_by_id(self, id):
    #     for member in self.get_member_list:
    #         if id == member.get_user_id:
    #             return member, id
    #     return "cant find"

    def add_booking(self, booking):
        if not isinstance(booking, Booking):
            return "Error"
        else:
            self.__booking_list.append(booking)
            return "Success"

    def add_member(self, member):  # k0
        if not isinstance(member, User):
            return "Error"
        else:
            self.__member_list.append(member)
            return "Success"

    def search_member_by_id(self, user_id):
        for member in self.get_member_list:
            if user_id == member.get_user_id:
                return member
        return "cant find"

    def search_accom_by_id(self, accom_id):  # 1
        for i in self.__accommodation_list:
            if i.get_id == accom_id:
                return i
        return "Not Found"
# ----------------------------------------------- downnnnnnnn

    def create_booking(self, accom, date, guess, member, check_in, check_out):
        # Check availability first
        if not self.check_accom_available(accom.get_id, check_in, check_out):
            return "Error: Accommodation not available for these dates"

        # Create the booking
        new_booking = Booking(accom=accom, date=date, guess=guess,
                              member=member, check_in=check_in, check_out=check_out)
        self.add_booking(new_booking)

        # Add the booked dates to the accommodation
        # booked_date = BookedDate(check_in, check_out)
        # accom.add_booked_date(booked_date)
        return "Booking created successfully"
# ---------------------------------------------------

    def create_booking(self, date, guest_amount, accom_id, price, menber_id):
        member = self.search_member_by_id(menber_id)
        accom = self.search_accom_by_id(accom_id)
        booking_item = Booking(accom=accom, date=date,
                               guess=guest_amount, member=member, amount=price)
        self.add_booking(booking_item)
        pass
# --------------------------------------------------^^^^^^^

    def search_booking_by_user(self, user):
        if not isinstance(user, User):
            return "Error"
        all_booking = []
        for booking in self.get_booking_list:
            if user == booking.get_member:
                all_booking.append(booking)
        return all_booking

    # ----------------------------------------------=tord1 downnnnnnnn

    def search_accommodations(self, query):
        # If there's no search term, show everything
        if not query:
            return self.get_accommodation_list

        # Make the search term lowercase so we can match without worrying about capital letters
        search_term = query.lower()

        # Create an empty list to store our matching results
        matching_accommodations = []

        # Look at each accommodation one by one
        for accommodation in self.get_accommodation_list:
            # Get the name and address in lowercase
            name = accommodation.get_acc_name.lower()
            address = accommodation.get_address.lower()

            # Check if our search term is in the name OR address
            if search_term in name or search_term in address:
                # If we found a match, add it to our results
                matching_accommodations.append(accommodation)

        # Give back all the matches we found
        return matching_accommodations
    # ----------------------------------------------=tord1 ^^^^^^^^^

    def search_booking_by_id(self, booking_id):
        for booking in self.get_booking_list:
            if booking_id == booking.get_booking_id:
                return booking
        return "cant find"

    def create_account(self, name: str, email: str, password: str, phone: str, age: int):  # dew
        acount = Member(name=name, email=email,
                        password=password, phone_num=phone, age=age)
        self.add_member(acount)
        pass

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
# ---------------------------------------------- cal toartal price

    def cal_price_in_accom(self, accom_id, guest, start_date, end_date):
        accom = self.search_accom_by_id(accom_id=accom_id)
        price = accom.cal_price(guest, start_date, end_date)
        return price
# -----------------------------------------------

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
# -----------------------------------------------------

    def search_host_by_accom(self, accom):
        if not isinstance(accom, Accommodation):
            return "Error"
        for host in self.get_host_list:
            for acc_in_host in host.get_accommodation:
                if accom == acc_in_host:
                    return host
        return "Not Found"
    # get accom detail

    def search_accom_detail(self, accom_id):
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

    def search_host_by_id(self, user_id):
        for host in self.__host_list:
            if host.get_user_id == user_id:
                return host.get_host_name
        pass

    def search_user_to_check(self, user_name, phone, email, password, age):  # dew not sure
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

    # korn does it really needed?
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

    def search_host_by_id_get_review(self, user_id):  # korn
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

    def create_payment(self, price, period, paymed, booking_id):
        booking_item = self.search_booking_by_id(booking_id=booking_id)
        payment = booking_item.create_payment(price, period, paymed)
        result = self.update_booking_pay(payment)
        return result
        pass  # call Booking to create

    def create_payment_med(self, details):
        details = "".join(i for i in details if i != '"')
        card_id, user, balance, password = details.split(",")
        balance = int(balance)
        user = self.search_member_by_id(user)
        pay_med = Debit(card_id, user, balance, password)
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


class User:
    count_id = 1

    def __init__(self, name, email, password):
        self.__user_id = User.count_id
        self.__user_name = name
        self.__email = email
        self.__password = password
        # self.__payment_methods = []  # To store payment methods
        User.count_id += 1

    # @property
    # def get_payment_method(self):
    #     return self.__payment_methods

    # def add_payment_method(self, payment_method):
    #     if not isinstance(payment_method, PaymentMethod):
    #         return "Error: Invalid payment method"
    #     self.__payment_methods.append(payment_method)
    #     return "Success"

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

    def __init__(self, name, address, info, price):
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__info = info
        self.__price = price
        self.__status = False
        self.__accom_pics = []
        self.__booked_date = []
        self.__reviews = []
        Accommodation.count_id += 1

    def add_booked_date(self, booked_date) -> str:
        if not isinstance(booked_date, BookedDate):
            return "Error"
        self.__booked_date.append(booked_date)
        return "Success"

    def del_booked_date(self, target):
        if not isinstance(target, BookedDate):
            return "Error"
        self.__booked_date.remove(target)
        return "Success"

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

    def add_host(self, host):
        if not isinstance(host, Host):
            return "Error"
        else:
            self.__host = host
            return "Success"

# ------------------------------------------------------------------
    def cal_price(self, start_date, end_date):
        # Convert HTML date strings (e.g., "2025-03-01") to datetime objects
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        # Calculate the difference in days
        day_count = (end - start).days

        # Ensure day_count is positive and makes sense
        if day_count <= 0:
            return "Error: End date must be after start date"

        # Calculate total price
        total_price = (day_count+1) * self.__price
        return total_price
# ----------------------------------------------------------------------

    def get_price_accom(self, start_date, end_date, guest_amount):
        day_between = (end_date - start_date).days
        total_price = (day_between + 1) * self.get_price
        fee = (total_price * 5 / 100) * guest_amount
        total_price = total_price + fee
        return total_price

# -----------------------------------------------------------------------------

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

    @property
    def get_reviews(self):
        return self.__reviews


class House(Accommodation):
    def __init__(self, name, address, info, price):
        super().__init__(name, address, info, price)


class Hotel(Accommodation):
    def __init__(self, name, address, info):
        super().__init__(name, address, info, price=0)
        self.__rooms = []

    def add_room(self, room):
        if not isinstance(room, Room):
            return "Error"
        else:
            self.__rooms.append(room)
            return "Success"

    def cal_price(self, start_date, end_date):
        price_list = []
        for room in self.__rooms:
            price = room.cal_price(start_date, end_date)
            price_list.append(price)
        return price_list

    @property
    def get_price(self):
        price_list = []
        for x in self.__rooms:
            price_list.append(x.get_price)
        return price_list

    @property
    def get_rooms(self):
        return self.__rooms


class Room(Accommodation):
    def __init__(self, room_id, room_floor, price, hotel_address, hotel_name):
        # FIXME:
        super().__init__(
            name=f"Room {room_id}",
            address=f"{hotel_address} - Floor {room_floor}",
            info=f"Room in {hoteln_ame}",
            price=price
        )
        self.__room_id = room_id
        self.__room_floor = room_floor
        self.__booked_date = []

    # def get_price_accom(self, start_date, end_date, guest_amount):
    #     num_days = (end_date - start_date).days
    #     return num_days * self.__price_per_day


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
        self.__booked_date = None
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
    def __init__(self, user, checkindate, checkoutdate):
        self.__checkindate = checkindate
        self.__checkoutdate = checkoutdate

    def get_checkindate(self):
        return self.__checkindate

    def get_checkoutdate(self):
        return self.__checkoutdate


class Payment:

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

    # def __init__(self, period, pay_med, id): tord2
    #     self.__status = False
    #     self.__period_list = period
    #     self.__pay_med = pay_med
    #     self.__pay_id = id

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


class PaymentMethod:
    def __init__(self, bank_id, user, balance):
        self.__bank_id = bank_id
        self.__owner = user
        self.__balance = balance

    def get_bank_id(self):
        return self.__bank_id

    def pay(self, pray_tang):
        self.__balance -= pray_tang
        self.__point += pray_tang/100


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
