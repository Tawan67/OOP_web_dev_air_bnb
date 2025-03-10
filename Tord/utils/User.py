
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
        return super().__str__() + f", Payment Method: {[str(paymed) for paymed in self.__payment_method]}"
    



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
