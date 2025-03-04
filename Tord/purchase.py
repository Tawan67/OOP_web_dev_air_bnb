from fasthtml.common import *
from datetime import datetime, timedelta
from calendar import monthrange, weekday

from utils.ControlSystem import ControlSystem 
from utils.Booking import Booking
from utils.Payment import Payment
from utils.Payment import PaymentMethod
from utils.User import User
from utils.User import Host
from utils.Booking import Booking
from utils.Accommodation import House
from utils.Accommodation import Hotel
from utils.Accommodation import Room
from utils.Booking import BookedDate
from utils.Payment import Card
from utils.Payment import Credit
from utils.User import Member




def add_user_and_payment_method(control_system):
    """
    Creates a User and PaymentMethod instance, associates them, and adds the User to ControlSystem
    """
    # Create a User instance
    member = Member("Jane Smith", "jane@example.com", "securepass123", "987-654-3210", 28)
    
    # Create a PaymentMethod instance associated with the user
    payment_method = PaymentMethod("BANK456", member, 500.0)
    
    # Add PaymentMethod to User
    result_payment = member.add_payment_method(payment_method)
    if result_payment != "Success":
        return f"Failed to add payment method: {result_payment}"
    
    # Add User to ControlSystem as a member
    result_member = control_system.add_member(member)
    if result_member != "Success":
        return f"Failed to add user to control system: {result_member}"
    
    return print(f"Successfully added user {member.get_user_id} with payment method to control system")

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

    return print("Test host, house, and hotel with room added successfully")
# TODO:
def make_booking(control_system):
    accom = control_system.search_accom_by_id(1)  # Assuming House with ID 1
    if accom == "Not Found":
        print("Accommodation not found")
        return
    
    check_in = datetime.now()
    check_out = datetime.now() + timedelta(days=5)
    
    result = control_system.create_booking(
        accom=accom,
        date= BookedDate(check_in, check_out),
        guess = 2,
        member = control_system.get_member_list[0]
    )
    print(result)
    
def add_accommodation_booked_date(control_system):
    new_booked_date = BookedDate(datetime.now(), datetime.now() + timedelta(days=2))
    control_system.get_accommodation_list[0].add_booked_date(new_booked_date)
    
    new_booked_date = BookedDate(datetime.now() + timedelta(days=4), datetime.now() + timedelta(days=6))
    control_system.get_accommodation_list[0].add_booked_date(new_booked_date)
    
    new_booked_date = BookedDate(datetime.now() + timedelta(days=8), datetime.now() + timedelta(days=12))
    control_system.get_accommodation_list[0].add_booked_date(new_booked_date)
    
   
# Updated CSS with calendar styling
def get_style():
    return Style("""
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
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
        .calendar { border-collapse: collapse; width: 100%; margin-top: 10px; }
        .calendar th, .calendar td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        .calendar th { background-color: #f2f2f2; }
        .calendar .booked { background-color: #ffcccc; }
    """)

app ,rt= fast_app()

######## Call Function ############

# Initialize control system and setup data
control_system = ControlSystem()
add_user_and_payment_method(control_system)
add_accommodation(control_system)
make_booking(control_system)
add_accommodation_booked_date(control_system)
get_date = control_system.get_booking_list[0].get_date

# Get booking details
display = control_system.get_member_list[0].get_paymed[0].get_balance
get_date = control_system.get_booking_list[0].get_date
checkin = get_date.get_checkindate_pretty
checkout = get_date.get_checkoutdate_pretty
guess = control_system.get_booking_list[0].get_guess_amount
my_booking = control_system.get_booking_list[0]
booking_price = my_booking.get_accommodation.get_price
accom_name = my_booking.get_accommodation.get_acc_name
accom_address = my_booking.get_accommodation.get_address



###################################


@rt('/')
def home():
    # Format booked dates as a readable string
    booked_dates_str = ""
    booked_dates = my_booking.get_accommodation.get_book_dates
    if booked_dates:
        booked_dates_str = ", ".join(
            f"{bd.get_checkindate().strftime('%Y-%m-%d')} to {bd.get_checkoutdate().strftime('%Y-%m-%d')}"
            for bd in booked_dates
        )
    else:
        booked_dates_str = "No booked dates yet"

    return Html(
        Head(Title('Payment Form'), get_style()),
        Body(
            Div(
                H1('Complete Your Booking Payment'),
                Form(
                    Fieldset(
                        Legend('Booking Summary'),
                        Div(
                            P(f'Accommodation: {accom_name}'),
                            P(f'Address: {accom_address}'),
                            P(f'Booked Dates: {booked_dates_str}'),  # Improved display
                            P(f'Guests: {guess}'),
                            P(f'Check-in: void'),
                            P(f'Check-out: void'),
                            P(f'Total Price: ${booking_price * guess}'),
                            cls='payment-details'
                        )
                    ),
                    # [Rest of the form remains unchanged]
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
                    P(f'Card Number: {control_system.get_member_list[0].get_payment_method[0].get_id}'),
                    P(f'Current Balance: ${control_system.get_member_list[0].get_payment_method[0].get_balance}'),
                    P(f'Point: {control_system.get_member_list[0].get_payment_method[0].get_point}'),
                    Button('Process Payment', type='submit'),
                    action='/process_payment',
                    method='post'
                ),
                cls='container'
            )
        )
    )

@rt('/process_payment')
async def process_payment(req):
    form_data = await req.form()
    # Simulate payment processing
    total_price = booking_price * guess
    pay_med = control_system.get_member_list[0].get_payment_method[0]
    booking = control_system.get_booking_list[0]

    #TODO: add check_accomo_avalable(booking_id)
    # Check availability for the booking's dates
    availability = control_system.check_accom_available(
        booking.get_accommodation.get_id,
        booking.get_date.get_checkindate,
        booking.get_date.get_checkoutdate
    )

    if (form_data.get('card_number') == pay_med.get_id) and (total_price < pay_med.get_balance) and availability:
        
        # booked_date = BookedDate(booking.get_check_in, booking.get_check_out)
        status = booking.get_accommodation.add_booked_date(control_system.get_booking_list[0].get_date)
        
        # Here you would normally process the payment
        # For this example, we'll just simulate success
        result = pay_med.pay(total_price)
        return Html(
            Head(Title('Payment Successful')),
            Body(
                Div(
                    H1('Payment Successful'),
                    P('Your payment has been processed successfully.', cls='success'),
                    P(f'New Balance: ${pay_med.get_balance}', cls='success'),
                    P(f'Booking Status: {status}', cls='success'),
                    Form(
                        Label('Go Back?'),
                        Button('Go Back', type='submit'),
                        action='/',
                        method='get'
                    ),
                    cls='container'
                )
            )
        )
    else:
        return Html(
            Head(Title('Payment Error')),
            Body(
                Div(
                    H1('Payment Error'),
                    P(form_data.get('card_number') == pay_med.get_id ),
                    P(f'Enough Money : {total_price < pay_med.get_balance}'),
                    P(f'Available : {availability}'),
                )
            )
            
        )
        

if __name__ == "__main__":
    serve(port=5002)
