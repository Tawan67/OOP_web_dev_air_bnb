import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
class Payment:

    count = 1

    def __init__(self, period, pay_med, price):
        self.__status = False
        self.__period_list = []
        self.__pay_med = pay_med
        self.__pay_id = Payment.count
        self.__interest = 5/100
        Payment.count += 1
        # total = self.cal_interest(price, period)
        if price != None:
            self.create_period(price, period)
        self.__total_price = price

        pass

    # def __init__(self, period, pay_med, id): tord2
    #     self.__status = False
    #     self.__period_list = period
    #     self.__pay_med = pay_med
    #     self.__pay_id = id
    
    @property
    def get_pay_med(self):
        return self.__pay_med

    def cal_interest(self, price, period):
        total_price = price*pow((1+((self.__interest/12)*period)), period)
        total_price = math.ceil(total_price)
        return total_price
        pass

    def pay_time(self):

        pass

    def create_period(self, price, period):
        if isinstance(period, str):
            period =int(period)
        if isinstance(price, str):
            price = int(price)
        price_per_time = math.ceil(int(price)/int(period))
        start_date = datetime.now()
        for p in range(period):
            new_date = start_date + relativedelta(months=p)
            pay_part = Period(price_per_time, new_date)
            self.__period_list.append(pay_part)
        return "Success"
    
    def __str__(self):
        return f"Payment ID: {self.__pay_id}, Price : {self.__total_price}, Payment Method: {self.__pay_med}, Period: {[str(per) for per in self.__period_list]}"

    def reset_increament(self):
        Payment.count = 1
      
    @property
    def get_period_list(self):
        return self.__period_list

class PaymentMethod:
    def __init__(self, bank_id, user, balance, expired_date=None, vcc=None):
        self.__bank_id = bank_id
        self.__owner = user
        self.__balance = balance
        self.__expired_date = expired_date
        self.__vcc = vcc

    @property
    def get_bank_id(self):
        return self.__bank_id

    def pay(self, pray_tang):
        self.__balance -= pray_tang
        self.__point += pray_tang
    
    @property
    def get_balance(self):
        return self.__balance
    
    @property
    def get_owner(self):
        return self.__owner
    
    def set_owner(self, new_owner):
        self.__owner = new_owner
        return "Owner updated successfully"
    
    @property
    def get_expired_date(self):
        return self.__expired_date
    
    @property
    def get_vcc_number(self):
        return self.__vcc
    
    @property
    def get_expired_date_pretty(self):
        return self.__expired_date.strftime("%Y-%m-%d")
    
    def deduction(self, pray_tang):
        if pray_tang > self.__balance:
            return "Not enough balance"
        else:   
            self.__balance -= pray_tang
            return "Success"
        return "fail to deduction"
    
    def update_balance(self, amount):
        self.__balance += amount
    
        
    def __str__(self):
        return f"id:{self.__bank_id}, owner:{self.__owner.get_user_name if self.__owner is not None else 'No Owner'}, balance:{self.__balance}, expired_date:{self.get_expired_date_pretty}, vcc:{self.__vcc}"


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

class Period:
    def __init__(self, price, date):
        self.status = False
        self.price = price
        self.date = date
        pass

    def update_status(self):
        new_status = not (self.status)
        self.status = new_status
    pass

    def get_price(self):
        return self.price

    def check_date(self, date_check):
        if self.__date == date_check:
            return True
        return False
    
    def __str__(self):
        return f"Price: {self.price}, Date: {self.date}, Status: {self.status}"
