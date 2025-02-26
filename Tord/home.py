from fasthtml.common import *

# ControlSystem class (abbreviated)
class ControlSystem:
    def __init__(self):
        self.__booking_list = []
        self.__member_list = []
        self.__host_list = []
        self.__accommodation_list = [] # stored hotel, house
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

# User class
class User:
    count_id = 1

    def __init__(self, name, email, password):
        self.__user_id = User.count_id
        self.__user_name = name
        self.__email = email
        self.__password = password
        User.count_id += 1

    @property
    def get_user_id(self):
        return self.__user_id

    @property
    def get_user_name(self):
        return self.__user_name

# Host class
class Host(User):
    def __init__(self, name, email, password, phone_num, age):
        super().__init__(name, email, password)
        self.__phone_num = phone_num
        self.__age = age
        self.__pay_med = None
        self.__my_accommodation = []

    def add_accommodation(self, input1):
        self.__my_accommodation = input1
        return "Success"

    @property
    def get_phone_num(self):
        return self.__phone_num

    @property
    def get_age(self):
        return self.__age

# Accommodation class
class Accommodation:
    count_id = 1

    def __init__(self, name, address):
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__status = False
        self.__accom_pics = []
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

class House(Accommodation):
    def __init__(self, name, address, info, price):
        super().__init__(name, address, info)
        self.__price = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price

class Hotel:
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
    def __init__(self, room_id, room_floor, price):
        self.__room_id = room_id
        self.__room_floor = room_floor
        self.__price_per_day = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price_per_day



# Function to add test instances with images
def add_accomodation(control_system):
    # Create a test Host instance
    test_host = Host(
        name="John Doe",
        email="john.doe@example.com",
        password="securepass123",
        phone_num="123-456-7890",
        age=35
    )

    # Create multiple test Accommodation instances with sample image URLs
    test_accom1 = Accommodation(name="Cozy Cottage", address="123 Forest Lane, Natureville")
    test_accom1.add_accom_pics("https://via.placeholder.com/300x200?text=Cozy+Cottage")
    
    test_accom2 = Accommodation(name="Beach House", address="456 Ocean Drive, Seaside")
    test_accom2.add_accom_pics("https://via.placeholder.com/300x200?text=Beach+House")
    
    test_accom3 = Accommodation(name="City Loft", address="789 Urban St, Metropolis")
    test_accom3.add_accom_pics("https://via.placeholder.com/300x200?text=City+Loft")

    # Add accommodations to the host's list
    test_host.add_accommodation([test_accom1, test_accom2, test_accom3])

    # Store in ControlSystem
    control_system.add_host(test_host)
    control_system.add_accommodation(test_accom1)
    control_system.add_accommodation(test_accom2)
    control_system.add_accommodation(test_accom3)

    return "Test host and accommodations added successfully"

# Define the FastHTML app
app = FastHTML()

# Enhanced CSS with card and image styling
css = """
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
    .header { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 1px solid #ddd; }
    .logo { font-size: 24px; font-weight: bold; color: #ff385c; }
    .nav-menu { display: flex; gap: 20px; }
    .nav-menu a { text-decoration: none; color: #222; font-weight: 500; }
    .nav-menu a:hover { color: #ff385c; }
    .search-bar { display: flex; align-items: center; border: 1px solid #ddd; border-radius: 40px; padding: 10px 20px; max-width: 300px; }
    .search-bar input { border: none; outline: none; width: 100%; font-size: 16px; }
    .user-menu { display: flex; align-items: center; gap: 15px; }
    .user-icon { width: 30px; height: 30px; background-color: #ddd; border-radius: 50%; }
    .container { padding: 20px; display: flex; flex-wrap: wrap; gap: 20px; }
    .card { border: 1px solid #ddd; border-radius: 8px; width: 300px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .card img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px 8px 0 0; margin-bottom: 10px; }
    .card h3 { margin: 0 0 10px; color: #222; }
    .card p { margin: 5px 0; color: #555; }
"""

# Create an instance of ControlSystem
control_system = ControlSystem()

# Add test data
add_accomodation(control_system)

# Define the route for the homepage
@app.route("/")
def get():
    # Generate cards for each accommodation with an image
    accommodation_cards = [
        Div(
            Img(src=accom.get_accom_pics[0] if accom.get_accom_pics else "https://via.placeholder.com/300x200?text=No+Image"),
            H3(accom.get_acc_name),
            P(f"Address: {accom.get_address}"),
            P(f"ID: {accom.get_id}"),
            cls="card"
        )
        for accom in control_system.get_accommodation_list
    ]

    return (
        Html(
            Head(
                Meta(charset="UTF-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Title("Airbnb Menu Layout"),
                Style(css)
            ),
            Body(
                Header(
                    Div("Airbnb", cls="logo"),
                    Nav(
                        A("Stays", href="#"),
                        A("Experiences", href="#"),
                        A("Online Experiences", href="#"),
                        cls="nav-menu"
                    ),
                    Div(
                        Div(
                            Input(type="text", placeholder="Where are you going?"),
                            cls="search-bar"
                        ),
                        A("Become a Host", href="#"),
                        A("Help", href="#"),
                        Div(cls="user-icon"),
                        cls="user-menu"
                    ),
                    cls="header"
                ),
                Div(
                    *accommodation_cards,  # Unpack the list of cards
                    cls="container"
                )
            )
        )
    )

# Run the app
if __name__ == "__main__":
    serve()