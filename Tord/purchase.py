from fasthtml.common import *
from datetime import datetime, timedelta

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

    def search_accom_by_id(self, accom_id):  # 1
        for i in self.__accommodation_list:
            if i.get_id == accom_id:
                return i
        return "Not Found"


    def create_booking(self, accom, date, guess, member):
        newbooking = Booking(accom=accom, date=date, guess=guess, member=member)
        self.add_booking(newbooking)

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

    def check_accom_available(self, booking_id):
        pass

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
        Accommodation.count_id += 1

    def add_accom_pics(self, pic):
        self.__accom_pics.append(pic)
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
        self.__bank_id = bank_id
        self.__owner = user
        self.__balance = balance

    @property
    def get_balance(self):
        return self.__balance

    def pay(self, pray_tang):
        pass

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

    def __init__(self, accom, date, guess, member):
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
        self.__check_in = None
        self.__check_out = None
        Booking.count += 1

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
        # FIXME:
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


def add_user_and_payment_method(control_system):
    """
    Creates a User and PaymentMethod instance, associates them, and adds the User to ControlSystem
    """
    # Create a User instance
    user = User("Jane Smith", "jane@example.com", "securepass123")
    
    # Create a PaymentMethod instance associated with the user
    payment_method = PaymentMethod("BANK456", user, 500.0)
    
    # Add PaymentMethod to User
    result_payment = user.add_payment_method(payment_method)
    if result_payment != "Success":
        return f"Failed to add payment method: {result_payment}"
    
    # Add User to ControlSystem as a member
    result_member = control_system.add_member(user)
    if result_member != "Success":
        return f"Failed to add user to control system: {result_member}"
    
    return f"Successfully added user {user.get_user_id} with payment method to control system"

def add_accommodation(control_system):
    # Create a test Host instance
    test_host = Host(
        name="John Doe",
        email="john.doe@example.com",
        password="securepass123",
        phone_num="123-456-7890",
        age=35
    )

    # Create a test House instance
    test_house = House(
        name="Cozy Cottage",
        address="123 Forest Lane, Natureville",
        info="A charming cottage in the woods",  # Added missing info parameter
        price=150.00
    )
    test_house.add_accom_pics("https://via.placeholder.com/300x200?text=Cozy+Cottage")

    # Create a test Hotel instance
    test_hotel = Hotel(
        name="Grand Hotel",
        address="456 City Ave, Metropolis",
        info="A luxurious downtown hotel"  # Added missing info parameter
    )
    test_hotel.add_accom_pics("https://via.placeholder.com/300x200?text=Grand+Hotel")

    # Create a test Room instance
    test_room = Room(
        room_id="R101",
        room_floor=1,
        price=120.00,
        hotel_address="456 City Ave, Metropolis",
        hotel_name="Grand Hotel"
    )
    
    test_room.add_accom_pics("https://via.placeholder.com/300x200?text=Room+101")

    # Add the room to the hotel
    test_hotel.add_room(test_room)

    # Add accommodations to the host's list
    test_host.add_accommodation([test_house, test_hotel])

    # Store in ControlSystem
    control_system.add_host(test_host)
    control_system.add_accommodation(test_house)
    control_system.add_accommodation(test_hotel)
    # Note: We don't add the room directly to control_system since it's part of the hotel

    return "Test host, house, and hotel with room added successfully"
# TODO:
def make_booking(control_system):
    control_system.create_booking(
        accom=control_system.search_accom_by_id(1), 
        date=datetime.now(), 
        guess=2, 
        member=control_system.search_member_by_id(1)
        )
    control_system.get_booking_list[0].set_check_in(datetime.now())
    control_system.get_booking_list[0].set_check_out(datetime.now() + timedelta(days=5))

def get_style():
    return Style("""
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 8px; margin-bottom: 10px; }
        button { background-color: #FF5A5F; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #FF6B70; }
        fieldset { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; }
        legend { font-size: 1.2em; font-weight: bold; }
        .payment-details { background-color: #f9f9f9; padding: 15px; border-radius: 4px; }
        .error { color: red; }
        .success { color: green; }
    """)

app = FastHTML()

# Initialize control system and setup data
control_system = ControlSystem()
add_user_and_payment_method(control_system)
add_accommodation(control_system)
make_booking(control_system)

# Get booking details
display = control_system.get_member_list[0].get_payment_method[0].get_balance
booking_price = control_system.get_booking_list[0].get_accommodation.get_price
checkin = control_system.get_booking_list[0].get_check_in
checkout = control_system.get_booking_list[0].get_check_out
guess = control_system.get_booking_list[0].get_guess

@app.route('/')
def home():
    return Html(
        Head(Title('Payment Form'), get_style()),
        Body(
            Div(
                H1('Complete Your Booking Payment'),
                Form(
                    Fieldset(
                        Legend('Booking Summary'),
                        Div(
                            P(f'Guests: {guess}'),
                            P(f'Check-in: {checkin.strftime("%Y-%m-%d %H:%M")}'),
                            P(f'Check-out: {checkout.strftime("%Y-%m-%d %H:%M")}'),
                            P(f'Total Price: ${booking_price * guess}'),
                            cls='payment-details'
                        )
                    ),
                    Fieldset(
                        Legend('Payment Details'),
                        Div(
                            Label('Payment Method'),
                            Select(
                                Option('Credit Card', value='credit'),
                                Option('Bank Transfer', value='bank'),
                                name='payment_type'
                            ),
                            cls='form-group'
                        ),
                        Div(
                            Label('Card Number'),
                            Input(type='text', name='card_number', placeholder='XXXX-XXXX-XXXX-XXXX', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('Card Holder Name'),
                            Input(type='text', name='card_holder', placeholder='John Doe', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('Expiration Date'),
                            Input(type='month', name='expiry_date', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('CVV'),
                            Input(type='text', name='cvv', placeholder='123', maxlength='4', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('Billing Address'),
                            Textarea(name='billing_address', rows='3', placeholder='Enter your billing address', required=True),
                            cls='form-group'
                        )
                    ),
                    P(f'Current Balance: ${display}'),
                    Button('Process Payment', type='submit'),
                    action='/process_payment',
                    method='post'
                ),
                cls='container'
            )
        )
    )

@app.route('/process_payment', methods=['POST'])
def process_payment(req):
    form_data = req.form
    
    # Basic validation
    if not all([form_data.get('card_number'), form_data.get('card_holder'), 
                form_data.get('expiry_date'), form_data.get('cvv')]):
        return Html(
            Head(Title('Payment Error')),
            Body(
                Div(
                    H1('Payment Failed'),
                    P('Please fill in all required fields.', cls='error'),
                    A('Try Again', href='/'),
                    cls='container'
                )
            )
        )
    
    # Simulate payment processing
    total_price = booking_price * guess
    current_balance = control_system.get_member_list[0].get_payment_method[0].get_balance
    
    if current_balance >= total_price:
        # Here you would normally process the payment
        # For this example, we'll just simulate success
        return Html(
            Head(Title('Payment Successful')),
            Body(
                Div(
                    H1('Payment Successful'),
                    P('Your booking has been confirmed!', cls='success'),
                    Div(
                        H3('Payment Details'),
                        P(f'Amount Paid: ${total_price}'),
                        P(f'Payment Method: {form_data["payment_type"]}'),
                        P(f'Card Ending: {form_data["card_number"][-4:]}'),
                        P(f'Transaction Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}'),
                        style='border-left: 4px solid #FF5A5F; padding-left: 15px;'
                    ),
                    A('Back to Home', href='/'),
                    cls='container'
                )
            )
        )
    else:
        return Html(
            Head(Title('Payment Error')),
            Body(
                Div(
                    H1('Payment Failed'),
                    P('Insufficient funds in your account.', cls='error'),
                    P(f'Required: ${total_price} | Available: ${current_balance}'),
                    A('Try Again', href='/'),
                    cls='container'
                )
            )
        )

if __name__ == "__main__":
    serve(port=5002)