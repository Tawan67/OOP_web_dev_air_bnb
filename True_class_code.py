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

    def search_member_by_id(self, user_id):
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


class Hotel(Accommodation):
    def __init__(self, name, info, address):
        super().__init__(name, info, address)
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
        self.__calendar = []


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

    def update_payment(self, input1):
        pass

    def update_pay_med(self, input1):
        pass


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


# Create an instance of ControlSystem
control_system = ControlSystem()

# Create Members
member1 = Member("Alice", "alice@example.com", "pass123", "123456789", 25)
member2 = Member("Bob", "bob@example.com", "secure456", "987654321", 30)

# Create Hosts
host1 = Host("Charlie", "charlie@example.com", "hostpass", "555555555", 40)
host2 = Host("David", "david@example.com", "host4321", "666666666", 35)

# Create Admin
admin1 = Admin("Eve", "eve@example.com", "admin123")

# Create Accommodations (Houses and Hotels)
house1 = House("Villa Paradise", "Luxury villa with sea view",
               "123 Beach Road", 500)
house2 = House("Cozy Cabin", "Small cabin in the woods",
               "456 Forest Lane", 100)

hotel1 = Hotel("Grand Hotel", "5-star hotel in downtown", "789 City Center")
hotel2 = Hotel(
    "Budget Inn", "Affordable stay with great service", "321 Main Street")

# Add accommodations to hosts
host1.add_accommodation(house1)
host1.add_accommodation(hotel1)
host2.add_accommodation(house2)
host2.add_accommodation(hotel2)

# Create Rooms for Hotels
room1 = Room("101", "1st Floor", 200)
room2 = Room("202", "2nd Floor", 300)
room3 = Room("303", "3rd Floor", 150)

hotel1.add_room(room1)
hotel1.add_room(room2)
hotel2.add_room(room3)

# Create Booked Dates
booked_date1 = BookedDate("2025-03-01", "2025-03-10")
booked_date2 = BookedDate("2025-06-15", "2025-06-20")

# Create Bookings
booking1 = Booking(house1, booked_date1, "2025-02-20", 4, member1)
booking2 = Booking(hotel1, booked_date2, "2025-07-10", 2, member2)
# booking1 status = Waiting
# booking2 status = Preserved
booking2.update_booking_status("Preserved")

# เพิ่ม booked_date2 ลงใน accommodation hotel1
hotel1.add_booked_date(booked_date2)

# Create Payment Methods
payment_method1 = Credit("11112222", member1, 5000, "1234")
payment_method2 = Debit("33334444", member2, 3000, "5678")

member1.update_payment_method(payment_method1)
member2.update_payment_method(payment_method2)

# Create Payments and Periods
period1 = Period(500, "2025-02-25")
period2 = Period(700, "2025-07-15")

payment1 = Payment([period1], payment_method1, "P12345")
payment2 = Payment([period2], payment_method2, "P67890")

# Update Booking Payment Details
booking1.update_payment(payment1)
booking1.update_pay_med(payment_method1)

booking2.update_payment(payment2)
booking2.update_pay_med(payment_method2)

# Add everything to ControlSystem
control_system.add_member(member1)
control_system.add_member(member2)

control_system.add_host(host1)
control_system.add_host(host2)

control_system.add_accommodation(house1)
control_system.add_accommodation(house2)
control_system.add_accommodation(hotel1)
control_system.add_accommodation(hotel2)

control_system.add_booking(booking1)
control_system.add_booking(booking2)

# Set ControlSystem's payment method
control_payment_method = Debit("99995555", control_system, 100000, "adminpass")
control_system.update_payment_method(control_payment_method)


# Test 1 ยกเลิก Booking when booking_status = Waiting
print(f"status booking1 = {booking1.get_booking_status}")
print(f"ถ้า print ออกมาแสดงว่ายังมีอยู่ {house1.get_booked_date}")

booking1.update_booking_status("Cancel")
print(f"หลังจากกดยกเลิก")
print(f"status booking1 = {booking1.get_booking_status}")
