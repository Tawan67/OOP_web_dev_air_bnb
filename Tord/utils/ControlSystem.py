from fasthtml.common import *


class ControlSystem:
    def __init__(self):
        self.__booking_list = []
        self.__member_list = []
        self.__host_list = []
        self.__accommodation_list = []  # stored hotel, house
        self.__payment_method_list = []
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

    def add_payment_method(self, input1):  # tdkko
        self.__payment_method_list.append(input1)
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
        
        if accom == "Not Found":
            return "Error: Accommodation not found"
        # Create the booking
        from .Booking import Booking
        new_booking = Booking(accom=accom, date=date, guess=guess,
                              member=member)
        self.__booking_list.append(new_booking)
        
        # Check availability 
        if not self.check_accom_available(new_booking):
            return "Error: Accommodation not available for these dates"
        
        print(new_booking)

        return new_booking
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

    def check_accom_available(self, booking):
        # Find the accommodation
        accom = booking.get_accommodation
        from .Accommodation import Accommodation
        if accom == "Not Found" and not isinstance(accom, Accommodation):
            return False

            # Check for overlap with existing booked dates
        for booked_date in accom.get_booked_date:
            existing_check_in = booked_date.get_checkindate
            existing_check_out = booked_date.get_checkoutdate

            # Overlap condition: if the requested range intersects with an existing range
            if (booking.get_date.get_checkindate < existing_check_out) and (booking.get_date.get_checkoutdate > existing_check_in):
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
                return host

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
    
    def process_payment(self, booking_id, web_paymenth_method, web_payment_owner_name):
        process_booking = self.search_booking_by_id(booking_id)
        process_payment_method = self.search_payment_method_by_id(web_paymenth_method)
        if process_payment_method == None:
            return self.get_html_payment_not_found(web_paymenth_method)
        # try:
        # except Exception as e:
        #     return Html(P(e))
        if (self.check_accom_available(process_booking)):              
            # deduction
            if web_payment_owner_name == process_payment_method.get_owner.get_user_name:
                process_payment_method.deduction(process_booking.cal_price())
            else:
                return self.get_html_payment_didnt_match(web_paymenth_method, web_payment_owner_name)
            
            # update accommodation
            booked_date = process_booking.get_date
            add_status = process_booking.get_accommodation.add_booked_date(booked_date)
            if add_status == "Error":
                return Html(P("add_booked_date fail"))
            
            # update member booking list
            process_booking.get_member.add_booking(process_booking)
            
            # return html success
            return self.get_html_purchase_sueccess()
        else:
            return self.get_html_accommodation_not_available()
        
    def search_payment_method_by_id(self, payment_method_id):
        for payment_method in self.__payment_method_list:
            if payment_method.get_bank_id == payment_method_id:
                return payment_method

    def get_html_payment_didnt_match(self, web_paymenth_method, web_payment_owner_name):
        return Html(
            Div(
                P("Payment Name and ID didn't match", 
                style="font-weight: 600; font-size: 18px; margin-bottom: 8px;"),
                P(f'Name: {web_payment_owner_name}',
                style="font-size: 16px; color: #484848; margin: 4px 0;"),
                P(f'Payment ID: {web_paymenth_method}',
                style="font-size: 16px; color: #484848;"),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #FF5A5F;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;"""
            )
        )

    def get_html_payment_not_found(self, web_paymenth_method):
        return Html(
            Div(
                P("Payment Method Not Found",
                style="font-weight: 600; font-size: 18px; margin-bottom: 8px;"),
                P(f'Payment ID: {web_paymenth_method}',
                style="font-size: 16px; color: #484848;"),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #FF5A5F;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;"""
            )
        )

    def get_html_purchase_sueccess(self):
        return Html(
            Div(
                P("Purchase Successful",
                style="font-weight: 600; font-size: 18px;"),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #008489;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;"""
            )
        )

    def get_html_accommodation_not_available(self):
        return Html(
            Div(
                P("Accommodation not available for these dates",
                style="font-weight: 600; font-size: 18px;"),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #FF5A5F;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;"""
            )
        )
        
    def generate_booking_html(self, result_booking, booking_id):
        try:
            return (
                Title("Request to Book"),
                Div(
                    H1("Request to Book"),
                    Form(
                        Div(
                            H3("Your Trip"),
                            Div(
                                P(f"Accommodation: {self.search_booking_by_id(booking_id).get_accommodation.get_acc_name}"),
                                style="margin-bottom: 15px;"
                            ),
                            Div(
                                P(f"Accommodation Booked Date: {self.search_booking_by_id(booking_id).get_accommodation.get_booked_date_string}"),
                                style="margin-bottom: 15px;"
                            ),
                            Div(
                                P(f"Check-in: {result_booking.get_date.get_checkindate}"),
                                style="margin-bottom: 15px;"
                            ),
                            Div(
                                P(f"Check-out: {result_booking.get_date.get_checkoutdate}"),
                                style="margin-bottom: 15px;"
                            ),
                            Div(
                                P(f"Guests: {result_booking.get_guess_amount}"),
                                style="margin-bottom: 15px;"
                            ),
                            Div(
                                P(f"Price: {result_booking.cal_price()}"),
                                style="margin-bottom: 15px;"
                            ),
                            style="border: 1px solid #ddd; padding: 20px; border-radius: 5px;"
                        ),
                        
                        Div(
                            H3("Your Payment Details"),
                            Div(
                                Label("Full Name"),
                                Input(type="text", name="full_name", required=True),
                                style="margin-bottom: 15px;"
                            ),
                            Div(
                                Label("Bank ID"),
                                Input(type="text", name="payment_method", required=True),
                                style="margin-bottom: 15px;"
                            ),
                            Div(
                                Label("Message to Host"),
                                Textarea(name="message", rows="4", placeholder="Tell the host about your trip..."),
                                style="margin-bottom: 15px;"
                            ),
                            style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; margin-top: 20px; margin-bottom: 20px;"
                        ),
                        Button("Request to Book", type="submit",
                            style="background-color: #FF5A5F; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;"),
                        action=f"/process_payment/booking_id={result_booking.get_booking_id}",
                        method="post"
                    ),
                    style="max-width: 500px; margin: 0 auto; padding: 20px;"
                )
            )
        except Exception as e:
            return Html(P(str(e)))
        
    def get_html_index(self):
        filtered_accommodation_list = []
        for accom in self.get_accommodation_list:
            from .Accommodation import Room
            if not isinstance(accom, Room):
                filtered_accommodation_list.append(accom)
                
        
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
                            Input(type="text", name="search_query", placeholder="Where are you going?", required=True),
                            Input(type="date", name="check_in", style="margin-right: 10px;",required=True),
                            Input(type="date", name="check_out", style="margin-right: 10px;", required=True),
                            Button("Search", type="submit"),
                            action="/search",
                            method="post",
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
                    *[A(Div(
                        Img(src=accom.get_accom_pics[0]),
                        H3(accom.get_acc_name),
                        P(f"Address: {accom.get_address}"),
                        P(f"ID: {accom.get_id}"),
                        P(f"Price: {accom.get_price}/night"),
                        P(f"Host: {accom.get_host.get_user_name if accom.get_host else 'No host assigned'}"),
                        cls="card"
                    ), style="text-decoration: none; color: inherit;", href=f"/accommodation/{accom.get_id}") for accom in filtered_accommodation_list],
                    cls="container"
                )
            )
        )
    )
        
    def get_html_search_query(self, query: str, check_in: str, check_out: str):
        results = self.search_accommodations(query)
        filtered_accommodation_list = []
        for accom in results:
            from .Accommodation import Room
            if not isinstance(accom, Room):
                filtered_accommodation_list.append(accom)
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
        # Generate search results content
        if results:
            results_content = [
                A(Div(
                    Img(src=accom.get_accom_pics[0]),
                    H3(accom.get_acc_name),
                    P(f"Address: {accom.get_address}"),
                    P(f"ID: {accom.get_id}"),
                    P(f"Price: {accom.cal_price(check_in,check_out)}/night"),
                    P(f"Host: {accom.get_host.get_user_name if accom.get_host else 'No host assigned'}"),
                    cls="card"
                ),style="text-decoration: none; color: inherit;", href=f"/accommodation/{accom.get_id}"
                )
                for accom in filtered_accommodation_list
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
                            cls="nav-menu",
                        ),
                        Div(
                           Form(
                            Input(type="text", name="search_query", placeholder="Where are you going?", required=True),
                            Input(type="date", name="check_in", style="margin-right: 10px;", required=True),
                            Input(type="date", name="check_out", style="margin-right: 10px;", required=True),
                            Button("Search", type="submit"),
                            action="/search",
                            method="post",
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