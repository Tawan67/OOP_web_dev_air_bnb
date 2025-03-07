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
    new_house = House("test_house", "location", "description", 6969, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJxo2NFiYcR35GzCk5T3nxA7rGlSsXvIfJwg&s")
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
        date=datetime.now(),
        guess=2,
        member=control_system.get_member_list[0]
    )
    control_system.get_booking_by_id(1).add_booked_date(BookedDate(datetime.now(), datetime.now() + timedelta(days=5)))
    
    control_system.create_booking(
        accom=control_system.get_accommodation_list[2],
        date=datetime.now(),
        guess=5,
        member=control_system.get_member_list[0]
    )
    control_system.get_booking_by_id(2).add_booked_date(BookedDate(datetime.now() + timedelta(days=6), datetime.now() + timedelta(days=10)))
    
    control_system.create_booking(
        accom=control_system.get_accommodation_list[2],
        # date=BookedDate(datetime.now() + timedelta(days=10), datetime.now() + timedelta(days=20)),
        date=datetime.now(),

        guess=10,
        member=control_system.get_member_list[0]
    )
    control_system.get_booking_by_id(3).add_booked_date(BookedDate(datetime.now() + timedelta(days=6), datetime.now() + timedelta(days=20)))

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
    # add_accommodation_booked_date(control_system)
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
        return web_control_system.generate_booking_html(result_booking, booking_id)
        

@rt('/process_payment/booking_id={booking_id:int}', methods=['POST'])
async def process_payment(req, booking_id: int):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_payment_method = form_data.get('payment_method')
    web_payment_owner_name = form_data.get('full_name')
    
    # TODO:
    result = web_control_system.process_payment(booking_id, web_payment_method, web_payment_owner_name)
    return result

@rt('/')
async def index(req):
    form_data = await req.form()
    user_id = form_data.get('user_id')
    web_control_system = req.app.state.control_system
    return web_control_system.get_html_index()



@rt('/payment')
def payment(req):
    web_control_system = req.app.state.control_system
    return Html(
        H1("Payment Method"),
        P(f'Bank ID : {web_control_system.get_member_list[0].get_payment_method_list[0].get_bank_id}'),
        P(f'Balance : {web_control_system.get_member_list[0].get_payment_method_list[0].get_balance}'),
        P(f'Name : {web_control_system.get_member_list[0].get_payment_method_list[0].get_owner.get_user_name}'),     
    )
    
@rt('/search')
async def search(req):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_search_query = form_data.get('search_query')
    web_check_in = form_data.get('check_in')
    web_check_out = form_data.get('check_out')
    
    return web_control_system.get_html_search_query( web_search_query, web_check_in, web_check_out)

@rt("/booking_history/{user_id}")
def get(user_id : int, req):
    web_control_system = req.app.state.control_system
    user_id = int(user_id)
    booking_list = web_control_system.get_booking_history(user_id)
    

    if booking_list == None:
        return Container(H1("Can't Find Booking History"),
                Form(Button("Back to Home page", type="submit"), 
                method="get",
                action=f"/"
            )
    )


    return Titled(
        "Booking History",
        Container(
            Form(Button("Back to Home Page", type="submit"), method="get", action="/")
        ),
        Table(
            Thead(Tr(Th("ID"), Th("Status"), Th("Date"), Th("Accommodation name"), Th("Check-In"), Th("Check-Out"), Th("Amount"), Th(""))),
            Tbody(*[
                Tr(
                    Td(p[0]), Td(p[1]), Td(p[2]),Td(p[3]),Td(p[4]),Td(p[5]),Td(p[6]),
                Td(
                    Form(
                        Button("Detail", type="submit"),
                        method="get",
                        action=f"/view_booking_detail/{user_id}/{p[0]}"
                    )
                )               
                )
                for p in booking_list
            ])
        )
    )      
    
@rt('/view_booking_detail/{user_id}/{booking_id}')
def get(user_id : int, booking_id: int):
    web_control_system = app.state.control_system
    detail = web_control_system.get_booking_detail(booking_id)
    cancel_button = None
    if detail[1] != "Cancelled" and detail[1] != "Completed":
        cancel_button = Form(
            Hidden(name="_method", value="PUT"),
            Button("Cancel Booking", type="submit"),
            method="post",
            action=f"/cancel_booking/{detail[0]}"
        )

    if detail == None:
        return Container(H1("Can't Find Booking"),
                Form(Button("Back to Booking History", type="submit"), 
                method="get",
                action=f"/booking_history/{user_id}"
            )
    )
    else:       
        return Titled(
        f"Booking Detail for {detail[0]}",
        Container(
            P(f"Booking ID: {detail[0]}"),
            P(f"Status: {detail[1]}"),
            P(f"date: {detail[2]}"),
            P(f"Accommodation Name: {detail[6]}"),
            P(f"Check-In Date: {detail[4]}"),
            P(f"Check-Out Date: {detail[5]}"),
            P(f"Amount: {detail[3]}"),
            P(f"Accommodation Info: {detail[7]}"),        
            P(f"Address: {detail[8]}"),
            P(f"Host Name: {detail[9]}"),
            P(f"Phone Number: {detail[10]}"),
            cancel_button,
            Form(Button("Back to Booking History", type="submit"), 
                method="get",
                action=f"/booking_history/{user_id}"
            )
        )
    )
      
      
      
@rt('/cancel_booking/{booking_id}', methods=["post"])
def cancel_booking(booking_id: int, _method: str = Form(...)):
    if _method.lower() == "put":
        web_control_system = app.state.control_system
        user_id = web_control_system.cancel_booking(booking_id)
        return RedirectResponse(f"/booking_history/{user_id}", status_code=303)
    return "Invalid method", 405

    



if __name__ == "__main__":
    
    serve()