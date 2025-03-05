from fasthtml.common import *
from datetime import datetime, timedelta
from calendar import monthrange, weekday

from utils.ControlSystem import ControlSystem 
from utils.Booking import Booking
from utils.Payment import Payment
from utils.Payment import PaymentMethod
from utils.User import User
from utils.User import Host
from utils.Accommodation import House
from utils.Accommodation import Hotel
from utils.Accommodation import Room
from utils.Accommodation import Accommodation
from utils.Booking import BookedDate
from utils.Payment import Card
from utils.Payment import Credit
from utils.User import Member

# Global variable to store the booking (optional, can remove if not needed)
my_booking = None

def add_member_and_payment_method(control_system):
    reset = Member('','','','','')
    reset.reset_increament()
    new_member = Member(name="Tord", email="saygex@gmail.com", password=1234, phone_num=1234567890, age=19)
    control_system.add_member(new_member)
    new_pay_med = PaymentMethod(bank_id="1234", user=new_member, balance=100000)
    control_system.add_payment_method(new_pay_med)
    control_system.search_member_by_id(new_member.get_user_id).add_payment_method(new_pay_med)
    balance = control_system.search_member_by_id(new_member.get_user_id).get_payment_method_list[0].get_balance
    print(f'name : {new_member.get_user_name}, balance : {balance}')

def add_accommodation(control_system):
    reset = Accommodation(None,None,None,None)
    reset.reset_increament()
    new_house = House("test_house", "location", "description", 6969)
    control_system.add_accommodation(new_house)
    new_host = Host(name="Tro", email="saygex1@gmail.com", password=12345, phone_num=1234567890, age=96)
    new_house.add_host(new_host)
    control_system.add_host(new_host)
    control_system.search_host_by_id(new_host.get_user_id).add_accommodation(new_house)
    print(f'Accommodation : {new_house.get_acc_name},ID : {new_house.get_id}, Host : {new_host.get_user_name}')    
    
    new_hotel = Hotel("test_hotel", "location_hotel", "description_hotel")
    control_system.add_accommodation(new_hotel)
    new_hotel.add_host(new_host)
    new_room = Room(room_id="1", room_floor=1, price=1000, hotel_address="location_hotel", hotel_name="test_hotel")
    control_system.add_accommodation(new_room)
    control_system.search_accom_by_id(new_hotel.get_id).add_room(new_room)
    control_system.search_host_by_id(new_host.get_user_id).add_accommodation(new_hotel)
    control_system.search_host_by_id(new_host.get_user_id).add_accommodation(new_room)
    print(f'Accommodation : {new_hotel.get_acc_name},ID : {new_hotel.get_id}, Host : {new_host.get_user_name}')  
    print(f'Accommodation : {new_room.get_acc_name},ID : {new_room.get_id}, Host : {new_host.get_user_name}')

def make_booking(control_system):
    reset = Booking(None,None,None,None)
    reset.reset_increment()

    
    control_system.create_booking(
        accom=control_system.get_accommodation_list[0],
        date=BookedDate(datetime.now(), datetime.now() + timedelta(days=5)),
        guess=2,
        member=control_system.get_member_list[0]
    )
    
    control_system.create_booking(
        accom=control_system.get_accommodation_list[2],
        date=BookedDate(datetime.now(), datetime.now() + timedelta(days=5)),
        guess=5,
        member=control_system.get_member_list[0]
    )
    
    control_system.create_booking(
        accom=control_system.get_accommodation_list[2],
        date=BookedDate(datetime.now() + timedelta(days=10), datetime.now() + timedelta(days=20)),
        guess=10,
        member=control_system.get_member_list[0]
    )

def add_accommodation_booked_date(control_system):
    new_booked_date = BookedDate(datetime.now(), datetime.now() + timedelta(days=2))
    control_system.get_accommodation_list[0].add_booked_date(new_booked_date)
    
    new_booked_date = BookedDate(datetime.now() + timedelta(days=4), datetime.now() + timedelta(days=6))
    control_system.get_accommodation_list[0].add_booked_date(new_booked_date)
    
    new_booked_date = BookedDate(datetime.now() + timedelta(days=8), datetime.now() + timedelta(days=12))
    control_system.get_accommodation_list[0].add_booked_date(new_booked_date)
    
    print(f'booked_date : {control_system.get_accommodation_list[0].get_booked_date}')

# Initialize the app
app, rt = fast_app()

# Setup function to initialize control_system
# @app.on_event("startup")
def setup_app(app):
    print("=========================Start===============================")
    control_system = ControlSystem()
    app.state.control_system = control_system
    
    # Perform initialization
    add_member_and_payment_method(control_system)
    add_accommodation(control_system)
    make_booking(control_system)
    add_accommodation_booked_date(control_system)
    print("=========================End===============================")
    return control_system

# Call setup once when the app starts
setup_app(app)

def get_style():
    return Style("""
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        .success { color: green; }
    """)

@rt('/purchase/booking_id={booking_id:int}', methods=['GET'])
async def purchase(req, booking_id: int):
    web_control_system = req.app.state.control_system
    result_booking = web_control_system.search_booking_by_id(booking_id)
    if result_booking == 'cant find':
        return Html(P(result_booking))
    else:
        """
        return Html(
            P(f"ID:{booking_id}"),
            P(f"Accommodation: {result_booking.get_accommodation.get_acc_name}"),
            P(f'Host : {result_booking.get_accommodation.get_host.get_user_name}'),
            P(f'Member: {result_booking.get_member.get_user_name}'),
        )
        """
        try:
            return (
            Title("Request to Book"),
            Div(
                H1("Request to Book"),
                Form(
                    Div(
                        H3("Your Trip"),
                        Div(
                            P(f"Accommodation: {web_control_system.search_booking_by_id(booking_id).get_accommodation.get_acc_name}"),
                            style="margin-bottom: 15px;"
                        ),
                        Div(
                            P(f"Accommodation Booked Date: {web_control_system.search_booking_by_id(booking_id).get_accommodation.get_booked_date_string}"),
                            style="margin-bottom: 15px;"
                        ),
                        Div(
                            P(f"Check-in: {result_booking.get_date.get_checkindate}"),
                            style="margin-bottom: 15px;"
                        ),
                        Div(
                            P(f"Check-out: {result_booking.get_date.get_checkoutdate}"),
                            style="margin-bottom: 15px;"
                        ),
                        Div(
                            P(f"Guests: {result_booking.get_guess_amount}"),
                            style="margin-bottom: 15px;"
                        ),
                        Div(
                            P(f"Price: {result_booking.cal_price()}"),
                            style="margin-bottom: 15px;"
                        ),
                        style="border: 1px solid #ddd; padding: 20px; border-radius: 5px;"
                    ),
                    
                    Div(
                        H3("Your Payment Details"),
                        
                        Div(
                            Label("Full Name"),
                            Input(type="text", name="fullname", required=True),
                            style="margin-bottom: 15px;"
                        ),
                        Div(
                            Label("Bank ID"),
                            Input(type="text", name="payment_method", required=True),
                            style="margin-bottom: 15px;"
                        ),
                        Div(
                            Label("Message to Host"),
                            Textarea(name="message", rows="4", placeholder="Tell the host about your trip..."),
                            style="margin-bottom: 15px;"
                        ),
                        style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; margin-top: 20px; margin-bottom: 20px;"
                    ),
                    Div(
                        Button("Request to Book", type="submit",
                            style="background-color: #FF5A5F; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;"),
                        action=f"/process_payment/booking_id={result_booking.get_booking_id}",
                        method="post"
                    )
                    
                    
                ),
                style="max-width: 500px; margin: 0 auto; padding: 20px;"
            )
        )
        except Exception as e:
            return Html(P(str(e)))
        
@rt('/payment')
def payment(req):
    web_control_system = req.app.state.control_system
    return Html(
        H1("Payment Method"),
        P(f'Bank ID : {web_control_system.get_member_list[0].get_payment_method_list[0].get_bank_id}'),
        P(f'Balance : {web_control_system.get_member_list[0].get_payment_method_list[0].get_balance}'),
        P(f'Name : {web_control_system.get_member_list[0].get_payment_method_list[0].get_owner.get_user_name}'),     
    )

@rt('/process_payment/booking_id={booking_id:int}', methods=['POST'])
async def process_payment(req, booking_id: int):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_payment_method = form_data.get('payment_method')
    web_payment_owner_name = form_data.get('full_name')
    
    # TODO:
    result = web_control_system.process_payment(booking_id, web_payment_method, web_payment_owner_name)
    return result

if __name__ == "__main__":
    
    serve()