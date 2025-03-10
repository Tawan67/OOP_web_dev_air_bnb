from fasthtml.common import *
from datetime import datetime, timedelta
from calendar import monthrange, weekday
import time

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
app, rt = fast_app(
    middleware=[
        Middleware(SessionMiddleware, secret_key="your-secret-key-here", max_age=3600)  # 1-hour session
    ]
)

# Setup function to initialize control_system
# @app.on_event("startup")
def setup_app(app):
    print("=========================Start===============================")
    control_system = ControlSystem()
    app.state.control_system = control_system
    
    # Perform initialization
    control_system.add_member_and_payment_method()
    control_system.add_accommodation_test()
    control_system.make_booking_and_payment()
    # control_system.add_accommodation_booked_date()
    print("=========================End===============================")
    return control_system

# Call setup once when the app starts
setup_app(app)

while True:
    current_time = datetime.now()
    if current_time - start_time >= timedelta(seconds=10):
        app.state.control_system.deduction_period()
        start_time = current_time  # Reset the timer
    time.sleep(1)  # Add small delay to prevent CPU overuse

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
    # form_data = await req.form()
    # web_user_id = form_data.get('user_id')
    web_user_id = req.session.get("user_id")
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
    user_id = req.session.get("user_id")
    if not user_id:
        return RedirectResponse("/log_in", status_code=303)  # Redirect to login if not authenticated
    
    web_control_system = req.app.state.control_system
    return web_control_system.get_html_index(user_id)

    
@rt('/payment/add')
async def add_payment(req):
    web_control_system = req.app.state.control_system
    # form_data = await req.form()
    # web_user_id = form_data.get('user_id')
    web_user_id = req.session.get("user_id")
    return web_control_system.get_html_add_payment(web_user_id)
    # return Html(P(f"user_id : {web_user_id}"))

@rt('/payment/add/process', methods=['POST'])
async def add_payment_process(req):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_bank_id = form_data.get('bank_id')
    web_expired_date = form_data.get('expired_date')
    web_vcc_number = form_data.get('vcc_number')
    # web_user_id = form_data.get('user_id')
    web_user_id = req.session.get("user_id")
    return web_control_system.get_html_add_payment_process(web_user_id,web_bank_id, web_expired_date, web_vcc_number)
    # return Html(P(f"user_id : {web_user_id}"),
    #             P(f"bank_id : {web_bank_id}"),
    #             P(f"expired_date : {web_expired_date}"),
    #             P(f"vcc_number : {web_vcc_number}"))

    
@rt('/search')
async def search(req):
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    user_id = req.session.get("user_id")
    web_search_query = form_data.get('search_query')
    web_check_in = form_data.get('check_in')
    web_check_out = form_data.get('check_out')
    
    return web_control_system.get_html_search_query( web_search_query, web_check_in, web_check_out, user_id)

@rt("/booking_history/{user_id}")
def get(user_id : int, req):
    web_control_system = req.app.state.control_system
    user_id = req.session.get("user_id")
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
    # return Html(P(book_id))
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
    return web_control_system.get_html_update_date_guest(start, end, guest_amount, book_id)
    # return Redirect(f"/booking/{book_id}")
    #----
    
@rt("/accommodation/{accom_id}")
async def room(accom_id: int, req):
    # assuming user host some accom
    controlsystem = app.state.control_system
    form_data = await req.form()
    user_id = req.session.get("user_id")
    # controlsystem.get_html_room_detail(accom_id, user_id)
    #--------
    # user_id = self.get_member_list[0].get_user_id  # 21
    # host_id = self.get_host_list[0].get_user_id  # 31
    process_accom = controlsystem.search_accom_by_id(accom_id)
    host_id = process_accom.get_host.get_user_id
    # print(user_id)

    # print(user_id)
    print(f"host_id = {host_id}")
    print(f"user_id = {user_id}")
    detail = controlsystem.search_accom_detail(accom_id)
    

    accommodation1 = controlsystem.search_accom_by_id(accom_id)

    pic_list = accommodation1.get_accom_pics
    print(detail[5])  # booked date
    # pic_list = accommodation1.get_accom_pics
    review_list1 = []
    true_review1 = accommodation1.get_reviews
    for i in true_review1:
        review_list1.append(i.get_info())

    print(review_list1)
    return Html(
        Head(
            Title("Airbnb - Room"),
            Script(
                """
                let guestCount = 0;

            function increaseGuests() {
                if (guestCount < 10) {
                    guestCount++;
                    document.getElementById("guest-count").textContent = guestCount;
                    document.getElementById("guest-input").value = guestCount; // ✅ Update hidden input
                }
            }

            function decreaseGuests() {
                if (guestCount > 0) {
                    guestCount--;
                    document.getElementById("guest-count").textContent = guestCount;
                    document.getElementById("guest-input").value = guestCount; // ✅ Update hidden input
                }
            }

            function validateDates() {
                const occupiedDates = JSON.parse(document.getElementById('occupied-dates').innerText);  // Get the occupied dates from the hidden div
                
                const checkInDate = document.getElementById('check-in').value;  // Get the selected check-in date
                const checkOutDate = document.getElementById('check-out').value;  // Get the selected check-out date

                const checkInInput = document.getElementById('check-in');
                const checkOutInput = document.getElementById('check-out');

                // Reset the validity state to make sure any previous custom validity is cleared
                checkInInput.setCustomValidity('');
                checkOutInput.setCustomValidity('');

                // Disable dates in the check-out calendar before the selected check-in date
                if (checkInDate) {
                    checkOutInput.setAttribute('min', checkInDate);  // Set min date for check-out to the selected check-in date
                }

                // Check if the selected dates are in the occupied date range
                for (const [startDate, endDate] of occupiedDates) {
                    const start = new Date(startDate);
                    const end = new Date(endDate);

                    // Disable occupied check-in dates
                    if (checkInDate) {
                        const selectedCheckIn = new Date(checkInDate);
                        // If the selected check-in date is within an occupied range, mark it as invalid
                        if (selectedCheckIn >= start && selectedCheckIn <= end) {
                            checkInInput.setCustomValidity("Selected check-in date is already occupied.");
                        }
                    }

                    // Disable occupied check-out dates
                    if (checkOutDate) {
                        const selectedCheckOut = new Date(checkOutDate);
                        // If the selected check-out date is within an occupied range, mark it as invalid
                        if (selectedCheckOut >= start && selectedCheckOut <= end) {
                            checkOutInput.setCustomValidity("Selected check-out date is already occupied.");
                        }
                    }
                }

                // Additional validation to ensure check-out date is after check-in date
                if (checkInDate && checkOutDate && new Date(checkOutDate) <= new Date(checkInDate)) {
                    checkOutInput.setCustomValidity("Check-out date must be after check-in date.");
                }

                // If there are any custom validity messages, the form won't submit
                if (checkInInput.validationMessage || checkOutInput.validationMessage) {
                    return false;
                }
                return true;
            }
    """
            ),
            Style(
                """
                @import url('https://fonts.googleapis.com/css2?family=Fredoka:wdth,wght@95.9,346&family=Roboto:ital,wght@0,100..900;1,100..900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
                body,html {
                    font-family: 'Fredoka', sans-serif;
                    margin: 0;
                    padding: 0;
                    overflow-x: hidden;
                }
                * {
                    margin: 0;
                    padding: 0;
                }

                .header{
                background-color: none;
                    width: 100%;
                    
                    /* Added padding for spacing */
                    display: flex; /* Use flexbox for horizontal alignment */
                    justify-content: center; /* Space out logo and switch button */
                    align-items: center; /* Vertically center items */
                }
                .header-container {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    width: 50%;
                    padding: 10px 5%;
                    height:60px;
                    position: relative; /* Ensure it stays part of the document flow */
                }
                .logo-button{
                    background: none;
                    border: none;
                    cursor: pointer;
                    width: 50px;
                    height: 50px;
                }
                .right-button {
                    display: flex;
                    align-items: center;
                    gap: 10px; /* Space between Switch and Profile buttons */
                }
                .switch-button{
                background-color: white;
                    transition: all 0.3s;
                    font-family: 'Fredoka';
                    font-size: 16px;
                    border: none;
                    border-radius: 50px;
                    cursor: pointer;
                    width: 150px;
                    height: 38px;
                    
                }
                .switch-button:hover{
                background-color: #e7e7e7;
                }
                .profile-button{
                    
                    
                }
                .profile-button-ui{
                    width: 70px;
                    height: 38px;
                    border-radius: 50px;
                    border-color: #e7e7e7;
                    
                    border-width:1px;
                    transition: all 0.2s ease-in-out;
                    font-size: 20px;
                    font-family: Verdana, Geneva, Tahoma, sans-serif;
                    font-weight: 600;
                    display: flex;
                    align-items: center;
                    justify-content:center;
                    background: white;
                    color: #f5f5f5;
                }
                .profile-button-ui:hover{
                    
                    box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
                    
                }
                
                .gray-line{
                background-color: #ededed;
                    height: 1px; /* Set the height of the gray line */
                    width: 100%; /* Make the gray line span the full width */
                    margin: 0;
                    padding: 0;
                }
                .below-header{
                flex:1;
                display:flex;
                justify-content:center;
                align-items: center;
                align-content:center;
                }
                .Hotel-Name-Like{
                width:50%;
                background-color:none;
                display:flex;
                justify-content: center;
                align-items:center;
                                                                                                                                    
                padding: 20px;
                gap:20px;
                }
                .hotel-name{
                    flex-grow:1; 
                    flex-shrink:0;
                    font-size: 26px;
                    font-weight: bold;
                }
                
                .share-button, .like-button {
                transition: all 0.3s;
                display:flex;
                align-items: center;
                padding : 8px 12px;
                border-radius: 10px;
                    font-size: 14px;
                    cursor: pointer;
                gap:8px;
                }
                .share-button:hover, .like-button:hover{
                background-color: #e7e7e7;
                }
                .picture-section{
                    width: auto; 
                    background-color: white; /* Light gray background */
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    
                    
                

                
                }
                .inner-picture-section { 
                    display: grid;
                    grid-template-columns: 450px 180px 180px; /* First column (big image) takes 2 fractions, the others take 1 each */
                    grid-template-rows: 180px 180px; /* Two equal rows */
                    /* Add spacing between images */
                    width: auto;
                    grid-gap:5px;
                    grid-row-gap:5px;
                    background-color: none;
                }

                .inner-picture-section img { 
                    width: 100%;
                    height: 100%;
                    border-radius:10px;
                    
                }

                .big-image {
                    object-fit: cover;
                    grid-row: span 2; /* Make the first image span 2 rows */
                }

                .small-image {
                    width: 100%;
                    height: auto;
                    object-fit: cover;
                }
                /*Info Section*/
                .info-section{
                    width: 100%;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    align-content:center;
                    padding:0px 0px;
                    

                }
                .info-room{
                    width: 50%;
                    display:flex;
                    flex-direction:column;   
                    padding: 20px 0px;
                    gap:10px;
                    
                } 
                .address{
                    
                    font-size: 22px;
                    font-weight: bold;
                }
                .host-by-name{
                    
                    gap:10px;
                    display: flex;
                    
                }
                .name{
                    font-weight: bold;
                }
                .hotel-about-section{
                    background-color:none;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;

                    padding: 0px 0px;
                    width:100%;

            
                }
                .about-this-place{
                    width:50%;
                    padding: 0px 0px;
                    gap:10px;
                    font-weight:bold;
                }
                .about-text{
                    width:50%;
                    padding: 10px 0px;
                    gap:10px;
                }
                /*price-section*/
                .price-per-night{
                    font-weight:bold;
                    font-size:18px;
                }
                .price-section{
                    display:flex;
                    flex-wrap: wrap;
                    justify-content:center;
                    align-items:center;
                    
                    width:auto;
                    padding:50px 50px;
                }
                .price-box{
                    box-sizing: border-box;
                    border-style:solid;
                    border-color:white;
                    border-width:10px;
                    background-color:#fffaeb;
                    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
                    border-radius:10px;
                    padding:15px 15px;
                    width:25%;
                    display:flex;
                    flex-direction:column;
                }
                .in-out-date-select{
                    display:flex;
                    justify-content: center;
                    align-items:center;
                    gap:10px;
                    padding:10px;
            
                }
                
                /* guest + - button*/
                .guest-selection {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    margin-top: 10px;
                }

                .minus-btn, .plus-btn {
                    background-color: white;
                    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
                    color: black;
                    border: none;
                    font-size: 18px;
                    width: 30px;
                    height: 30px;
                    border-radius: 100%;
                    cursor: pointer;
                }

                .minus-btn:hover, .plus-btn:hover {
                    background-color: #e7e7e7;
                }

                .guest-count {
                    font-size: 18px;
                    font-weight: bold;
                    min-width: 20px;
                    text-align: center;
                }
            .total-price{
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    padding:15px 20px;
            } 
                .submit-button{
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    padding:20px 20px;
                }
                .submit-price-button{
                    box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
                    background-color: white;
                    transition: all 0.3s;
                    font-family: 'Fredoka';
                    font-size: 16px;
                    border: none;
                    border-radius: 50px;
                    cursor: pointer;
                    width: 150px;
                    height: 38px;
                }
                .submit-price-button:hover{
                background-color: #e7e7e7;
                }

                
                
                        
                            """
            ),
        ),
        Body(
            Div(
                Div(
                    A(
                        Button(
                            Img(
                                src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/800px-Airbnb_Logo_B%C3%A9lo.svg.png",
                                width=90,
                            ),
                            cls="logo-button",
                            # style="background: none; border: none; cursor: pointer; position: absolute; top: 20px; left: 25%; width:50px; height:50px"
                        ),
                        href="/",
                    ),
                    Div(
                        A(
                            Button("Switch to Hosting", cls="switch-button"),
                            href=f"/Hosting/{host_id}",
                        ),
                        Div(
                            Button(
                                Img(
                                    src="https://www.freeiconspng.com/thumbs/menu-icon/menu-icon-24.png",
                                    width=20,
                                ),
                                cls="profile-button-ui",
                            ),
                            cls="profile-button",
                        ),
                        cls="right-button",  # group switch button and profile button
                    ),
                    cls="header-container",
                ),
                cls="header",
            ),
            # grey line
            Div(cls="gray-line"),
            Div(
                Div(
                    Div(
                        detail[0],
                        cls="hotel-name",
                    ),
                    Div(
                        Img(
                            src="https://static-00.iconduck.com/assets.00/share-ios-icon-373x512-o947u0eq.png",
                            width=13,
                        ),
                        "Share",
                        cls="share-button",
                    ),
                    Div(
                        Img(
                            src="https://pngfre.com/wp-content/uploads/Black-Heart-2.png",
                            width=20,
                        ),
                        "Like",
                        cls="like-button",
                    ),
                    cls="Hotel-Name-Like",
                ),
                cls="below-header",
            ),
            #######################           Picture          ########################
            Div(
                Div(
                    Img(
                        src=pic_list[0],
                        cls="big-image",
                    ),
                    Div(
                        Img(
                            src=pic_list[1],
                            cls="small-image",
                        ),
                        Img(
                            src=pic_list[2],
                            cls="small-image",
                        ),
                    ),
                    Div(
                        Img(
                            src=pic_list[3],
                            cls="small-image",
                        ),
                        Img(
                            src=pic_list[4],
                            cls="small-image",
                        ),
                    ),
                    cls="inner-picture-section",
                ),
                cls="picture-section",
            ),
            ############################    Info    ###################################
            Div(
                Div(
                    Div(detail[2], cls="address"),
                    Div(
                        Div("Hosted by ", cls="host-by"),
                        Div(detail[1], cls="name"),
                        cls="host-by-name",
                    ),
                    cls="info-room",
                ),
                cls="info-section",
            ),
            Div(
                Div("About this place :", cls="about-this-place"),
                Div(
                    detail[3],
                    cls="about-text",
                ),
                cls="hotel-about-section",
            ),
            #######################price box###########################
            Div(
                Form(
                    Div(
                        f"{accommodation1.get_price} night",
                        Input(
                            type="hidden",
                            name="price-per-night",
                            value=f"{accommodation1.get_price}",
                        ),
                        cls="price-per-night",
                    ),
                    Div(
                        Input(
                            type="date",
                            cls="check-in-date",
                            required=True,
                            id="check-in",
                            name="check-in",
                            onchange="validateDates()",
                        ),
                        Input(
                            type="date",
                            cls="check-out-date",
                            required=True,
                            id="check-out",
                            name="check-out",
                            onchange="validateDates()",
                        ),
                        cls="in-out-date-select",
                    ),
                    Div(
                        "Guests :",
                        Button(
                            "-",
                            cls="minus-btn",
                            onclick="decreaseGuests()",
                            type="button",
                        ),
                        Span("0", id="guest-count", cls="guest-count"),
                        Button(
                            "+",
                            cls="plus-btn",
                            onclick="increaseGuests()",
                            type="button",
                        ),
                        # ✅ Hidden input to store guest count
                        Input(
                            type="hidden",
                            name="guest-count",
                            id="guest-input",  # This will be updated dynamically
                            value="0",
                        ),
                        cls="guest-selection",
                    ),
                    # Div("", cls="total-price"),
                    Div(
                        Button(
                            "Submit",
                            type="submit",
                            cls="submit-price-button",
                            id="submit-btn",
                        ),
                        cls="submit-button",
                    ),
                    # ✅ เพิ่ม div ซ่อนค่า occupied_dates ไว้
                    # Div(
                    #     json.dumps(detail[5]),
                    #     id="occupied-dates",
                    #     style="display:none;",
                    # ),
                    cls="price-box",
                    method="post",
                    action=f"/price_summary/{user_id}/{accom_id}",
                ),
                cls="price-section",
            ),
        ),
    )

@rt("/Hosting/{user_id}")
def host(user_id: int, req):
    user_id = req.session.get("user_id")
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
    request: Request
):
    controlsystem = app.state.control_system
    user_id = request.session.get("user_id")
    book_id = controlsystem.get_html_create_booking(user_id, check_in, check_out, accom_id, total_price, guests)
    return Redirect(f"/booking/{book_id}")
    #-----
    
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
def post(name: str, email: str, phone_num: str, password: str, age, req):
    control = app.state.control_system
    result = control.create_account(name, email, password, phone_num, age)
    user_id = control.get_member_id(name, email, phone_num, password)
    if not user_id:
        return Div(H1("Error: Could not retrieve user ID"), A(Button("Try Again"), href="/sign_up"))
    # return Div(H1(f"create Account {result} and yor id is {id}", style="""
    #                 background-color:white;
    #                 color:black;"""),
    #            Form(
    #                Input(type="hidden", name="user_id", value=id),
    #                Button("Home", type="submit", style="width:50%"),
    #                method="post",
    #                action="/",
                   
    #            ),
    #         #    A(Button("Home"), href=f"/"),
    #            style="""
    #                 background-color:white;
    #                 color:black;
    #                 display: flex;
    #                 flex-direction: column;
    #                 align-items: center;
    #                 justify-content: center;
    #                 text-align: center;
    #                 height:100vh;
    #                 """)
    # TODO: redirect to home with session
    # Store user_id in session
    req.session["user_id"] = str(user_id)  # Convert to string for session storage
    return RedirectResponse("/", status_code=303)

@rt('/log_in')
def get():
    return Div(
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
        height:60px;
        align-items: center;
        """
        ),
        Div(H1("Log in", style="padding-top:20%"),
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
            Button("Log in", type="submit", style="width:50%"), Hr("Or"),
            method="post",
            action="/check_for_log_in",
            style="padding:15px;width:100%"

        ),
            style="""
    background-color:white;
    padding-top:30vh
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
    ), Div(A(Button("Sign Up"), href="/sign_up",
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

@rt('/check_for_log_in')
async def post(req):
    form_data = await req.form()
    name = form_data.get('name')
    email = form_data.get('email')
    phone_num = form_data.get('phone_num')
    password = form_data.get('password')
    
    control = app.state.control_system
    user_id = control.get_member_id(name, email, phone_num, password)
    if not user_id:
        return Div(H1("Error: Login Fail"), A(Button("Try Again"), href="/log_in"))
     
    req.session["user_id"] = str(user_id)
    return RedirectResponse("/", status_code=303)

@rt('/logout')
def get(req):
    req.session.clear()  # Clear the session
    return RedirectResponse("/log_in", status_code=303)

@rt("/price_summary/{user_id}/{accom_id}", methods=["POST"])
async def post(user_id: int, accom_id: int, request: Request):
    user_id = request.session.get("user_id")
    print(f"accom id in price = {accom_id}")
    controlsystem = app.state.control_system
    accom_name = controlsystem.search_accomodation_by_id(accom_id).get_acc_name
    accom_address = controlsystem.search_accom_by_id(accom_id).get_address
    # print(accom_name)
    form_data = (
        await request.form()
    )  # ✅ Retrieve the submitted form data # wait until the form data is available

    # ✅ Extract values from the form
    price_per_night = form_data.get("price-per-night")
    check_in = form_data.get("check-in")
    check_out = form_data.get("check-out")
    guests = form_data.get("guest-count")
    check_in_date = datetime.strptime(form_data.get("check-in"), "%Y-%m-%d")
    check_out_date = datetime.strptime(form_data.get("check-out"), "%Y-%m-%d")
    guests_int = int(form_data.get("guest-count"))
    # print(check_in)
    # print(check_out)
    total_price = controlsystem.find_total_price(
        accom_id, check_in_date, check_out_date, guests_int
    )
    print(total_price)
    return Html(
        Head(
            Title("Airbnb - Confirm Pay"),
            Style(
                """
                @import url('https://fonts.googleapis.com/css2?family=Fredoka:wdth,wght@95.9,346&family=Roboto:ital,wght@0,100..900;1,100..900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
                body,html {
                    font-family: 'Fredoka', sans-serif;
                    margin: 0;
                    padding: 0;
                    overflow-x: hidden;
                }
                * {
                    margin: 0;
                    padding: 0;
                }

                .header{
                   background-color: none;
                    width: 100%;
                    
                     /* Added padding for spacing */
                    display: flex; /* Use flexbox for horizontal alignment */
                    justify-content: center; /* Space out logo and switch button */
                    align-items: center; /* Vertically center items */
                  }
                  .header-container {
                    
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    width: 100%;
                    padding: 10px 5%;
                    height:60px;
                    position: relative; /* Ensure it stays part of the document flow */
                }
                .logo-button{
                    background: none;
                    border: none;
                    cursor: pointer;
                    width: 50px;
                    height: 50px;
                  }
                .gray-line{
                  background-color: #ededed;
                    height: 1px; /* Set the height of the gray line */
                    width: 100%; /* Make the gray line span the full width */
                    margin: 0;
                    padding: 0;
                  }
                .price-section{
                    display:flex;
                    flex-wrap: wrap;
                    justify-content:center;
                    align-items:center;
                    
                    width:auto;
                    padding:50px 50px;
                }
                .price-box{
                    gap:20px;
                    box-sizing: border-box;
                    border-style:solid;
                    border-color:white;
                    border-width:10px;
                    background-color:#fffaeb;
                    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
                    border-radius:10px;
                    padding:15px 15px;
                    width:25%;
                    display:flex;
                    flex-direction:column;
                }
                .accom-name{
                    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
                    border-radius:10px;
                    font-size:20px;
                    font-weight:bold;
                    background-color:#ffffff;
                    padding:20px;
                }
                .line{
                    border: none; /* Removes default border */
                    border-top: 2px solid #ededed; /* Change color and thickness */
                    
                
                }
                .total-price{
                    font-size:20px;
                    font-weight:bold;
                    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
                    border-radius:10px;
                    font-size:20px;
                    font-weight:bold;
                    background-color:#ffffff;
                    padding:20px;
                }
                .form-shit{
                    gap:20px;
                    display:flex;
                    justify-content:center;
                    flex-direction:column;
                }
                .reserve-shit{
                    
                }
                  """
            ),
        ),
        Body(
            Div(
                Div(
                    A(
                        Button(
                            Img(
                                src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/800px-Airbnb_Logo_B%C3%A9lo.svg.png",
                                width=90,
                            ),
                            cls="logo-button",
                            # style="background: none; border: none; cursor: pointer; position: absolute; top: 20px; left: 25%; width:50px; height:50px"
                        ),
                        href="/",
                    ),
                    cls="header-container",
                ),
                cls="header",
            ),
            # grey line
            Div(cls="gray-line"),
            Div(
                Div(
                    Form(
                        Div(f"{accom_name}, {accom_address}", cls="accom-name"),
                        Div(f"Price per night : {price_per_night} ฿"),
                        Hr(cls="line"),
                        Div(f"Check-in-date : {check_in}"),
                        Hr(cls="line"),
                        Div(f"Check-out-date : {check_out}"),
                        Hr(cls="line"),
                        Div(f"Guests : {guests}"),
                        Hr(cls="line"),
                        Div(f"Total Price: {total_price} ฿", cls="total-price"),
                        ######
                        Input(type="hidden", name="user_id", value=f"{user_id}"),
                        Input(type="hidden", name="check_in", value=f"{check_in}"),
                        Input(type="hidden", name="check_out", value=f"{check_out}"),
                        Input(type="hidden", name="accom_id", value=f"{accom_id}"),
                        Input(
                            type="hidden", name="total_price", value=f"{total_price}"
                        ),
                        Input(type="hidden", name="guests", value=f"{guests}"),
                        Button("Reserve", type="submit", cls="reserve-shit"),
                        method="post",
                        action=f"/create_booking",
                        cls="form-shit",
                    ),
                    cls="price-box",
                ),
                cls="price-section",
            ),
        ),
    )


if __name__ == "__main__":
    
    serve()