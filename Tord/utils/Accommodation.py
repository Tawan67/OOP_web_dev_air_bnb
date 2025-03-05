from datetime import datetime

class Accommodation:
    count_id = 1

    def __init__(self, name, address, info, price):
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__info = info
        self.__price = price
        self.__status = False
        self.__accom_pics = []
        self.__booked_date_list = []
        self.__reviews = []
        self.__host = None
        Accommodation.count_id += 1

    def reset_increament(self):
        Accommodation.count_id = 1

    
    def add_booked_date(self, booked_date) -> str:
        from .Booking import BookedDate
        if not isinstance(booked_date, BookedDate):
            return "Error"
        self.__booked_date_list.append(booked_date)
        return "Success"

    def del_booked_date(self, target):
        if not isinstance(target, BookedDate):
            return "Error"
        self.__booked_date_list.remove(target)
        return "Success"

    def add_accom_pics(self, pic) -> str:
        self.__accom_pics.append(pic)
        return "Success"

    def update_status(self) -> str:
        self.__status = True
        return "Success"

    def add_review(self, review):
        if isinstance(review, Review):
            self.__reviews.append(review)
            return "Success"
        return "Invalid Review"

    def add_host(self, host):
        from .User import Host
        if not isinstance(host, Host):
            return "Error"
        else:
            self.__host = host
            return "Success"

# ------------------------------------------------------------------
    """
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
    """
# ----------------------------------------------------------------------

    def cal_price_accom(self, start_date, end_date, guest_amount):
        day_between = (end_date - start_date).days
        total_price = (day_between + 1) * self.get_price
        fee = (total_price * 5 / 100) * guest_amount
        total_price = total_price + fee
        return total_price

# -----------------------------------------------------------------------------

    @property
    def get_info(self):
        return self.__info

    @property
    def get_price(self):
        return self.__price

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
    def get_booked_date_string(self):
        list = []
        #get_booked_date_by_id
        for x in self.__booked_date_list:
            list.append(x.to_string)
        return list
    
    @property
    def get_booked_date(self):
        return self.__booked_date_list




    @property
    def get_reviews(self):
        return self.__reviews
    
    @property
    def get_host(self):
        return self.__host
    @property 
    def get_booked_date_by_id(self, id):
        for x in self.__booked_date_list:
            if x.get_id == id:
                return x

#


class House(Accommodation):
    def __init__(self, name, address, info, price):
        super().__init__(name, address, info, price)


class Hotel(Accommodation):
    def __init__(self, name, address, info):
        super().__init__(name, address, info, price=0)
        self.__rooms = []

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

    @property
    def get_price(self):
        price_list = []
        for x in self.__rooms:
            price_list.append(x.get_price)
        return price_list

    @property
    def get_rooms(self):
        return self.__rooms


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
        self.__booked_date = []

    # def get_price_accom(self, start_date, end_date, guest_amount):
    #     num_days = (end_date - start_date).days
    #     return num_days * self.__price_per_day


class Review:
    def __init__(self, rating: int, user, message):
        self.__rating = rating
        self.__user = user
        self.__message = message
        pass

    def get_info(self):
        return f"Review by {self.__user.get_user_name}: {self.__rating}/5 - {self.__message}"

    @property
    def get_rating(self):
        return self.__rating

    @property
    def get_user(self):
        return self.__user

    @property
    def get_message(self):
        return self.__message
