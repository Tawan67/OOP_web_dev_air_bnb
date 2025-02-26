from fasthtml.common import *

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

    def search_accom_by_id(self, accom_id):
        pass

    def create_booking(self):
        pass

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

    def search_accomodation_by_id(self, accom_id):
        pass

    def search_host_by_accom(self, Accom):
        pass

class Accommodation:
    count_id = 1

    def __init__(self, name, address):
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__status = False
        self.__accom_pics = []
        Accommodation.count_id += 1

    def add_accom_pics(self, pic) -> str:
        self.__accom_pics.append(pic)
        return "Success"

    def update_status(self) -> str:
        self.__status = True
        return "Success"

    def update_calendar(self):
        pass

    def calculate(self, adult, children, pet):
        pass

    def sort_dates_list(self, dates_list):
        pass

    def get_accom_detail(self, Accommodation):
        pass

    def get_price(self, date, guest_amount):
        pass

    def cal_total_price(self):
        pass

    def get_review(self, Accommodation):
        pass

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
        self.__date = date
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
        Booking.count += 1

    @property
    def get_payment_method(self):
        return self.__pay_med

    @property
    def get_frequency(self):
        return self.__frequency

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

app = FastHTML()

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
    """)

@app.route('/')
def home():
    return Html(
        Head(Title('Request to Book'), get_style()),
        Body(
            Div(
                H1('Request to Book'),
                Form(
                    Fieldset(
                        Legend('Trip Details'),
                        Div(
                            Label('Check-in', Input(type='date', name='checkin', required=True)),
                            Label('Check-out', Input(type='date', name='checkout', required=True)),
                            Label('Guests', 
                                Select(
                                    *[Option(str(i), value=str(i)) for i in range(1, 11)],
                                    name='guests',
                                    required=True
                                )
                            ),
                            cls='form-group'
                        )
                    ),
                    
                    Fieldset(
                        Legend('About You'),
                        Div(
                            Label('Full Name', Input(type='text', name='name', required=True)),
                            Label('Email', Input(type='email', name='email', required=True)),
                            Label('Phone', Input(type='tel', name='phone', required=True)),
                            cls='form-group'
                        )
                    ),
                    
                    Fieldset(
                        Legend('Message to Host'),
                        Div(
                            Textarea(
                                name='message', 
                                rows=4, 
                                placeholder='Hi! I’m interested in booking your place. Could you tell me more about...',
                                cls='form-group'
                            )
                        )
                    ),
                    
                    Button('Request to Book', type='submit'),
                    
                    action='/submit',
                    method='post'
                ),
                cls='container'
            )
        )
    )

@app.route('/submit', methods=['POST'])
def submit(req):
    form_data = req.form
    return Html(
        Head(Title('Request Submitted')),
        Body(
            Div(
                H1('Request Submitted'),
                P('We’ve sent your request to the host.'),
                P('You’ll hear back within 24 hours.'),
                Div(
                    H3('Your Details'),
                    P(f'Name: {form_data["name"]}'),
                    P(f'Email: {form_data["email"]}'),
                    P(f'Dates: {form_data["checkin"]} to {form_data["checkout"]}'),
                    P(f'Guests: {form_data["guests"]}'),
                    style='border-left: 4px solid #FF5A5F; padding-left: 15px;'
                ),
                cls='container'
            )
        )
    )

if __name__ == "__main__":
    # Create ControlSystem instance
    control_system = ControlSystem()
    
    # Call the function
    result = add_user_and_payment_method(control_system)
    print(result)
    
    # Verify the setup
    print(f"Members in ControlSystem: {len(control_system.get_member_list)}")
    if control_system.get_member_list:
        user = control_system.get_member_list[0]
        print(f"User ID: {user.get_user_id}")
        print(f"User Name: {user.get_user_name}")
    
    serve(port=5002)