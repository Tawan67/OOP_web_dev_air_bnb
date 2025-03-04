from fasthtml.common import *
from datetime import datetime

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
        
    def search_accommodations(self, query):
    # If there's no search term, show everything
        if not query:
            return self.get_accommodation_list
        
        # Make the search term lowercase so we can match without worrying about capital letters
        search_term = query.lower()
        
        # Create an empty list to store our matching results
        matching_accommodations = []
        
        # Look at each accommodation one by one
        for accommodation in self.get_accommodation_list:
            # Get the name and address in lowercase
            name = accommodation.get_acc_name.lower()
            address = accommodation.get_address.lower()
            
            # Check if our search term is in the name OR address
            if search_term in name or search_term in address:
                # If we found a match, add it to our results
                matching_accommodations.append(accommodation)
        
        # Give back all the matches we found
        return matching_accommodations

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
    def get_name(self):
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

    def __init__(self, name, address, info, price):
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__status = False
        self.__accom_pics = []
        self.__info = info
        self.__host = None
        self.__price = price
        Accommodation.count_id += 1

    def add_accom_pics(self, pic):
        self.__accom_pics.append(pic)
        return "Success"
    
    def add_host(self, host):
        if not isinstance(host, Host):
            return "Error"
        else:
            self.__host = host
            return "Success"
        
    def cal_price(self, start_date, end_date):
        # Convert HTML date strings (e.g., "2025-03-01") to datetime objects
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Calculate the difference in days
        day_count = (end - start).days
        
        # Ensure day_count is positive and makes sense
        if day_count <= 0:
            return "Error: End date must be after start date"
        
        # Calculate total price
        total_price = (day_count+1) * self.__price
        return total_price
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
    def get_host(self):
        return self.__host

class House(Accommodation):
    def __init__(self, name, address, info, price):
        super().__init__(name, address, info, price)
        self.__price = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price

class Hotel(Accommodation):
    def __init__(self, name, address, info):
        super().__init__(name, address, info, price=0)
        self.__rooms = []

    @property
    def get_price(self):
        price_list = []
        for x in self.__rooms:
            price_list.append(x.get_price)
        return price_list
    
    def add_room(self, room):
        if not isinstance(room, Room):
            return "Error"
        else:
            self.__rooms.append(room)
            return "Success"
        
    def cal_price(self, start_date, end_date):
        price_list = []
        for room in self.__rooms:
            price = room.cal_price(start_date, end_date)
            price_list.append(price)
        return price_list

class Room(Accommodation):
    
    def __init__(self, room_id, room_floor, price, hotel_address, hotel_name): 
        # FIXME:
        super().__init__(
            name=f"Room {room_id}",
            address=f"{hotel_address} - Floor {room_floor}",
            info=f"Room in {hotel_name}",
            price=price
        )
        self.__room_id = room_id
        self.__room_floor = room_floor
        self.__price_per_day = price
        self.__booked_date = []

    @property
    def get_price(self):
        return self.__price_per_day



def add_accomodation(control_system):
    # Create first test Host instance
    test_host1 = Host(
        name="John Doe",
        email="john.doe@example.com",
        password="securepass123",
        phone_num="123-456-7890",
        age=35
    )

    # Create second test Host instance
    test_host2 = Host(
        name="Jane Smith",
        email="jane.smith@example.com",
        password="password456",
        phone_num="987-654-3210",
        age=28
    )

    # Create first test House instance
    test_house1 = House(
        name="Cozy Cottage",
        address="123 Forest Lane, Natureville",
        info="A charming cottage in the woods",
        price=150.00
    )
    test_house1.add_accom_pics("https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    test_house1.add_host(test_host1)

    # Create second test House instance
    test_house2 = House(
        name="Beach Bungalow",
        address="789 Ocean Drive, Beachside",
        info="A relaxing beachfront property",
        price=200.00
    )
    test_house2.add_accom_pics("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJxo2NFiYcR35GzCk5T3nxA7rGlSsXvIfJwg&s")

    # Create first test Hotel instance
    test_hotel1 = Hotel(
        name="Grand Hotel",
        address="456 City Ave, Metropolis",
        info="A luxurious downtown hotel"
    )
    test_hotel1.add_accom_pics("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg")
    test_hotel1.add_host(test_host2)
    # Create second test Hotel instance
    test_hotel2 = Hotel(
        name="Mountain Lodge",
        address="101 Ridge Road, Peakville",
        info="A cozy hotel with mountain views"
    )
    test_hotel2.add_accom_pics("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc9APxkj0xClmrU3PpMZglHQkx446nQPG6lA&s")

    # Create test Room instances for Grand Hotel
    test_room1 = Room(
        room_id="R101",
        room_floor=1,
        price=120.00,
        hotel_address="456 City Ave, Metropolis",
        hotel_name="Grand Hotel"
    )
    test_room1.add_accom_pics("https://via.placeholder.com/300x200?text=Room+101")

    test_room2 = Room(
        room_id="R202",
        room_floor=2,
        price=150.00,
        hotel_address="456 City Ave, Metropolis",
        hotel_name="Grand Hotel"
    )
    test_room2.add_accom_pics("https://via.placeholder.com/300x200?text=Room+202")

    # Create test Room instance for Mountain Lodge
    test_room3 = Room(
        room_id="M101",
        room_floor=1,
        price=130.00,
        hotel_address="101 Ridge Road, Peakville",
        hotel_name="Mountain Lodge"
    )
    test_room3.add_accom_pics("https://via.placeholder.com/300x200?text=Room+M101")

    # Add rooms to their respective hotels
    test_hotel1.add_room(test_room1)
    test_hotel1.add_room(test_room2)
    test_hotel2.add_room(test_room3)

    # Add accommodations to hosts' lists
    test_host1.add_accommodation([test_house1, test_hotel1])
    test_host2.add_accommodation([test_house2, test_hotel2])

    # Store in ControlSystem
    control_system.add_host(test_host1)
    control_system.add_host(test_host2)
    control_system.add_accommodation(test_house1)
    control_system.add_accommodation(test_house2)
    control_system.add_accommodation(test_hotel1)
    control_system.add_accommodation(test_hotel2)
    # Note: Rooms are not added directly to control_system since they're part of hotels

    return "Test hosts, houses, and hotels with rooms added successfully"


# Define the FastHTML app
app, rt = fast_app(static_dir="static")

# Enhanced CSS with card and image styling
css = """
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
    .header { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 1px solid #ddd; }
    .logo { font-size: 24px; font-weight: bold; color: #ff385c; }
    .nav-menu { display: flex; gap: 20px; }
    .nav-menu a { text-decoration: none; color: #222; font-weight: 500; }
    .nav-menu a:hover { color: #ff385c; }
    .search-bar { 
        display: flex; 
        align-items: center; 
        border: 1px solid #ddd; 
        border-radius: 40px; 
        padding: 10px 20px; 
        width: 100%; 
        max-width: 600px; /* Increased from 300px to 600px */
        gap: 10px; /* Added spacing between elements */
    }
    .search-bar input[type="text"] { 
        border: none; 
        outline: none; 
        flex-grow: 1; /* Allows text input to take available space */
        font-size: 16px; 
        min-width: 150px; /* Ensures text input has a minimum size */
    }
    .search-bar input[type="date"] { 
        border: none; 
        outline: none; 
        font-size: 14px; 
        padding: 5px; 
    }
    .search-bar button { 
        border: none; 
        background: #ff385c; 
        color: white; 
        padding: 8px 16px; 
        border-radius: 20px; 
        cursor: pointer; 
        white-space: nowrap; /* Prevents button text from wrapping */
    }
    .user-menu { display: flex; align-items: center; gap: 15px; }
    .user-icon { width: 30px; height: 30px; background-color: #ddd; border-radius: 50%; }
    .container { padding: 20px; display: flex; flex-wrap: wrap; gap: 20px; }
    .card { border: 1px solid #ddd; border-radius: 8px; width: 300px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .card img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px 8px 0 0; margin-bottom: 10px; }
    .card h3 { margin: 0 0 10px; color: #222; }
    .card p { margin: 5px 0; color: #555; }
    .search-results { padding: 20px; }
    .no-results { color: #555; font-style: italic; }
"""

# Create an instance of ControlSystem
control_system = ControlSystem()

# Add test data
add_accomodation(control_system)

# Define the route for the homepage
@rt("/")
def get():
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
                    A("Airbnb", cls="logo", href="/"),
                    Nav(
                        A("Stays", href="#"),
                        A("Experiences", href="#"),
                        A("Online Experiences", href="#"),
                        cls="nav-menu"
                    ),
                    Div(
                        Form(
                            Input(type="text", name="query", placeholder="Where are you going?"),
                            Input(type="date", name="check_in", style="margin-right: 10px;"),
                            Input(type="date", name="check_out", style="margin-right: 10px;"),
                            Button("Search", type="submit"),
                            action="/search",
                            method="get",
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
                    *[Div(
                        Img(src=accom.get_accom_pics[0]),
                        H3(accom.get_acc_name),
                        P(f"Address: {accom.get_address}"),
                        P(f"ID: {accom.get_id}"),
                        P(f"Price: {accom.get_price}/night"),
                        P(f"Host: {accom.get_host.get_name if accom.get_host else 'No host assigned'}"),
                        cls="card"
                    ) for accom in control_system.get_accommodation_list],
                    cls="container"
                )
            )
        )
    )

# Define the search results route
@rt("/search")
def get(query: str, check_in: str, check_out: str):
    results = control_system.search_accommodations(query)
    
    # Generate search results content
    if results:
        results_content = [
            Div(
                Img(src=accom.get_accom_pics[0]),
                H3(accom.get_acc_name),
                P(f"Address: {accom.get_address}"),
                P(f"ID: {accom.get_id}"),
                P(f"Price: {accom.cal_price(check_in, check_out)}"),
                P(f"Host: {accom.get_host.get_name if accom.get_host else 'No host assigned'}"),
                cls="card"
            )
            for accom in results
        ]
    else:
        results_content = [P("No results found for your search.", cls="no-results")]

    return (
        Html(
            Head(
                Meta(charset="UTF-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Title(f"Search Results for '{query}' - Airbnb"),
                Style(css)
            ),
            Body(
                Header(
                    A("Airbnb", cls="logo", href="/"),
                    Nav(
                        A("Stays", href="#"),
                        A("Experiences", href="#"),
                        A("Online Experiences", href="#"),
                        cls="nav-menu"
                    ),
                    Div(
                        Form(
                            Input(type="text", name="query", placeholder="Where are you going?"),
                            Input(type="date", name="check_in", style="margin-right: 10px;"),
                            Input(type="date", name="check_out", style="margin-right: 10px;"),
                            Button("Search", type="submit"),
                            action="/search",
                            method="get",
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
                    H2(f"Search Results for '{query}', from {check_in} to {check_out}"),
                    Div(*results_content, cls="container"),
                    cls="search-results"
                )
            )
        )
    )

# Run the app
if __name__ == "__main__":
    serve()