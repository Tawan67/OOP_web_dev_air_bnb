
class ControlSystem:
    def __init__(self):
        self.__booking_list = []
        self.__member_list = []
        self.__host_list = []
        self.__accommodation_list = []  # stored hotel, house
        self.__paymentmethod = None
        # self.__balance = None ไม่ควรมี เพราะ ค่านี้คสวรอยู่ใน paymed

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
        from .User import User
        if not isinstance(host, User):
            return "Error"
        else:
            self.__host_list.append(host)  # t
            return "Success"

    def add_accommodation(self, accommodation):  # t
        from .Accommodation import Accommodation
        if not isinstance(accommodation, Accommodation):
            return "Error"
        else:
            self.__accommodation_list.append(accommodation)
            return "Success"

    def update_payment_method(self, input1):  # tdkko
        self.__paymentmethod = input1
        return "Success"

    # def search_member_by_id(self, id):
    #     for member in self.get_member_list:
    #         if id == member.get_user_id:
    #             return member, id
    #     return "cant find"

    def add_booking(self, booking):
        from .Booking import Booking
        if not isinstance(booking, Booking):
            return "Error"
        else:
            self.__booking_list.append(booking)
            return "Success"

    def add_member(self, member):  # k0
        from .User import Member
        if not isinstance(member, Member):
            return "Error"
        else:
            self.__member_list.append(member)
            return "Success"

    def search_member_by_id(self, user_id):
        for member in self.get_member_list:
            if user_id == member.get_user_id:
                return member
        return "cant find"

    def search_accom_by_id(self, accom_id):  # 1
        for i in self.__accommodation_list:
            if i.get_id == accom_id:
                return i
        return "Not Found"

# FIXME:
# ----------------------------------------------- downnnnnnnn
    def create_booking(self, accom, date, guess, member):
        # Check availability first
        if not self.check_accom_available(accom.get_id, date.get_checkindate, date.get_checkoutdate):
            return "Error: Accommodation not available for these dates"

        if accom == "Not Found":
            return "Error: Accommodation not found"
        # Create the booking
        from .Booking import Booking
        new_booking = Booking(accom=accom, date=date, guess=guess,
                              member=member)
        self.__booking_list.append(new_booking)

        # Add the booked dates to the accommodation
        # booked_date = BookedDate(check_in, check_out)
        # accom.add_booked_date(booked_date)
        return f"Booking created successfully Accommodation:{new_booking.get_accommodation.get_acc_name}"
# ---------------------------------------------------

    """
    def create_booking(self, date, guest_amount, accom_id, price, member_id):
        from .Booking import Booking
        member = self.search_member_by_id(member_id)
        accom = self.search_accom_by_id(accom_id)
        booking_item = Booking(accom=accom, date=date,
                               guess=guest_amount, member=member)
        self.add_booking(booking_item)
        pass
    """
# --------------------------------------------------^^^^^^^

    def search_booking_by_user(self, user):
        if not isinstance(user, User):
            return "Error"
        all_booking = []
        for booking in self.get_booking_list:
            if user == booking.get_member:
                all_booking.append(booking)
        return all_booking

    # ----------------------------------------------=tord1 downnnnnnnn

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
    # ----------------------------------------------=tord1 ^^^^^^^^^

    def search_booking_by_id(self, booking_id):
        for booking in self.get_booking_list:
            if booking_id == booking.get_booking_id:
                return booking
        return "cant find"

    def create_account(self, name: str, email: str, password: str, phone: str, age: int):  # dew
        acount = Member(name=name, email=email,
                        password=password, phone_num=phone, age=age)
        self.add_member(acount)
        pass

    def check_accom_available(self, accom_id, requested_check_in, requested_check_out):
        # Find the accommodation
        accom = self.search_accom_by_id(accom_id)
        if accom == "Not Found":
            return False

            # Check for overlap with existing booked dates
        for booked_date in accom.get_booked_date:
            existing_check_in = booked_date.get_checkindate()
            existing_check_out = booked_date.get_checkoutdate()

            # Overlap condition: if the requested range intersects with an existing range
            if (requested_check_in < existing_check_out) and (requested_check_out > existing_check_in):
                return False  # Not available
        return True  # Available
# ---------------------------------------------- cal toartal price

    def cal_price_in_accom(self, accom_id, guest, start_date, end_date):
        accom = self.search_accom_by_id(accom_id=accom_id)
        price = accom.cal_price(guest, start_date, end_date)
        return price
# -----------------------------------------------

    def find_total_price(self, accom_id, start_date, end_date, guest_amount):
        accommodation = self.search_accomodation_by_id(accom_id)
        if isinstance(accommodation, House):
            total_price = accommodation.get_price_accom(
                start_date, end_date, guest_amount
            )
            return total_price
        elif isinstance(accommodation, Hotel):
            for room in accommodation.get_rooms:
                if room.get_id == accom_id:
                    return room.get_price_accom(start_date, end_date, guest_amount)
        return None
# -----------------------------------------------------

    def search_host_by_accom(self, accom):
        if not isinstance(accom, Accommodation):
            return "Error"
        for host in self.get_host_list:
            for acc_in_host in host.get_accommodation:
                if accom == acc_in_host:
                    return host
        return "Not Found"
    # get accom detail

    def search_accom_detail(self, accom_id):
        accommodation = self.search_accomodation_by_id(accom_id)
        if accommodation == "Not Found":
            return "Accommodation not found"

        host = self.search_host_by_accom(accommodation)
        if host == "Not Found":
            return "Host not found"
        host_name = host.get_user_name
        accom_name = accommodation.get_acc_name
        accom_address = accommodation.get_address
        accom_info = accommodation.get_info
        accom_list_pic = accommodation.get_accom_pics
        # show occupied date of that accom to user
        occupied_dates = []
        for booking in self.__booking_list:
            if booking.get_accommodation == accommodation:
                booking_date = booking.get_booking_date
                occupied_dates.append(
                    (booking_date.get_checkin_date, booking_date.get_checkout_date)
                )

        return (
            accom_name,
            host_name,
            accom_address,
            accom_info,
            accom_list_pic,
            occupied_dates,
        )
        pass

    def search_accomodation_by_id(self, accom_id):
        for accom in self.__accommodation_list:
            if accom.get_id == accom_id:
                return accom
        return "Not Found"

    def search_host_by_id(self, user_id):
        for host in self.__host_list:
            if host.get_user_id == user_id:
                return host.get_host_name
        pass

    def search_user_to_check(self, user_name, phone, email, password, age):  # dew not sure
        for member in self.__member_list:
            if member.get_phone_num == phone and member.get_user_nane == user_name and member.get_email == email:
                return "You have an Account, Wanna Login?"
        try:
            self.create_account(name=user_name, email=email,
                                password=password, age=age)
            return "Success"
        except:
            return "Sign up Fail"
        pass  # search for check if user want to sign up

    # korn does it really needed?
    def search_host_by_id_get_accom(self, user_id):
        that_host = None
        for host in self.__host_list:
            if host.get_user_id == user_id:
                that_host = host
                break
        if that_host is None:
            return "Host Not Found"
        my_accom_list = that_host.get_accommodation
        accom_list = [
            {"name": myaccom.get_acc_name, "address ": myaccom.get_address}
            for myaccom in my_accom_list
        ]
        return accom_list

    def search_coupon_by_user_id(self, user_id):
        user = self.search_member_by_id(user_id)
        coupons = user.get_coupons
        result = self.show_coupon(coupons)
        return result

    def show_coupon(self, coupons):
        result = []
        for cou in coupons:
            if cou.check_expirat():
                result.append(cou.get_info())
        return result
        # for show all coupon on UI
        pass

    def search_host_by_id_get_review(self, user_id):  # korn
        that_host = None
        for host in self.__host_list:
            if host.get_user_id == user_id:
                that_host = host
                break
        if that_host is None:
            return "Host Not Found"

        my_accom_list = that_host.get_accommodation
        review_list = []
        for accom in my_accom_list:
            for review in accom.get_reviews:
                review_list.append(
                    {
                        "accommodation": accom.get_acc_name,
                        "rating": review.get_rating,
                        "user": review.get_user.get_user_name,
                        "message": review.get_message,
                    }
                )
        return review_list

    def create_payment(self, price, period, paymed, booking_id):
        booking_item = self.search_booking_by_id(booking_id=booking_id)
        payment = booking_item.create_payment(price, period, paymed)
        result = self.update_booking_pay(payment)
        return result
        pass  # call Booking to create

    def create_payment_med(self, details):
        details = "".join(i for i in details if i != '"')
        card_id, user, balance, password = details.split(",")
        balance = int(balance)
        user = self.search_member_by_id(user)
        pay_med = Debit(card_id, user, balance, password)
        return pay_med
        # key use
        # cal member to create and put on Booking after create
        pass

    def update_booking_payment(self, booking_id, payment):
        booking = self.search_booking_by_id(booking_id=booking_id)
        result = booking.update_payment(payment)
        # to put payment and pay_med into Booking
        pass

    def update_booking_pay_med(self, booking_id, paymed):
        booking = self.search_booking_by_id(booking_id=booking_id)
        result = booking.update_pay_med(paymed)
        return result
        pass
