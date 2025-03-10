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

# Initialize the app
app, rt = fast_app()

# Setup function to initialize control_system
# @app.on_event("startup")
def setup_app(app):
    print("=========================Start===============================")
    control_system = ControlSystem()
    app.state.control_system = control_system
    
    # Perform initialization
    control_system.add_member_and_payment_method()
    control_system.add_accommodation_test()
    control_system.make_booking()
    # control_system.add_accommodation_booked_date()
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

@rt('/monitor', methods=['GET'])
async def monitor(req):
    web_control_system = req.app.state.control_system
    return web_control_system.get_html_monitor_airbnb()


@rt('/purchase/booking_id={booking_id:int}', methods=['POST'])
async def purchase(req, booking_id: int):
    
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_user_id = form_data.get('user_id')
    result_booking = web_control_system.search_booking_by_id(booking_id)
    if result_booking == 'cant find':
        return Html(P(result_booking))
    else:
        return web_control_system.generate_booking_html(result_booking, booking_id, web_user_id)
        

@rt('/process_payment/booking_id={booking_id:int}', methods=['POST'])
async def process_payment(req, booking_id: int):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_payment_method = form_data.get('payment_method_id')
    web_payment_expired_date = form_data.get('expired_date')
    web_payment_vcc = form_data.get('vcc_number')
    web_payment_type = form_data.get('payment_type')
    web_period = form_data.get('period')
    
    # TODO:
    result = web_control_system.process_payment(booking_id, web_payment_method, web_payment_expired_date, web_payment_vcc, web_payment_type, web_period)
    return result

@rt('/')
async def index(req):
    form_data = await req.form()
    user_id = form_data.get('user_id')
    web_control_system = req.app.state.control_system
    return web_control_system.get_html_index(user_id)

    
@rt('/payment/add')
async def add_payment(req):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_user_id = form_data.get('user_id')
    return web_control_system.get_html_add_payment(web_user_id)
    # return Html(P(f"user_id : {web_user_id}"))

@rt('/payment/add/process', methods=['POST'])
async def add_payment_process(req):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_bank_id = form_data.get('bank_id')
    web_expired_date = form_data.get('expired_date')
    web_vcc_number = form_data.get('vcc_number')
    web_user_id = form_data.get('user_id')
    return web_control_system.get_html_add_payment_process(web_user_id,web_bank_id, web_expired_date, web_vcc_number)
    # return Html(P(f"user_id : {web_user_id}"),
    #             P(f"bank_id : {web_bank_id}"),
    #             P(f"expired_date : {web_expired_date}"),
    #             P(f"vcc_number : {web_vcc_number}"))

    
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
    return web_control_system.get_html_booking_history(user_id)
    #---------------
    
    
@rt('/view_booking_detail/{user_id}/{booking_id}')
def get(user_id : int, booking_id: int):
    web_control_system = app.state.control_system
    return web_control_system.get_html_view_booking_detail(user_id, booking_id)
    #------
      
      
      
@rt('/cancel_booking/{booking_id}', methods=["post"])
def cancel_booking(booking_id: int, _method: str = Form(...)):
    if _method.lower() == "put":
        web_control_system = app.state.control_system
        user_id = web_control_system.cancel_booking(booking_id)
        return RedirectResponse(f"/booking_history/{user_id}", status_code=303)
    return "Invalid method", 405


@rt('/booking/{book_id}')
def get(book_id: str):
    web_control_system = app.state.control_system
    return web_control_system.get_html_booking(book_id)


@rt('/create_pay')
def post(payment: str, period: str,
         paymed: str, card_num: str, expiration_date: str, password: str, booking_id: str):
    web_control_system = app.state.control_system
    return web_control_system.get_html_create_pay(payment, period, paymed, card_num, expiration_date, password, booking_id)


@rt('/edit_date_guest/{book_id}')
def get(book_id: str):
    web_control_system = app.state.control_system
    return web_control_system.get_html_edit_date_guest(book_id)

@rt('/update_date_guest/{book_id}')
def update(start: str, end: str, guest_amount: str, book_id: str):
    # อัปเดตวันที่และจำนวนแขกใน booking
    # return P(f"{book_id}")
    web_control_system = app.state.control_system
    web_control_system.get_html_update_date_guest(start, end, guest_amount, book_id)
    return Redirect(f"/booking/{book_id}")
    #----
    
@rt("/room/{accom_id}")
def room(accom_id: int):
    # assuming user host some accom
    controlsystem = app.state.control_system
    controlsystem.get_html_room_detail(accom_id)
    #--------

@rt("/Hosting/{user_id}")
def host(user_id: int):
    controlsystem = app.state.control_system
    controlsystem.get_html_hosting(user_id)
    #--------
    

@rt("/price_summary/{user_id}/{accom_id}", methods=["POST"])
async def post(user_id: int, accom_id: int, request: Request):
    controlsystem = app.state.control_system
    form_data = (
        await request.form()
    )  # ✅ Retrieve the submitted form data # wait until the form data is available
    controlsystem.get_html_price_summary(user_id, accom_id, form_data)
    
    #------
    
@rt("/create_booking", methods="POST")
def post_bookin(
    user_id: str,
    check_in: str,
    check_out: str,
    accom_id: str,
    total_price: str,
    guests: str,
):
    controlsystem = app.state.control_system
    controlsystem.get_html_create_booking(user_id, check_in, check_out, accom_id, total_price, guests)
    
@rt("/update_accommodation_status")
def get():
    web_control_system = app.state.control_system
    accommodation_list = web_control_system.show_accom_to_update()
    
    return Titled(
        "Confirm Accommodation",
        Container(
            Form(Button("Back to Home Page", type="submit"), method="get", action="/")
        ),
        Table(
            Thead(Tr(Th("ID"), Th("Status"), Th(""))),
            Tbody(*[
                Tr(
                    Td(p[0]),
                    Td("Approved" if p[1] else "Pending"),
                    Td(
                        Form(
                            Hidden(name="_method", value="PUT"),
                            Button("Cancel Approve" if p[1] else "Approve", type="submit"),
                            method="post",
                            action=f"/update_accommodation/{p[0]}"
                        )
                    )
                )
                for p in accommodation_list
            ])
        )
    )
    
@rt('/update_accommodation/{accommodation_id}', methods=["post"])
def post(accommodation_id: int, _method: str = Form(...)):
    web_control_system = app.state.control_system
    if _method.lower() == "put":
        
        detail = web_control_system.approve_accommodation(accommodation_id)

        if detail != "Success":
            return H1("Error")

        return RedirectResponse(f"/update_accommodation_status", status_code=303) 
    return "Invalid method", 405
    
@rt('/sign_up')
def get(): return Div(
    {"data-theme": "light"},
    Title("Booking 999"),
    Div(
        A(
            Img(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/1200px-Airbnb_Logo_B%C3%A9lo.svg.png",
                style="""
                margin: 0;
                padding: 5px;
                text-align: center;
                items-align: center;
                background-color: white;
                height: 60px;
                border: none;
                cursor: pointer;
                """),
            href="/"),

        style="""
        background-color:white;
        padding: 15px;
        height:80px;
        align-items: center;
        """
    ),
    Div(H1("Sign Up", style="padding-top: 20%"),
        {"data-theme": "light"},

        Form(
        Div(
            Label("Name"),
            Input(type="text", id="name", name="name",
                  placeholder="Enter your name"),
            style="""
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
            """
        ),
        Div(
            Label("Email"),
            Input(type="text", id="email", name="email",
                  placeholder="Enter your email"),
            style="""
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
            """
        ),
        Div(
            Label("Phone Number"),
            Input(type="text", id="phone_num", name="phone_num",
                  placeholder="Enter your Phone Number"),
            style="""
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
            """
        ),
        Div(
            Label("Age"),
            Input(type="number", id="age", name="age",
                  placeholder="Enter your Age"),
            style="""
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
            """
        ),
        Div(
            Label("Create Password"),
            Input(type="password", id="password", name="password",
                  placeholder="Enter your password"),
            style="""
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
            """
        ),
        Button("Sign Up", type="submit", style="width:50%"), Hr("Or"),
        method="post",
        action="/create_account",
        style="padding:15px;width:100%"

    ),
        style="""
    padding-top:30vh
    background-color:white;
    color:black;
    width: 500px;
    margin: auto;
    height:70vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    """
    ),
    style="background-color:white"
), Div(A(Button("Login"), href="/log_in",
         style="""
     background-color:white;
    color:black;
    """), style="""
     background-color:white;
    color:black;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height:30vh;
    """)



@rt('/create_account')
def post(name: str, email: str, phone_num: str, password: str, age):
    control = app.state.control_system
    result = control.create_account(name, email, password, phone_num, age)
    id = control.get_member_id(name, email, phone_num, password)
    if not id:
        return Div(H1("Error: Could not retrieve user ID"), A(Button("Try Again"), href="/sign_up"))
    return Div(H1(f"create Account {result} and yor id is {id}", style="""
                    background-color:white;
                    color:black;"""),
               A(Button("Home"), href=f"/home/{id}"),
               style="""
                    background-color:white;
                    color:black;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    height:100vh;
                    """)


if __name__ == "__main__":
    
    serve()