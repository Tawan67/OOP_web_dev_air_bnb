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
print(control_system.get_booking_list)

# # Get booking details
# display = control_system.get_member_list[0].get_paymed[0].get_balance
# get_date = control_system.get_booking_list[0].get_date
# checkin = get_date.get_checkindate_pretty
# checkout = get_date.get_checkoutdate_pretty
# guess = control_system.get_booking_list[0].get_guess_amount
# my_booking = control_system.get_booking_list[0]
# booking_price = my_booking.get_accommodation.get_price
# accom_name = my_booking.get_accommodation.get_acc_name
# accom_address = my_booking.get_accommodation.get_address



###################################


# serve()