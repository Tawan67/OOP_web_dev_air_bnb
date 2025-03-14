from datetime import datetime


class Booking:
    id = 1

    def __init__(self, accom, guess, member):
        self.__booking_id = Booking.id
        self.__accommodation = accom
        # self.__date = date วันที่ทำรายการจอง
        self.__booked_date = None
        self.__date = datetime.now()
        self.__amount = 0  # ราคาที่ต้องจ่าย
        self.__guess_amount = guess
        self.__booking_status = "Waiting"
        # self.__member = member เก็บ Member ทั้งก้อน
        self.__member = member
        # self.__payment เก็บ payment ทั้งก้อน
        # self.__pay_med เก็บ pay_med ทั้งก้อน
        self.__payment = None
        self.__pay_med = None
        self.__price = None
        self.__coupon = None
        Booking.id += 1

    # dew
    @property
    def reset_id(self):
        Booking.count = 1
        return "Success reset"

    def reset_increment(self):
        Booking.id = 1

    def set_status(self, status):
        self.__booking_status = status
        return "Success"

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

    @property
    def get_cou(self):
        return self.__coupon

    def update_booking_status(self, input1):
        if not isinstance(input1, str):
            return "Wrong input"

        self.__booking_status = input1
        return "Succees"

    def update_payment(self, payment):
        from .Payment import Payment
        isinstance(payment, Payment)
        self.__payment = payment
        return "Success"
        pass

    def update_pay_med(self, pay_med: 'PaymentMethod'):
        self.__pay_med = pay_med
        return "Success"
        pass

    def update_date(self, start, end):
        result = self.create_booked_date(start, end)
        return result

    def update_guest(self, guest):
        try:
            if not (isinstance(guest, int)):
                guest = int(guest)
            self.__guess_amount = guest
            return "Success"
        except:
            return "can't update guest"

    def create_payment(self, price, period, paymed):
        from .Payment import Payment
        if not (isinstance(price, int) and isinstance(period, int)):
            payment = Payment(None, None, None)
            return payment
        payment = Payment(period=period, pay_med=paymed, price=price)
        return payment

    def create_payment_and_med(self, payment, paymed, card_num, password, period, balance, point=10):
        from .Payment import Payment
        if self.__member.get_pay_med.get_bank_id == card_num:
            return "You already Have this Card"
        if paymed == "Debit":
            paymed = self.create_pay_med(
                card_num, self.__member, balance, password)
        else:
            paymed = self.create_pay_med(
                card_num, self.__member, balance, password, point)
        if payment == "OneTime":
            payment = Payment(period=1, pay_med=paymed, price=self.__amount)
        else:
            payment = Payment(period=period, pay_med=paymed,
                              price=self.__amount)
        self.update_pay_med(paymed)
        self.update_payment(payment)
        return "Success"

    def create_pay_med(self, id, balance):
        from .Payment import PaymentMethod
        pay_med = PaymentMethod(
            bank_id=id, user=self.__member, balance=balance)
        return pay_med

    def create_booked_date(self, start, end):
        try:
            start = datetime.strptime(start, "%Y-%m-%d")
            end = datetime.strptime(end, "%Y-%m-%d")
            self.__booked_date = BookedDate(start, end)
            return "success"
        except:
            return "create date got a problem"

    def cal_price(self):
        try:
            result = self.get_accommodation.cal_price_accom(
                self.get_booked_date.get_checkindate,
                self.get_booked_date.get_checkoutdate,
                self.get_guess_amount

            )
            return result
        except Exception as e:
            return e

    def add_booked_date(self, date):
        try:
            isinstance(date, BookedDate)
            self.__booked_date = date
            return "Success"
        except Exception as e:
            return e

    # format booking class to text format

    def __str__(self):
        return (
            f"Booking ID: {self.__booking_id}\n"
            f"Accommodation: {self.__accommodation.get_acc_name}\n"
            f"Check-in Date: {self.__booked_date.get_checkindate_pretty}\n"
            f"Check-out Date: {self.__booked_date.get_checkoutdate_pretty}\n"
            f"Number of Guests: {self.__guess_amount}\n"
            f"Booking Status: {self.__booking_status}\n"
            # f"Member: {self.__member.get_user_name}\n"
            f"Payment: {self.__payment}\n"
            f"Payment Method: {self.__pay_med}"
            f"Price : {self.__price}"
            f"User ID: {self.__member.get_user_id}"
        )

    def set_amount(self, amount):
        self.__amount = amount
        
    def add_payment(self, payment):
        self.__payment = payment

    def add_coupon_by_id(self, coupon_id):
        from .User import Coupon
        from .User import Member
        if coupon_id == "del":
            self.set_cou(None)
        coupon = self.__member.search_cou_by_id(coupon_id)
        if isinstance(coupon, str):
            return coupon
        self.set_cou(coupon)

    def set_cou(self, coupon):
        self.__coupon = coupon


class BookedDate:
    def __init__(self, checkindate, checkoutdate):
        self.__checkindate = checkindate
        self.__checkoutdate = checkoutdate

    @property
    def get_checkindate(self):
        return self.__checkindate

    @property
    def get_checkoutdate(self):
        return self.__checkoutdate

    @property
    def get_checkindate_pretty(self):
        return self.__checkindate.strftime("%d/%m/%Y")

    @property
    def get_checkoutdate_pretty(self):
        return self.__checkoutdate.strftime("%d/%m/%Y")

    @property
    def to_string(self):
        return f"{self.__checkindate.strftime('%d-%m-%Y')} to {self.__checkoutdate.strftime('%d-%m-%Y')}"
