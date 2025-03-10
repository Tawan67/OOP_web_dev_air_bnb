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

# Initialize the app with SessionMiddleware
app, rt = fast_app(
    middleware=[
        Middleware(SessionMiddleware, secret_key="your-secret-key-here", max_age=3600)  # 1-hour session
    ]
)

# Setup function (unchanged)
def setup_app(app):
    print("=========================Start===============================")
    control_system = ControlSystem()
    app.state.control_system = control_system
    control_system.add_member_and_payment_method()
    control_system.add_accommodation_test()
    print("=========================End===============================")
    return control_system

setup_app(app)

# Login route (GET)
@rt('/log_in')
def get(req):
    return Div(
        Title("Booking 999"),
        Div(
            A(
                Img(
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/1200px-Airbnb_Logo_B%C3%A9lo.svg.png",
                    style="height: 60px; padding: 5px;"
                ),
                href="/"
            ),
            style="background-color:white; padding: 15px; height:60px; text-align: center;"
        ),
        Div(
            H1("Log in", style="padding-top:20%"),
            Form(
                Div(
                    Label("Name"),
                    Input(type="text", id="name", name="name", placeholder="Enter your name")
                ),
                Div(
                    Label("Email"),
                    Input(type="text", id="email", name="email", placeholder="Enter your email")
                ),
                Div(
                    Label("Phone Number"),
                    Input(type="text", id="phone_num", name="phone_num", placeholder="Enter your Phone Number")
                ),
                Div(
                    Label("Password"),
                    Input(type="password", id="password", name="password", placeholder="Enter your password")
                ),
                Button("Log in", type="submit"),
                method="post",  # Changed to POST for security
                action="/check_for_log_in",
                style="padding:15px; width:500px; display:flex; flex-direction:column; gap:10px;"
            ),
            style="background-color:white; margin:auto; padding-top:30vh; width:500px; height:70vh; text-align:center;"
        ),
        Div(
            A(Button("Sign Up"), href="/sign_up"),
            style="background-color:white; height:30vh; display:flex; justify-content:center; align-items:center;"
        )
    )

# Login check route (POST)
@rt('/check_for_log_in', methods=["POST"])
async def post(req):
    form_data = await req.form()
    name = form_data.get("name")
    email = form_data.get("email")
    phone_num = form_data.get("phone_num")
    password = form_data.get("password")
    
    control = app.state.control_system
    user_id = control.get_member_id(name, email, phone_num, password)
    
    if not user_id:
        return Div(H1("Error: Login Failed"), A(Button("Try Again"), href="/log_in"))
    
    # Store user_id in session
    req.session["user_id"] = str(user_id)  # Convert to string for session storage
    return RedirectResponse("/", status_code=303)

# Logout route
@rt('/logout')
def get(req):
    req.session.clear()  # Clear the session
    return RedirectResponse("/log_in", status_code=303)

# Index route (protected by session)
@rt('/')
def index(req):
    user_id = req.session.get("user_id")
    if not user_id:
        return RedirectResponse("/log_in", status_code=303)  # Redirect to login if not authenticated
    
    web_control_system = req.app.state.control_system
    return web_control_system.get_html_index(user_id)

# Example of a protected route
@rt("/booking_history/{user_id}")
def get(req, user_id: int):
    session_user_id = req.session.get("user_id")
    if not session_user_id or str(user_id) != session_user_id:
        return RedirectResponse("/log_in", status_code=303)  # Unauthorized access
    
    web_control_system = req.app.state.control_system
    return web_control_system.get_html_booking_history(user_id)

# Add this helper to check authentication in other routes
def require_auth(req):
    if "user_id" not in req.session:
        return RedirectResponse("/log_in", status_code=303)
    return req.session["user_id"]

# Example usage in another route
@rt("/payment/add")
async def add_payment(req):
    user_id = require_auth(req)
    if isinstance(user_id, RedirectResponse):
        return user_id
    
    web_control_system = req.app.state.control_system
    form_data = await req.form()
    web_user_id = form_data.get("user_id")
    return web_control_system.get_html_add_payment(web_user_id)

if __name__ == "__main__":
    serve()