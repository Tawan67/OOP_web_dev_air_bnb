from fasthtml.common import *
from datetime import datetime, timedelta
from calendar import monthrange, weekday

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
