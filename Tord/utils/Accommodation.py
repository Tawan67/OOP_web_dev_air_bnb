from datetime import datetime


class Accommodation:
    count_id = 1

    def __init__(
        self,
        name,
        address,
        info,
        price,
        pic="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    ):
        self.__id = Accommodation.count_id
        self.__accom_name = name
        self.__address = address
        self.__info = info
        self.__price = price
        self.__status = False
        self.__accom_pics = []
        self.__accom_pics.append(pic)
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
        from .Booking import BookedDate

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

    def create_review(self, rating, user, message):
        try:
            my_review = Review(rating, user, message)
            for i in self.__reviews:
                if i.get_user == user:
                    self.__reviews.remove(i)
                    self.__reviews.append(my_review)
                    return "Update Complete"
            self.add_review(my_review)
            return "Added Complete"
            pass
        except:
            return "Wrong Type Review"

    def cal_price_not_fee(self, start_date, end_date):
        # Convert HTML date strings (e.g., "2025-03-01") to datetime objects
        if not isinstance(start_date, datetime):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if not isinstance(end_date, datetime):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        # Calculate the difference in days
        day_count = (end_date - start_date).days

        # Ensure day_count is positive and makes sense
        if day_count <= 0:
            return "Error: End date must be after start date"

        # Calculate total price
        total_price = day_count * self.__price
        return total_price

    def cal_price_accom(self, start_date, end_date, guest_amount=1):
        if isinstance(start_date, str):
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("start_date must be in 'YYYY-MM-DD' format")

        if isinstance(end_date, str):
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("end_date must be in 'YYYY-MM-DD' format")

        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError("Dates must be datetime objects or valid date strings")

        if end_date <= start_date:
            raise ValueError("end_date must be after start_date")

        days_between = (end_date - start_date).days + 1

        base_price = days_between * self.get_price

        service_fee = base_price * 0.05 * guest_amount

        total_price = base_price + service_fee

        return total_price

    def get_price_accom(self, start_date, end_date, guest_amount, get_fee=False):
        day_between = (end_date - start_date).days
        total_price = (day_between) * self.get_price
        fee = (total_price * (5 / 100)) * guest_amount
        total_price = total_price + fee
        if get_fee:
            return fee
        return total_price

    @property
    def get_status(self):
        return self.__status

    # def clear_accom_pics(self):
    #     self.__accom_pics = []

    # -----------------------------------------------------------------------------

    @property
    def get_info(self):
        return self.__info

    @property
    def get_price(self):
        return self.__price

    """ dew
    @property
    def get_one_price(self):
        return self.__price
    """

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
        # get_booked_date_by_id
        for x in self.__booked_date_list:
            list.append(x.to_string)
        return list

    @property
    def get_booked_date_list(self):  # change from get_booked_date
        return self.__booked_date_list

    """ dew
    @property
    def get_booked_date(self):
        return self.__booked_date
    """

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

    @property
    def get_booked_date(self, booked_date):
        from .Booking import BookedDate

        if not isinstance(booked_date, BookedDate):
            return "Error"
        else:
            for booked in self.get_booked_date_list:
                if booked_date == booked:
                    return booked
            return "Cant find"

    def update_status(self) -> str:
        self.__status = not self.__status
        return "Success"

    def clear_accom_pics(self):  # ✅ Add this method
        self.__accom_pics = []


#


class House(Accommodation):
    def __init__(
        self,
        name,
        address,
        info,
        price,
        pic="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    ):
        super().__init__(name, address, info, price, pic)

    def cal_price(self, start_date, end_date):
        return self.cal_price_accom(start_date, end_date)

    def __str__(self):
        return f"House: {self.get_acc_name}, Address: {self.get_address}, Price: {self.get_price}"


class Hotel(Accommodation):
    room_id = 1  # Class variable to track room IDs globally

    def __init__(
        self,
        name,
        address,
        info,
        pic="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    ):
        super().__init__(name, address, info, price=0, pic=pic)
        self.__rooms = []

    def cal_price(self, start_date, end_date, guest_amount=1):
        if isinstance(start_date, str):
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("start_date must be in 'YYYY-MM-DD' format")

        if isinstance(end_date, str):
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("end_date must be in 'YYYY-MM-DD' format")

        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError("Dates must be datetime objects or valid date strings")

        if end_date <= start_date:
            raise ValueError("end_date must be after start_date")

        days_between = (end_date - start_date).days
        price_list = []
        for room in self.__rooms:
            price = room.cal_price_accom(start_date, end_date, guest_amount)
            price_list.append(price)
        return price_list

    def add_room(self, price, room_type, hotel_address, hotel_name, number_of_room):
        """Create a new room and assign an auto-incrementing room_id"""
        for _ in range(number_of_room):  # Ensure it loops the correct number of times
            new_room = Room(Hotel.room_id, room_type, price, hotel_address, hotel_name)
            self.__rooms.append(new_room)
            Hotel.room_id += 1  # Increment room_id for the next room
            print(new_room)
        print(self.__rooms)
        return "Success"

    def cal_price(self, start_date, end_date):
        price_list = []
        for room in self.__rooms:
            price = room.cal_price_accom(start_date, end_date)
            price_list.append(price)
        return price_list

    def __str__(self):
        return f"Hotel: {self.get_acc_name}, Address: {self.get_address}, Rooms: {[str(room) for room in self.get_rooms]}"

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
    def __init__(self, room_id, room_type, price, hotel_address, hotel_name):
        """Each room gets a unique room_id from the Hotel class"""
        super().__init__(
            name=f"Room {room_id}",
            address=f"{hotel_address} - Room Type {room_type}",
            info=f"Room in {hotel_name}",
            price=price,
        )

    @property
    def get_price(self):
        return self.__price

    @property
    def get_room_id(self):
        return self.__room_id

    def __str__(self):
        return f"Room: {self.get_acc_name}, Address: {self.get_address}, Price: {self.get_price}"


class Review:
    def __init__(self, rating: int, user, message):
        self.__rating = rating
        self.__user = user
        self.__message = message

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
