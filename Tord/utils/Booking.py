class Booking:
    id = 1

    def __init__(self, accom, date, guess, member):
        self.__booking_id = Booking.id
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
        self.__price = None
        Booking.id += 1

    def reset_increment(self):
        Booking.id = 1
    
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
        from .Payment import Payment
        payment = Payment(period=period, pay_med=paymed, price=price)
        return payment
    
    def cal_price(self):
        try:
            result = self.get_accommodation.cal_price_accom(
                self.get_date.get_checkindate, 
                self.get_date.get_checkoutdate, 
                self.get_guess_amount
            )
            return result
        except Exception as e:
            return e
        
    
    # format booking class to text format
    def __str__(self):
        return (
            f'-----------------------------------'
            f"Booking ID: {self.__booking_id}\n"
            f"Accommodation: {self.__accommodation.get_acc_name}\n"
            f"Check-in Date: {self.__date.get_checkindate_pretty}\n"
            f"Check-out Date: {self.__date.get_checkoutdate_pretty}\n"
            f"Number of Guests: {self.__guess_amount}\n"
            f"Booking Status: {self.__booking_status}\n"
            f"Member: {self.__member.get_user_name}\n"
            f"Payment: {self.__payment}\n"
            f"Payment Method: {self.__pay_med}"
            f'-----------------------------------'
        )

    


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
