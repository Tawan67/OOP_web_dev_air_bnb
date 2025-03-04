import math
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
