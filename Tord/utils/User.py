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

    def login(self, name, email, password):
        if not (self.get_user_name == name or self.get_email == email):
            return "Not Found", False
        if not (self.get_password == password):
            return "Not Found", False
        return self.get_user_id, True


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

    def __str__(self):
        return (
            super().__str__()
            + f", Payment Method: {[str(paymed) for paymed in self.__payment_method]}"
        )


class Host(User):
    def __init__(self, name, email, password, phone_num, age):
        super().__init__(name, email, password)
        self.__phone_num = phone_num
        self.__age = age
        self.__pay_med = None
        self.__payment_method = []
        self.__my_accommodation = []
        self.__booking_list = []

    def update_payment_method(self, input1):
        self.__pay_med = input1
        return "Success"

    def add_accommodation(self, input1):
        from .Accommodation import Accommodation

        if not isinstance(input1, Accommodation):
            return "Error"
        self.__my_accommodation.append(input1)
        return "Success"

    def add_payment_method(self, payment_method):
        from .Payment import PaymentMethod

        if not isinstance(payment_method, PaymentMethod):
            return "Error"
        self.__payment_method.append(payment_method)
        return "Success"

    def add_booking(self, input1):
        self.__booking_list.append(input1)

    @property
    def get_phone_num(self):
        return self.__phone_num

    @property
    def get_age(self):
        return self.__age

    @property
    def get_accommodation(self):
        return self.__my_accommodation

    def create_house(self, name, address, info, price):
        from .Accommodation import House

        a = House(name, address, info, price)
        self.add_accommodation(a)
        return a

    def create_hotel(self, name, address, info, rooms):
        from .Accommodation import Hotel

        a = Hotel(name, address, info)
        print(rooms)
        for room in rooms:
            a.add_room(room[1], room[0], address, name, room[2])

        self.add_accommodation(a)
        return a


class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def approve_accom(self, accom):
        pass
