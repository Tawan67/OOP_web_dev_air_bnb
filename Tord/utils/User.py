
import random


class User:
    count_id = 1

    def __init__(self, name, email, password):
        self.__user_id = User.count_id
        self.__user_name = name
        self.__email = email
        self.__password = password
        User.count_id += 1

    # @property
    # def get_payment_method(self):
    #     return self.__payment_methods

    # def add_payment_method(self, payment_method):
    #     if not isinstance(payment_method, PaymentMethod):
    #         return "Error: Invalid payment method"
    #     self.__payment_methods.append(payment_method)
    #     return "Success"

    def reset_increament(self):
        User.count_id = 1

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
    def get_password(self):
        return self.__password

    def __str__(self):
        return f"User ID: {self.__user_id}\nUser Name: {self.__user_name}\nEmail: {self.__email}"


class Member(User):
    def __init__(self, name, email, password, phone_num, age):
        super().__init__(name, email, password)
        self.__phone_num = phone_num
        self.__age = age
        self.__payment_method = []
        self.__my_coupons = []
        self.__booking_list = []
        self.__host = None

    def add_payment_method(self, payment_method):
        from .Payment import PaymentMethod
        if not isinstance(payment_method, PaymentMethod):
            return "Error"
        self.__payment_method.append(payment_method)
        return "Success"

    def add_coupon(self, input1):
        self.__my_coupons.append(input1)
        return "Success"

    def use_coupon(self, input1):
        self.__my_coupons.remove(input1)
        pass

    def add_booking(self, input1):
        self.__booking_list.append(input1)

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
    def get_payment_method_list(self):
        return self.__payment_method

    def search_cou_by_id(self, cou_id):
        for i in self.__my_coupons:
            if i.get_code == cou_id:
                return i
        return "Not found"

    def __str__(self):
        return super().__str__() + f", Payment Method: {[str(paymed) for paymed in self.__payment_method]}"

    def login(self, name, email, phone_num, password):
        if not (self.get_user_name == name or self.get_email == email):
            return "Wrong name or email", False
        if not (self.get_phone_num == phone_num):
            return "Wrong Phone Num", False
        if not (self.get_password == password):
            return "Wrong Password ", False
        return self.get_user_id, True


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
        from .Accommodation import Accommodation
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


class Coupon:
    used_codes = set()  # เก็บโค้ดที่ถูกสร้างไปแล้ว

    def __init__(self, discount=15):
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        self.__dis = discount
        self.__expiration_date = datetime.now() + relativedelta(months=6)
        self.__code = self.__generate_unique_code()

    def __generate_unique_code(self):
        """สร้างโค้ด 4 หลักที่ไม่ซ้ำ"""
        while True:
            new_code = f"{random.randint(1000, 9999)}"  # สร้างตัวเลข 4 หลัก
            if new_code not in Coupon.used_codes:
                Coupon.used_codes.add(new_code)
                return new_code

    @property
    def get_dis(self):
        return self.__dis

    @property
    def get_code(self):
        return self.__code

    @property
    def get_ex_date(self):
        return self.__expiration_date

    def use(self, price):
        import math
        dis = self.get_dis
        per_dis = dis/100
        total_price = math.ceil(price*(1-per_dis))
        return total_price
