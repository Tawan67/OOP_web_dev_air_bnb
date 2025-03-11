from fasthtml.common import *
from datetime import datetime, timedelta
import json
from fastapi import Request
from typing import Optional  # For Optional[int] in form handling


class ControlSystem:
    def __init__(self):
        self.__booking_list = []
        self.__member_list = []
        self.__host_list = []
        self.__accommodation_list = []  # stored hotel, house
        self.__payment_method_list = []
        self.__payment_list = []
        # self.__balance = None ไม่ควรมี เพราะ ค่านี้คสวรอยู่ใน paymed

    def add_payment(self, input1):
        self.__payment_list.append(input1)

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

    def details_date_by_booking_id(self, booking_id):  # dew sequen1

        booking_item = self.search_booking_by_id(booking_id)
        if isinstance(booking_item, str):
            return "Not Found"
        s = booking_item.get_booked_date.get_checkindate
        e = booking_item.get_booked_date.get_checkoutdate
        if s.month == e.month:
            print(f"{s.strftime('%b')} {s.day} - {e.day}")
            return f"{s.strftime('%b')} {s.day} - {e.day}"
        else:
            print(f"{s.strftime('%b')} {s.day} - {e.strftime('%b')} {e.day}")
            return f"{s.strftime('%b')} {s.day} - {e.strftime('%b')} {e.day}"

    def get_guest_amount(self, book_id):
        booking_item = self.search_booking_by_id(book_id)
        if isinstance(booking_item, str):
            return booking_item
        return booking_item.get_guess_amount

    def get_accom_name(self, booking_id):
        book_item = self.search_booking_by_id(booking_id=booking_id)
        if isinstance(book_item, str):
            return "Can't Find This Booking"
        accom = book_item.get_accommodation
        if isinstance(accom, str):
            return "Can't Find This Accommodation"
        return book_item.get_accommodation.get_acc_name

    def get_pic_from_book_id(self, booking_id):
        try:
            booking_item = self.search_booking_by_id(booking_id)
            accom = booking_item.get_accommodation
            pic = accom.get_accom_pics[0]
            return pic
        except:
            return "https://www.elegantthemes.com/blog/wp-content/uploads/2020/08/000-http-error-codes.png"

    def get_av_rating(self, booking_id):
        try:
            booking_item = self.search_booking_by_id(booking_id)
            accom = booking_item.get_accommodation
            review_list = accom.get_reviews
            point = 0
            count = len(review_list)
            if count == 0:
                return "No Rating Yet"
            for rating in review_list:
                point += rating.get_rating

            return f"{(point/count):.1f}"
        except Exception as e:
            return e

    @property
    def get_payment_method_list(self):  # tdkko
        return self.__payment_method_list

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
            if int(user_id) == member.get_user_id:
                return member
        return None

    def search_accom_by_id(self, accom_id):  # 1
        for i in self.__accommodation_list:
            if i.get_id == accom_id:
                return i
        return "Not Found"

    # FIXME:
    # ----------------------------------------------- downnnnnnnn
    # def create_booking(self, guest_amount, accom_id, price, menber_id,check_in,check_out):
    def create_booking(self, user_id, check_in, check_out, accom_id, guests):
        # guest_amount = int(guest_amount)
        accom_id = int(accom_id)
        member = self.search_member_by_id(user_id)
        accom = self.search_accom_by_id(accom_id)
        from .Booking import Booking

        booking_item = Booking(accom=accom, guess=guests, member=member)
        booking_item.update_date(check_in, check_out)
        self.add_booking(booking_item)

        return booking_item

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
        from .User import User

        if not isinstance(user, User):
            return "Error"
        print(user)
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
            if int(booking_id) == booking.get_booking_id:
                return booking
        return None

    def create_account(
        self, name: str, email: str, password: str, phone: str, age: int
    ):  # dew
        from .User import Member

        acount = Member(
            name=name, email=email, password=password, phone_num=phone, age=age
        )
        self.add_member(acount)
        pass

    def check_accom_available(self, booking):
        # Find the accommodation
        accom = booking.get_accommodation
        from .Accommodation import Accommodation

        if accom == "Not Found" and not isinstance(accom, Accommodation):
            return False

            # Check for overlap with existing booked dates
        for booked_date in accom.get_booked_date_list:
            existing_check_in = booked_date.get_checkindate
            existing_check_out = booked_date.get_checkoutdate

            # Overlap condition: if the requested range intersects with an existing range
            if (booking.get_booked_date.get_checkindate < existing_check_out) and (
                booking.get_booked_date.get_checkoutdate > existing_check_in
            ):
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
        from .Accommodation import House, Hotel

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
        from .Accommodation import Accommodation

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
                booking_date = booking.get_booked_date
                occupied_dates.append(
                    (booking_date.get_checkindate, booking_date.get_checkoutdate)
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
        if isinstance(user_id, str):
            user_id = int(user_id)
        for host in self.__host_list:
            if host.get_user_id == user_id:
                return host
        return "Host Not Found"

    def search_user_to_check(
        self, user_name, phone, email, password, age
    ):  # dew not sure
        for member in self.__member_list:
            if (
                member.get_phone_num == phone
                and member.get_user_nane == user_name
                and member.get_email == email
            ):
                return "You have an Account, Wanna Login?"
        try:
            self.create_account(name=user_name, email=email, password=password, age=age)
            return "Success"
        except:
            return "Sign up Fail"
        pass  # search for check if user want to sign up

    # korn does it really needed?
    def search_host_by_id_get_accom(self, user_id):
        if isinstance(user_id, str):
            user_id = int(user_id)
        that_host = None
        listhost = []
        for host in self.__host_list:
            listhost.append(host.get_user_id)
            if host.get_user_id == user_id:
                that_host = host
                break
        if that_host is None:
            return f"Host Not Found----- {listhost}-----{user_id}"
        my_accom_list = that_host.get_accommodation
        accom_list = [
            {"name": myaccom.get_acc_name, "address": myaccom.get_address}
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
            if host.get_user_id == int(user_id):
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
        result = self.update_booking_payment(booking_id, payment)
        self.add_payment(payment)
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

    def process_payment(
        self,
        booking_id,
        web_payment_method,
        web_payment_expired_date,
        web_payment_vcc,
        web_payment_type,
        web_period,
    ):
        process_booking = self.search_booking_by_id(booking_id)
        process_payment_method = self.search_payment_method_by_id(web_payment_method)
        if process_payment_method == None:
            return self.get_html_payment_not_found(web_payment_method)
        # try:
        # except Exception as e:
        #     return Html(P(e))
        if self.check_accom_available(process_booking):
            # Verify
            if (
                web_payment_expired_date
                == process_payment_method.get_expired_date_pretty
                and web_payment_vcc == str(process_payment_method.get_vcc_number)
            ):

                # create payment
                from .Payment import Payment

                new_payment = Payment(
                    web_period, process_payment_method, self.get_all_price(booking_id)
                )
                process_booking.update_payment(new_payment)
                self.add_payment(new_payment)

                # deduction
                if web_payment_type == "Period":
                    # return Html(P("Period"))
                    # new_payment.create_period(self.get_all_price(booking_id), web_period)
                    pass
                if web_payment_type == "One Time":
                    deduction_status = process_payment_method.deduction(
                        process_booking.get_payment.get_total
                    )
                    if deduction_status == "Not enough balance":
                        return Html(P("Not enough balance"))
            else:
                return self.get_html_payment_didnt_match(
                    web_payment_expired_date, web_payment_vcc
                )

            # update accommodation
            booked_date = process_booking.get_booked_date
            add_status = process_booking.get_accommodation.add_booked_date(booked_date)
            if add_status == "Error":
                return Html(P("add_booked_date fail"))

            # update member booking list
            process_booking.get_member.add_booking(process_booking)

            # change status
            process_booking.set_status("Paid")

            # return html success
            return self.get_html_purchase_sueccess()
        else:
            return self.get_html_accommodation_not_available()

    def search_payment_method_by_id(self, payment_method_id):
        for payment_method in self.__payment_method_list:
            if payment_method.get_bank_id == payment_method_id:
                return payment_method

    def search_payment_method_by_user_id(self, user_id):
        result_list = []
        for payment_method in self.__payment_method_list:
            if (
                int(payment_method.get_owner.get_user_id)
                if payment_method.get_owner
                else None == int(user_id)
            ):
                result_list.append(payment_method)

        return result_list

    def get_html_payment_didnt_match(
        self, web_payment_expired_date, web_payment_vcc_number
    ):
        return Html(
            Div(
                P(
                    "Payment Expired Date and VCC Number didn't match",
                    style="font-weight: 600; font-size: 18px; margin-bottom: 8px;",
                ),
                P(
                    f"Expired Date: {web_payment_expired_date}",
                    style="font-size: 16px; color: #484848; margin: 4px 0;",
                ),
                P(
                    f"VCC Number: {web_payment_vcc_number}",
                    style="font-size: 16px; color: #484848;",
                ),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #FF5A5F;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;""",
            )
        )

    def get_html_payment_not_found(self, web_paymenth_method):
        return Html(
            Div(
                P(
                    "Payment Method Not Found",
                    style="font-weight: 600; font-size: 18px; margin-bottom: 8px;",
                ),
                P(
                    f"Payment ID: {web_paymenth_method}",
                    style="font-size: 16px; color: #484848;",
                ),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #FF5A5F;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;""",
            )
        )

    def get_html_purchase_sueccess(self):
        return Html(
            Div(
                P("Purchase Successful", style="font-weight: 600; font-size: 18px;"),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #008489;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;""",
            )
        )

    def get_html_accommodation_not_available(self):
        return Html(
            Div(
                P(
                    "Accommodation not available for these dates",
                    style="font-weight: 600; font-size: 18px;",
                ),
                style="""background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #EBEBEB;
                        color: #FF5A5F;
                        font-family: 'Circular', -apple-system, 'Helvetica Neue', sans-serif;
                        max-width: 400px;""",
            )
        )

    def generate_booking_html(self, result_booking, booking_id, user_id):
        result_member = self.search_member_by_id(user_id)
        result_payment_method = self.search_payment_method_by_user_id(user_id)

        return (
            Title("Request to Book"),
            Div(
                H1("Request to Book"),
                Form(
                    Div(
                        H3("Your Trip"),
                        Div(
                            P(
                                f"Accommodation: {self.search_booking_by_id(booking_id).get_accommodation.get_acc_name}"
                            ),
                            style="margin-bottom: 15px;",
                        ),
                        Div(
                            P(
                                f"Accommodation Booked Date: {self.search_booking_by_id(booking_id).get_accommodation.get_booked_date_string}"
                            ),
                            style="margin-bottom: 15px;",
                        ),
                        Div(
                            P(
                                f"Check-in: {result_booking.get_booked_date.get_checkindate}"
                            ),
                            style="margin-bottom: 15px;",
                        ),
                        Div(
                            P(
                                f"Check-out: {result_booking.get_booked_date.get_checkoutdate}"
                            ),
                            style="margin-bottom: 15px;",
                        ),
                        Div(
                            P(f"Guests: {result_booking.get_guess_amount}"),
                            style="margin-bottom: 15px;",
                        ),
                        Div(
                            P(f"Price: {result_booking.cal_price()}"),
                            style="margin-bottom: 15px;",
                        ),
                        style="border: 1px solid #ddd; padding: 20px; border-radius: 5px;",
                    ),
                    Div(
                        H3("Your Payment Details"),
                        Label("Choose Your Card"),
                        Select(
                            *[
                                Option(
                                    f"Bank ID: {method.get_bank_id} (Balance: {method.get_balance})",
                                    value=method.get_bank_id,
                                )
                                for method in result_payment_method
                            ],
                            name="payment_method_id",
                            required=True,
                        ),
                        Div(
                            Label("Expired Date"),
                            Input(type="date", name="expired_date", required=True),
                            style="margin-bottom: 15px;",
                        ),
                        Div(
                            Label("VCC Number"),
                            Input(type="text", name="vcc_number", required=True),
                            style="margin-bottom: 15px;",
                        ),
                        Div(
                            Label("Payment Type"),
                            Select(
                                # TODO:
                                Option("One Time", value="OneTime"),
                                Option("Period", value="Period"),
                                name="payment_type",
                                required=True,
                            ),
                            Div(
                                Label("Period"),
                                Input(
                                    type="number",
                                    name="period",
                                    required=False,
                                    value="2",
                                ),
                                id="periodInput",
                                style="margin-bottom: 15px; display: none;",
                            ),
                        ),
                        Div(
                            Label("Message to Host"),
                            Textarea(
                                name="message",
                                rows="4",
                                placeholder="Tell the host about your trip...",
                            ),
                            style="margin-bottom: 15px;",
                        ),
                        style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; margin-top: 20px; margin-bottom: 20px;",
                    ),
                    Button(
                        "Request to Book",
                        type="submit",
                        style="background-color: #FF5A5F; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;",
                    ),
                    action=f"/process_payment/booking_id={result_booking.get_booking_id}",
                    method="post",
                    onsubmit="return validateForm()",
                ),
                Script(
                    """
                    function togglePeriodInput() {
                        var paymentType = document.querySelector('select[name="payment_type"]').value;
                        var periodInput = document.getElementById('periodInput');
                        periodInput.style.display = paymentType === 'Period' ? 'block' : 'none';
                    }

                    document.querySelector('select[name="payment_type"]').addEventListener('change', togglePeriodInput);

                    function validateForm() {
                        var paymentType = document.querySelector('select[name="payment_type"]').value;
                        var periodInput = document.querySelector('input[name="period"]');
                        if (paymentType === 'Period' && !periodInput.value) {
                            alert('Please enter a period.');
                            return false;
                        }
                        return true;
                    }
                """
                ),
                Form(
                    Input(type="hidden", name="user_id", value=user_id),
                    Button("Didn't have a card?", type="submit"),
                    action="/payment/add",
                    method="POST",
                ),
                style="max-width: 500px; margin: 0 auto; padding: 20px;",
            ),
        )

    def get_html_index(self, user_id=None):
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
        return Html(
            Head(
                Meta(charset="UTF-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Title("Airbnb Menu Layout"),
                Style(css),
            ),
            Body(
                Header(
                    A("Airbnb", cls="logo", href="/"),
                    Nav(
                        Form(
                            Button("Stays", type="submit"),
                            action=f"/booking_history/{user_id}",  # Move action to Form, use f-string
                            method="get",
                            cls="nav-form",  # Optional: add a class for styling
                        ),
                        A("Experiences", href="#"),
                        A("Online Experiences", href="#"),
                        cls="nav-menu",
                    ),
                    Div(
                        Form(
                            Input(
                                type="text",
                                name="search_query",
                                placeholder="Where are you going?",
                                required=True,
                            ),
                            Input(
                                type="date",
                                name="check_in",
                                style="margin-right: 10px;",
                                required=True,
                            ),
                            Input(
                                type="date",
                                name="check_out",
                                style="margin-right: 10px;",
                                required=True,
                            ),
                            Button("Search", type="submit"),
                            action="/search",
                            method="post",
                            cls="search-bar",
                        ),
                        A("Become a Host", href="#"),
                        A("Help", href="#"),
                        Div(cls="user-icon"),
                        cls="user-menu",
                    ),
                    cls="header",
                ),
                Div(
                    *[
                        A(
                            Div(
                                Img(src=accom.get_accom_pics[0]),
                                H3(accom.get_acc_name),
                                P(f"Address: {accom.get_address}"),
                                P(f"ID: {accom.get_id}"),
                                P(f"Price: {accom.get_price}/night"),
                                P(
                                    f"Host: {accom.get_host.get_user_name if accom.get_host else 'No host assigned'}"
                                ),
                                cls="card",
                            ),
                            style="text-decoration: none; color: inherit;",
                            href=f"/accommodation/{accom.get_id}",
                        )
                        for accom in filtered_accommodation_list
                    ],
                    cls="container",
                ),
                P(f"user id : {user_id}"),
            ),
        )

    def get_html_search_query(
        self, query: str, check_in: str, check_out: str, user_id: str
    ):
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
        if filtered_accommodation_list:
            results_content = [
                A(
                    Div(
                        Img(src=accom.get_accom_pics[0]),
                        H3(accom.get_acc_name),
                        P(f"Address: {accom.get_address}"),
                        P(f"ID: {accom.get_id}"),
                        P(f"Price: {accom.cal_price(check_in,check_out)}/night"),
                        P(
                            f"Host: {accom.get_host.get_user_name if accom.get_host else 'No host assigned'}"
                        ),
                        cls="card",
                    ),
                    style="text-decoration: none; color: inherit;",
                    href=f"/accommodation/{accom.get_id}",
                )
                for accom in filtered_accommodation_list
            ]
        else:
            results_content = [P("No results found for your search.", cls="no-results")]

        return Html(
            Head(
                Meta(charset="UTF-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Title(f"Search Results for '{query}' - Airbnb"),
                Style(css),
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
                            Input(
                                type="text",
                                name="search_query",
                                placeholder="Where are you going?",
                                required=True,
                            ),
                            Input(
                                type="date",
                                name="check_in",
                                style="margin-right: 10px;",
                                required=True,
                            ),
                            Input(
                                type="date",
                                name="check_out",
                                style="margin-right: 10px;",
                                required=True,
                            ),
                            Button("Search", type="submit"),
                            action="/search",
                            method="post",
                            cls="search-bar",
                        ),
                        A("Become a Host", href="#"),
                        A("Help", href="#"),
                        Div(cls="user-icon"),
                        cls="user-menu",
                    ),
                    cls="header",
                ),
                Div(
                    H2(f"Search Results for '{query}', from {check_in} to {check_out}"),
                    Div(*results_content, cls="container"),
                    cls="search-results",
                ),
            ),
        )

    def get_booking_history(self, user_id):
        user = self.search_member_by_id(user_id)
        if user == None:
            return None

        booking_list = []
        for booking in self.search_booking_by_user(user):
            book = []
            book.append(booking.get_booking_id)
            book.append(booking.get_booking_status)
            book.append(booking.get_date)
            book.append(booking.get_accommodation.get_acc_name)
            print(f"///////////////////////////////:{booking.get_booked_date}")
            book.append(booking.get_booked_date.get_checkindate)
            book.append(booking.get_booked_date.get_checkoutdate)
            book.append(booking.get_amount)
            booking_list.append(book)

        return booking_list

    def get_booking_detail(self, booking_id):
        booking = self.search_booking_by_id(booking_id)
        show_booking_detail = []
        show_booking_detail.append(booking.get_booking_id)
        show_booking_detail.append(booking.get_booking_status)
        show_booking_detail.append(booking.get_date)
        show_booking_detail.append(booking.get_amount)
        show_booking_detail.append(booking.get_guess_amount)

        booked_date = booking.get_booked_date
        accom = booking.get_accommodation

        show_booking_detail.append(booked_date.get_checkindate)
        show_booking_detail.append(booked_date.get_checkoutdate)

        show_booking_detail.append(accom.get_acc_name)
        show_booking_detail.append(accom.get_info)
        show_booking_detail.append(accom.get_address)

        host = self.search_host_by_accom(accom)

        show_booking_detail.append(host.get_user_name)
        show_booking_detail.append(host.get_phone_num)

        return show_booking_detail

    def cancel_booking(self, booking_id):
        booking = self.search_booking_by_id(booking_id)
        user = booking.get_member

        # booked_date = booking.get_booked_date
        # accom = booking.get_accommodation
        # print(f"before {booking.get_booking_status}")
        # print(f"Target before {accom.get_booked_date(booked_date)}")
        if booking.get_booking_status == "Confirmed":
            amount = booking.get_amount
            booked_date = booking.get_booked_date
            accom = booking.get_accommodation
            user_get_pay_med = user.get_pay_med
            control_system_pay_med = self.__paymentmethod
            self.payback(control_system_pay_med, user_get_pay_med, amount)
            accom.del_booked_date(booked_date)
            booking.update_booking_status("Cancelled")

        else:
            booking.update_booking_status("Cancelled")

        return user.get_user_id

    def payback(self, system_pay_med, user_pay_med, amount, tranfer_type="default"):

        print(
            f"system_balance before {system_pay_med.get_balance}, user_balance before {user_pay_med.get_balance}"
        )

        system_pay_med.update_balance(-amount)
        user_pay_med.update_balance(+amount)

        print(
            f"system_balance after {system_pay_med.get_balance}, user_balance after {user_pay_med.get_balance}"
        )
        return "Success"

    def get_booking_by_id(self, booking_id):
        for booking in self.get_booking_list:
            if booking.get_booking_id == booking_id:
                return booking

    @property
    def get_payment_list(self):
        return self.__payment_list

    def get_html_monitor_airbnb(self):
        # Airbnb-inspired CSS styling
        css = """
            <style>
                .monitor-container {
                    font-family: 'Circular', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 1200px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                .monitor-title {
                    color: #222222;
                    font-size: 24px;
                    font-weight: 600;
                    margin-bottom: 20px;
                }
                .monitor-table {
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0;
                }
                .monitor-table th {
                    color: #717171;
                    font-size: 14px;
                    font-weight: 600;
                    text-align: left;
                    padding: 10px 15px;
                    border-bottom: 1px solid #e0e0e0;
                }
                .monitor-table td {
                    color: #222222;
                    font-size: 14px;
                    padding: 15px;
                    vertical-align: top;
                    border-bottom: 1px solid #e0e0e0;
                }
                .monitor-table tr:last-child td {
                    border-bottom: none;
                }
                .item-list {
                    margin: 0;
                    padding: 0;
                    list-style: none;
                }
                .item-list li {
                    margin-bottom: 8px;
                    line-height: 1.4;
                }
                .item-list li:hover {
                    color: #FF5A5F;
                    transition: color 0.2s ease;
                }
                .timestamp {
                    color: #717171;
                    font-size: 12px;
                    margin-top: 10px;
                }
                @media (max-width: 768px) {
                    .monitor-table th, .monitor-table td {
                        padding: 10px;
                        font-size: 12px;
                    }
                }
            </style>
        """

        # Get the data
        members = self.get_member_list
        payment_method_list = self.get_payment_method_list
        accommodations = self.get_accommodation_list
        hosts = self.get_host_list
        bookings = self.get_booking_list
        payments = self.get_payment_list

        # Build the HTML structure
        return Html(
            Style(css),
            Div(
                H3(
                    "Monitor", klass="monitor-title"
                ),  # 'klass' is used instead of 'class' to avoid Python keyword conflict
                Table(
                    Thead(
                        Tr(
                            Th("Members"),
                            Th("Payment Methods"),
                            Th("Accommodations"),
                            Th("Hosts"),
                            Th("Bookings"),
                            Th("Payments"),
                        )
                    ),
                    Tbody(
                        Tr(
                            Td(
                                Ul(
                                    *[Li(str(member)) for member in members],
                                    klass="item-list",
                                )
                            ),
                            Td(
                                Ul(
                                    *[
                                        Li(str(paymentmethod))
                                        for paymentmethod in payment_method_list
                                    ],
                                    klass="item-list",
                                )
                            ),
                            Td(
                                Ul(
                                    *[Li(str(acc)) for acc in accommodations],
                                    klass="item-list",
                                )
                            ),
                            Td(
                                Ul(
                                    *[Li(str(host)) for host in hosts],
                                    klass="item-list",
                                )
                            ),
                            Td(
                                Ul(
                                    *[Li(str(booking)) for booking in bookings],
                                    klass="item-list",
                                )
                            ),
                            Td(
                                Ul(
                                    *[Li(str(payment)) for payment in payments],
                                    klass="item-list",
                                )
                            ),
                        )
                    ),
                    klass="monitor-table",
                ),
                P(
                    f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    klass="timestamp",
                ),
                klass="monitor-container",
            ),
        )

    def add_member_and_payment_method(self):
        from .User import Member
        from .Payment import PaymentMethod

        reset = Member("", "", "", "", "")
        reset.reset_increament()
        new_member = Member(
            name="test", email="test", password="1234", phone_num="test", age="19"
        )
        self.add_member(new_member)

        new_pay_med = PaymentMethod(
            bank_id="1234",
            user=new_member,
            balance=100000,
            expired_date=datetime.now(),
            vcc=555,
        )
        self.add_payment_method(new_pay_med)
        self.search_member_by_id(new_member.get_user_id).add_payment_method(new_pay_med)
        balance = (
            self.search_member_by_id(new_member.get_user_id)
            .get_payment_method_list[0]
            .get_balance
        )
        print(f"name : {new_member.get_user_name}, balance : {balance}")

        new_pay_med_2 = PaymentMethod(
            bank_id="4321",
            user=new_member,
            balance=99999,
            expired_date=datetime.now(),
            vcc=666,
        )
        self.add_payment_method(new_pay_med_2)
        self.search_member_by_id(new_member.get_user_id).add_payment_method(
            new_pay_med_2
        )
        balance = (
            self.search_member_by_id(new_member.get_user_id)
            .get_payment_method_list[1]
            .get_balance
        )
        print(f"name : {new_member.get_user_name}, balance : {balance}")

        new_pay_med_3 = PaymentMethod(
            bank_id="4399", user=None, balance=50, expired_date=datetime.now(), vcc=888
        )
        self.add_payment_method(new_pay_med_3)

    def add_accommodation_test(self):
        from .Accommodation import Accommodation, House, Hotel, Room
        from .User import Host

        reset = Accommodation(None, None, None, None)
        reset.reset_increament()
        new_house = House(
            "test_house",
            "location",
            "description",
            6969,
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJxo2NFiYcR35GzCk5T3nxA7rGlSsXvIfJwg&s",
        )
        accom_pics = [
            "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4wLkW7-Z5PXiWG6VF7BjPpGTjmVIZwZHo3Zb5vJf8nppOzQhjfRdx2GTAfr6JaO1uHeA&usqp=CAU",
            "https://t4.ftcdn.net/jpg/09/22/37/79/360_F_922377968_S7Y7lesMSbv91kQtO2u1GET0bUtgOrL1.jpg",
            "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
            "https://www.brightonhomes-idaho.com/2020/wp-content/uploads/2020/03/Available_Homes-600x400.jpg",
        ]
        for pic in accom_pics:
            new_house.add_accom_pics(pic)
        self.add_accommodation(new_house)

        new_host = Host(
            name="Tro",
            email="saygex1@gmail.com",
            password=12345,
            phone_num=1234567890,
            age=96,
        )
        new_house.add_host(new_host)
        self.add_host(new_host)
        self.search_host_by_id(new_host.get_user_id).add_accommodation(new_house)
        print(
            f"Accommodation : {new_house.get_acc_name},ID : {new_house.get_id}, Host : {new_host.get_user_name}"
        )

        # new_hotel = Hotel("test_hotel", "location_hotel", "description_hotel")
        # for pic in accom_pics:
        #     new_hotel.add_accom_pics(pic)
        # self.add_accommodation(new_hotel)
        # new_hotel.add_host(new_host)
        # new_room = Room(room_id="1", room_floor=1, price=1000, hotel_address="location_hotel", hotel_name="test_hotel")
        # self.add_accommodation(new_room)
        # self.search_accom_by_id(new_hotel.get_id).add_room(new_room)
        # self.search_host_by_id(new_host.get_user_id).add_accommodation(new_hotel)
        # self.search_host_by_id(new_host.get_user_id).add_accommodation(new_room)
        # print(f'Accommodation : {new_hotel.get_acc_name},ID : {new_hotel.get_id}, Host : {new_host.get_user_name}')
        # print(f'Accommodation : {new_room.get_acc_name},ID : {new_room.get_id}, Host : {new_host.get_user_name}')

    def make_booking_and_payment(self):
        from .Booking import Booking, BookedDate

        reset = Booking(None, None, None).reset_increment()

        new_booking = self.create_booking(
            "1",
            check_in="2025-03-11",
            check_out="2025-03-12",
            accom_id=self.get_accommodation_list[0].get_id,
            guests=2,
        )
        reset_increment = new_booking.create_payment(
            None, None, None
        ).reset_increament()
        self.create_payment(
            self.get_all_price(new_booking.get_booking_id, True),
            1,
            self.get_payment_method_list[0],
            new_booking.get_booking_id,
        )
        return new_booking

    def add_accommodation_booked_date(self):
        from .Booking import BookedDate

        new_booked_date = BookedDate(datetime.now(), datetime.now() + timedelta(days=2))
        self.get_accommodation_list[0].add_booked_date(new_booked_date)

        new_booked_date = BookedDate(
            datetime.now() + timedelta(days=4), datetime.now() + timedelta(days=6)
        )
        self.get_accommodation_list[0].add_booked_date(new_booked_date)

        new_booked_date = BookedDate(
            datetime.now() + timedelta(days=8), datetime.now() + timedelta(days=12)
        )
        self.get_accommodation_list[0].add_booked_date(new_booked_date)

        print(f"booked_date : {self.get_accommodation_list[0].get_booked_date_list}")

    def get_html_add_payment(self, user_id):
        user_name = self.search_member_by_id(user_id).get_user_name
        return Html(
            Title(f"Add Payment Method - {user_name}"),
            Div(
                H3(f"Add a Payment Method for {user_name}"),
                Form(
                    Div(
                        Div(
                            Label(
                                "Bank ID",
                                style="font-weight: bold; margin-bottom: 5px; display: block;",
                            ),
                            Input(
                                type="text",
                                name="bank_id",
                                placeholder="Enter your Bank ID",
                                required=True,
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;",
                            ),
                            style="margin-bottom: 20px;",
                        ),
                        Div(
                            Label(
                                "Expiration Date",
                                style="font-weight: bold; margin-bottom: 5px; display: block;",
                            ),
                            Input(
                                type="date",
                                name="expired_date",
                                required=True,
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;",
                            ),
                            style="margin-bottom: 20px;",
                        ),
                        Div(
                            Label(
                                "Security Code (VCC)",
                                style="font-weight: bold; margin-bottom: 5px; display: block;",
                            ),
                            Input(
                                type="text",
                                name="vcc_number",
                                placeholder="Enter security code",
                                required=True,
                                maxlength="4",
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;",
                            ),
                            style="margin-bottom: 20px;",
                        ),
                        style="background: white; padding: 20px; border: 1px solid #e4e4e4; border-radius: 8px;",
                    ),
                    Button(
                        "Add Payment Method",
                        type="submit",
                        style="background-color: #FF5A5F; color: white; padding: 12px 24px; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 20px; transition: background-color 0.2s;"
                        ":hover {background-color: #E0474C;}",
                    ),
                    Input(type="hidden", name="user_id", value=user_id),
                    action="/payment/add/process",
                    method="post",
                    style="max-width: 400px; margin: 20px auto;",
                ),
                style="font-family: 'Circular', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;",
            ),
        )

    def get_html_add_payment_process(
        self, web_user_id, web_bank_id, web_expired_date, web_vcc_number
    ):
        # try:
        process_payment_method = self.search_payment_method_by_id(web_bank_id)
        if process_payment_method is None:
            return Html(
                P(f"Payment Method : {web_bank_id} not found"),
            )
        process_member = self.search_member_by_id(web_user_id)
        if process_member is None:
            return Html(
                P(f"User : {web_user_id} not found"),
            )
        if (
            web_expired_date == process_payment_method.get_expired_date_pretty
            and web_vcc_number == str(process_payment_method.get_vcc_number)
        ):  # check vcc and expired
            process_payment_method.set_owner(process_member)
            process_member.add_payment_method(process_payment_method)
            return Html(
                P(
                    f"Payment Method : {process_payment_method.get_bank_id} added successfully",
                    style="font-weight: 600; font-size: 18px;",
                ),
                P(
                    f"User : {process_member.get_user_name} added successfully",
                    style="font-weight: 600; font-size: 18px;",
                ),
            )

    # except Exception as e:
    #     return Html(P(f"Error: {str(e)}", style="font-weight: 600; font-size: 18px;"))

    def get_price_per_night(self, booking_id):
        try:
            booking_item = self.search_booking_by_id(booking_id)
            accom = booking_item.get_accommodation
            price = accom.get_price
            return str(price)
        except Exception as e:
            return e

    def get_night(self, booking_id):
        try:
            booking_item = self.search_booking_by_id(booking_id)
            s = booking_item.get_booked_date.get_checkindate
            e = booking_item.get_booked_date.get_checkoutdate
            delta_date = (e - s).days
            return str(delta_date)
        except:
            return "Get Nights Wrong"

    def get_total_price_to_show(self, booking_id, out_int=False):
        try:
            booking_item = self.search_booking_by_id(booking_id)
            accom = booking_item.get_accommodation
            price = accom.get_price
            guest = booking_item.get_guess_amount
            start = booking_item.get_booked_date.get_checkindate
            end = booking_item.get_booked_date.get_checkoutdate
            total_price = self.cal_price_in_accom_not_fee(accom, start, end)
            if out_int == True:
                return total_price
            return str(total_price)
        except Exception as e:
            return e

    def cal_price_in_accom_not_fee(self, accom, start_date, end_date):  # with_out_fee

        price = accom.cal_price_not_fee(start_date, end_date)
        return price

    def get_fee(self, booking_id, out_int=False):
        # try:
        booking_item = self.search_booking_by_id(booking_id)
        accom = booking_item.get_accommodation
        start_date = booking_item.get_booked_date.get_checkindate
        end_date = booking_item.get_booked_date.get_checkoutdate
        guest_amount = booking_item.get_guess_amount
        fee = accom.get_price_accom(start_date, end_date, guest_amount, get_fee=True)
        fee = math.ceil(fee)
        if out_int == True:
            return fee
        return str(fee)
        # except:
        #     return 'Fee MEE pan HAA'

    def get_all_price(self, booking_id, out_int=False):  # true if want int
        try:
            total_price_with_fee = self.get_fee(
                booking_id, out_int=True
            ) + self.get_total_price_to_show(booking_id, out_int=True)
            if out_int:
                return total_price_with_fee
            return str(total_price_with_fee)
        except Exception as e:
            return e

    def get_html_booking(self, book_id):
        if not book_id:
            return Titled("ข้อผิดพลาด", P("ไม่พบหมายเลขการจอง กรุณาลองใหม่"))
        pay_div = None
        if pay_div != None:
            pay_div = Div(
                H3("Pay With"),
                Form(  # start FORM
                    Label("Choose Payment:"),
                    Select(
                        Option("One Time", value="one_time", id="one_time"),
                        Option("Parts", value="parts"),
                        id="payment",
                        name="payment",
                        onchange="toggleInstallments()",
                    ),
                    Div(
                        Label("Choose Period:"),
                        Select(
                            Option("2", value="2"),
                            Option("4", value="4"),
                            Option("6", value="6"),
                            id="installments",
                            name="period",
                        ),
                        id="installmentsDiv",
                        name="period_div",
                        style="display: none;",
                    ),
                    Label("Debit or Credit:"),
                    Select(
                        Option("Debit", value="debit"),
                        Option("Credit", value="credit"),
                        id="paymed",
                        name="paymed",
                    ),
                    Label("Card Number:"),
                    Input(
                        type="text",
                        id="card_number",
                        name="card_num",
                        placeholder="Enter your card number",
                    ),
                    Label("Expiration Date:"),
                    Input(type="date", id="expiration_date", name="expiration_date"),
                    Label("Password:"),
                    # Input(type="text", id="cvv", placeholder="Enter CVV"),
                    Input(
                        type="password",
                        id="cvv",
                        name="password",
                        placeholder="Enter Password",
                    ),
                    Input(type="hidden", name="user_id", value="{{user_id}}"),
                    Input(type="hidden", name="booking_id", value=f"{book_id}"),
                    Button("Confirm and Pay", type="submit"),
                    method="post",
                    action="/create_pay",
                ),  # endform
                style="width:50%",
            )
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
                    """,
                    ),
                    href="/",
                ),
                style="""
            padding: 15px;
            height:80px;
            align-items: center;
            """,
            ),  # head
            Hr(),
            # back button
            Div(
                A(
                    Button(
                        "<",
                        style="""
                        background-color:white;
                        color:black;
                        border: 2px solid black;
                        border-radius: 8px;
                        font-size:20px""",
                    ),
                    href="/back",
                ),
                H1("Confirm and pay", style=""" color:black;"""),
                style="""
            padding-left: 15px;
            width:400px;
            height : 100px ;
            background-color: white;
            display:flex;
            justify-content: space-between;
            
            """,
            ),
            Hr(
                style=""" padding: 10 px;
            background-color: blue px;"""
            ),
            # main block
            Div(
                Div(  # left side
                    Div(H3("Your trip", style=""" color:black;""")),
                    Div(
                        H6("Dates", style="color:black;"),
                        Div(
                            P(
                                self.details_date_by_booking_id(book_id),
                                style="flex:1; text-align:left;color:black;",
                            ),
                            A(
                                P("Edit", style="text-align:right;color:black;"),
                                href=f"/edit_date_guest/{book_id}",
                            ),
                            style="display:flex; justify-content: space-between; align-items: center;height:20px; ",
                        ),
                        Div(
                            H6("Guest", style="color:black;"),
                            Div(
                                P(
                                    f"{self.get_guest_amount(book_id)} guest",
                                    style="flex:1; text-align:left;color:black;",
                                ),
                                A(
                                    P(
                                        "Edit",
                                        style="text-align:right;color:black;gap:30px; ",
                                    ),
                                    href=f"/edit_date_guest/{book_id}",
                                ),
                                style="display:flex; justify-content: space-between; align-items: center;height:20px;",
                            ),
                        ),
                        style="width:400px",
                    ),  # Pay and Post
                    pay_div,
                    Script(
                        """
                    function toggleInstallments() {
                        let paymentSelect = document.getElementById("payment");
                        let installmentsDiv = document.getElementById("installmentsDiv");
                        if (paymentSelect.value === "parts") {
                            installmentsDiv.style.display = "block";
                        } else {
                            installmentsDiv.style.display = "none";
                        }
                    }
                """
                    ),
                    style="width: 50%; background-color: white; padding: 20px;color:black;overflow-y: auto;",
                ),  # end post
                # right
                Div(
                    Div(
                        Div(
                            Div(
                                Img(
                                    src=self.get_pic_from_book_id(book_id),
                                    style="width:100%; height:auto; border-radius:8px;",
                                ),
                                style="width:30%;",
                            ),
                            Div(
                                H4(
                                    self.get_accom_name(book_id),
                                    style="margin: 0; padding-left: 10px;",
                                ),
                                P(
                                    f"Rating : {self.get_av_rating(book_id)}⭐",
                                    style="margin: 0; padding-left: 10px;",
                                ),
                                style="width:70%; display:flex; flex-direction:column; justify-content:center;",
                            ),
                            style="""display:flex;
                        align-items:center; 
                        gap:10px; 
                        background-color: white; 
                        padding: 10px; 
                        border-radius:8px;
                        width:500px""",
                        ),
                        Div(
                            Table(
                                Tr(
                                    Td(
                                        f"${self.get_price_per_night(book_id)} x {self.get_night(book_id)} nights",
                                        style="background-color:white;color:black;",
                                    ),
                                    Td(
                                        f"${self.get_total_price_to_show(book_id)}",
                                        style="background-color:white;color:black;",
                                    ),
                                ),
                                Tr(
                                    Td(
                                        "fee",
                                        style="background-color:white;color:black;",
                                    ),
                                    Td(
                                        "$" + self.get_fee(book_id),
                                        style="background-color:white;color:black;",
                                    ),
                                ),
                                Tr(
                                    Td(
                                        B(
                                            "total",
                                            style="background-color:white;color:black;",
                                        )
                                    ),
                                    Td(
                                        B(
                                            "$" + self.get_all_price(book_id),
                                            style="background-color:white;color:black;",
                                        )
                                    ),
                                ),
                                Tr(
                                    Form(
                                        Button(
                                            "Pay",
                                            style="background-color:white;color:black;border: 2px solid black;border-radius: 8px;",
                                        ),
                                        method="post",
                                        action=f"/purchase/booking_id={book_id}",
                                    )
                                ),
                                style="background-color:white;",
                            ),
                            header=H4(
                                "Price Details",
                                style="background-color:white;color:black;",
                            ),
                            footer=Div(
                                Div(H6("Total Price"), style="text-align:left"),
                                Div(
                                    H6("$" + self.get_all_price(book_id)),
                                    style="text-align:right",
                                ),
                                style="""background-color:white;
                                                color:black;
                                                display:flex;
                                                justify-content: space-between""",
                            ),
                            style="background-color:white;padding:15px;width:500px",
                        ),
                        style="""width: 100%;
                background-color: white;
                items-align:center;
                padding:50px;
                border: 2px solid black;
                border-radius: 8px;
                padding-left:10px""",
                    )
                ),
                style="display: flex; flex-direction: row; height: 100vh;padding-right: 15px;padding-left: 15px;",
            ),
            Hr(
                style=""" padding: 10 px;
            background-color: blue px;"""
            ),
            style=""" padding: 0px;
        background-color : white;
        
        """,
        )

    def get_html_edit_date_guest(self, book_id):
        return Div(
            Div(
                H1(
                    "Edit Booking Date & Guests",
                    style="text-align: center; color: black; margin-bottom: 20px;",
                )
            ),
            Div(
                Form(
                    Div(
                        Label("Start Date:", style="color: black;"),
                        Input(type="date", id="start", name="start"),
                        style="padding-bottom: 10px; display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;",
                    ),
                    Div(
                        Label("End Date:", style="color: black;"),
                        Input(type="date", id="end", name="end"),
                        style="padding-bottom: 10px; display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;",
                    ),
                    Div(
                        Label("Guest Amount:", style="color: black;"),
                        Input(
                            type="number",
                            id="guest_amount",
                            name="guest_amount",
                            min="1",
                            max="10",
                        ),
                        style="padding-bottom: 10px; display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;",
                    ),
                    Button(
                        "Confirm",
                        type="submit",
                        style="background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px;",
                    ),
                    method="post",
                    action=f"/update_date_guest/{book_id}",
                    style="""
                display: flex; flex-direction: column; align-items: center; 
                background-color: white; padding: 20px; width: 100%; 
                margin: auto; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                """,
                )
            ),
            style="""display: flex;
            flex-direction: column;
            justify-content: center; 
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;""",
        )

    def update_date(self, booking_id, start, end):
        if not (isinstance(booking_id, str)):
            booking_id = str(booking_id)
        booking_item = self.search_booking_by_id(booking_id)
        result = booking_item.update_date(start, end)
        return result
        pass

    def update_guest(self, booking_id, guest):
        if not (isinstance(booking_id, str)):
            booking_id = str(booking_id)
        booking_item = self.search_booking_by_id(booking_id)
        result = booking_item.update_guest(guest)
        return result
        pass

    def get_html_booking_history(self, user_id):
        booking_list = self.get_booking_history(user_id)
        if booking_list == None:
            return Container(
                H1("Can't Find Booking History"),
                Form(
                    Button("Back to Home page", type="submit"),
                    method="get",
                    action=f"/",
                ),
            )
        return Titled(
            "Booking History",
            Container(
                Form(
                    Button("Back to Home Page", type="submit"), method="get", action="/"
                )
            ),
            Table(
                Thead(
                    Tr(
                        Th("ID"),
                        Th("Status"),
                        Th("Date"),
                        Th("Accommodation name"),
                        Th("Check-In"),
                        Th("Check-Out"),
                        Th("Amount"),
                        Th(""),
                    )
                ),
                Tbody(
                    *[
                        Tr(
                            Td(p[0]),
                            Td(p[1]),
                            Td(p[2]),
                            Td(p[3]),
                            Td(p[4]),
                            Td(p[5]),
                            Td(p[6]),
                            Td(
                                Form(
                                    Button("Detail", type="submit"),
                                    method="get",
                                    action=f"/view_booking_detail/{user_id}/{p[0]}",
                                )
                            ),
                        )
                        for p in booking_list
                    ]
                ),
            ),
        )

    def get_html_view_booking_detail(self, user_id, booking_id):
        control_system = self
        detail = control_system.get_booking_detail(booking_id)
        cancel_button = None
        edit_detail = None
        if detail[1] != "Cancelled" and detail[1] != "Completed":
            cancel_button = Form(
                Hidden(name="_method", value="PUT"),
                Button("Cancel Booking", type="submit"),
                method="post",
                action=f"/cancel_booking/{detail[0]}",
            )

        ###########################################
        if detail[1] == "Waiting":
            edit_detail = Form(
                Button("Change detail", type="submit"),
                method="get",
                # ส่งไปหน้าดิวที่ใช้ในการอัปเดรต booking
                action=f"/edit_date_guest/{booking_id}",
            )

        #############################################
        if detail == None:
            return Container(
                H1("Can't Find Booking"),
                Form(
                    Button("Back to Booking History", type="submit"),
                    method="get",
                    action=f"/booking_history/{user_id}",
                ),
            )
        else:
            return Titled(
                f"Booking Detail for {detail[0]}",
                Container(
                    P(f"Booking ID: {detail[0]}"),
                    P(f"Status: {detail[1]}"),
                    P(f"date: {detail[2]}"),
                    P(f"Accommodation Name: {detail[7]}"),
                    P(f"Guess Amount: {detail[4]}"),
                    P(f"Check-In Date: {detail[5]}"),
                    P(f"Check-Out Date: {detail[6]}"),
                    P(f"Amount: {detail[3]}"),
                    P(f"Accommodation Info: {detail[8]}"),
                    P(f"Address: {detail[9]}"),
                    P(f"Host Name: {detail[10]}"),
                    P(f"Phone Number: {detail[11]}"),
                    edit_detail,
                    cancel_button,
                    Form(
                        Button("Back to Booking History", type="submit"),
                        method="get",
                        action=f"/booking_history/{user_id}",
                    ),
                ),
            )

    def get_html_create_pay(
        self, payment, period, paymed, card_num, expiration_date, password, booking_id
    ):
        if self.check_expiraion_date(expiration_date):
            result = self.post_payment(
                payment, paymed, booking_id, card_num, password, period, balance=1000.00
            )
        else:
            return Div(
                H2(
                    "Can't Booking Your Card has Gone I'm sorry but you have to move on to a New Card",
                    style="padding : 30px;color:black;",
                ),
                A(
                    Button("Go back", style="padding:30px"),
                    href=f"/booking/{booking_id}",
                ),
                style="""padding: 20px; 
                    text-align: center;
                    background-color: #f4f4f4;
                    height: 100vh;
                    color:black;
                    font-size:16;
                    flex-direction: column;
                        display:flex;
                        align:center;
                    """,
            )

        return Div(
            H3(f"Payment Confirmation for Booking {booking_id}"),
            P(f"Payment Method: {paymed}"),
            P(f"Card Number: {card_num}"),
            P(f"Total Amount: {self.get_all_price(booking_id)}"),
            Button("Back to Home", action="/"),
            style="padding: 20px;",
        )

    def get_html_update_date_guest(self, start, end, guest_amount, book_id):
        # try:
        date_result = self.update_date(book_id, start, end)
        guest_result = self.update_guest(book_id, guest_amount)
        amount = self.get_all_price(book_id, True)
        self.get_booking_by_id(int(book_id)).set_amount(amount)
        return Redirect(f"/booking/{book_id}")  # ส่งผู้ใช้กลับไปยังหน้าจอง
        # except Exception as e:
        #     return Html(e)
        return Div(
            H1(
                f"Booking updated successfully!",
                style=""" text-align: center; background-color: #f4f4f4;color:black;""",
            ),
            H1(
                f"Booking updated date is {date_result}!",
                style=""" text-align: center; background-color: #f4f4f4;color:black;""",
            ),
            H1(
                f"Booking updated guest amount is {guest_result}!",
                style=""" text-align: center; background-color: #f4f4f4;color:black;""",
            ),
            A(
                Button(
                    "Go back to Booking",
                    style=""" text-align: center;
                    background-color:#88E788;
                    color:black;""",
                ),
                href=f"/booking/{book_id}",
                style=""" text-align: center; background-color: #f4f4f4;color:black;""",
            ),
            style="""padding: 20px; text-align: center; background-color: #f4f4f4;height: 100vh;""",
        )

    def get_html_room_detail(self, accom_id, user_id):
        # user_id = self.get_member_list[0].get_user_id  # 21
        # host_id = self.get_host_list[0].get_user_id  # 31
        process_accom = self.search_accom_by_id(accom_id)
        host_id = process_accom.get_host.get_user_id
        # print(user_id)

        # print(user_id)
        print(f"host_id = {host_id}")
        print(f"user_id = {user_id}")
        detail = self.search_accom_detail(accom_id)

        accommodation1 = self.search_accom_by_id(accom_id)
        if accom_id == 1:
            accom_pics = [
                "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4wLkW7-Z5PXiWG6VF7BjPpGTjmVIZwZHo3Zb5vJf8nppOzQhjfRdx2GTAfr6JaO1uHeA&usqp=CAU",
                "https://t4.ftcdn.net/jpg/09/22/37/79/360_F_922377968_S7Y7lesMSbv91kQtO2u1GET0bUtgOrL1.jpg",
                "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
                "https://www.brightonhomes-idaho.com/2020/wp-content/uploads/2020/03/Available_Homes-600x400.jpg",
            ]
        # elif accom_id == 22:
        #     accom_pics = [
        #         "https://images.immediate.co.uk/production/volatile/sites/3/2021/05/minecraft-blueprints-0d97805.png",
        #         "https://images.immediate.co.uk/production/volatile/sites/3/2021/05/victorian-castle-minecraft-d5a2a31.png",
        #         "https://i.pinimg.com/736x/4f/58/10/4f5810b188b42fb7af207cc77bef2e9c.jpg",
        #         "https://i.ytimg.com/vi/gL_4xJ6TO7g/maxresdefault.jpg",
        #         "https://assetsio.gnwcdn.com/pale-garden-house.jpg?width=1200&height=630&fit=crop&enable=upscale&auto=webp",
        #     ]
        # elif accom_id == 23:
        #     accom_pics = [
        #         "https://example.com/accom3_img1.jpg",
        #         "https://example.com/accom3_img2.jpg",
        #         "https://example.com/accom3_img3.jpg",
        #         "https://example.com/accom3_img4.jpg",
        #         "https://example.com/accom3_img5.jpg",
        #     ]
        # elif accom_id == 24:
        #     accom_pics = [
        #         "https://example.com/accom4_img1.jpg",
        #         "https://example.com/accom4_img2.jpg",
        #         "https://example.com/accom4_img3.jpg",
        #         "https://example.com/accom4_img4.jpg",
        #         "https://example.com/accom4_img5.jpg",
        #     ]
        else:
            accom_pics = []  # Default empty list if no match

        # accommodation1.clear_accom_pics()

        for pic in accom_pics:
            accommodation1.add_accom_pics(pic)

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

    # def get_html_hosting(self, user_id):
    #     listmyaccom = self.search_host_by_id_get_accom(user_id)  # Host Not Found
    #     print(f"-----55>>>>{listmyaccom}")
    #     listreview = self.search_host_by_id_get_review(user_id)
    #     print(f"Listreview : {listreview}")
    #     return Html(
    #         Head(
    #             Title("Airbnb - Hosting"),
    #             Style(
    #                 """
    #             @import url('https://fonts.googleapis.com/css2?family=Fredoka:wdth,wght@95.9,346&family=Roboto:ital,wght@0,100..900;1,100..900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
    #             body,html {
    #                 font-family: 'Fredoka', sans-serif;
    #                 margin: 0;
    #                 padding: 0;
    #                 overflow-x: hidden;
    #             }
    #             * {
    #                 margin: 0;
    #                 padding: 0;
    #             }

    #             .header{
    #                background-color: none;
    #                 width: 100%;

    #                  /* Added padding for spacing */
    #                 display: flex; /* Use flexbox for horizontal alignment */
    #                 justify-content: center; /* Space out logo and switch button */
    #                 align-items: center; /* Vertically center items */
    #               }
    #               .header-container {

    #                 display: flex;
    #                 align-items: center;
    #                 justify-content: space-between;
    #                 width: 100%;
    #                 padding: 10px 5%;
    #                 height:60px;
    #                 position: relative; /* Ensure it stays part of the document flow */
    #             }
    #             .logo-button{
    #                 background: none;
    #                 border: none;
    #                 cursor: pointer;
    #                 width: 50px;
    #                 height: 50px;
    #               }
    #             .right-button {
    #                 display: flex;
    #                 align-items: center;
    #                 gap: 10px; /* Space between Switch and Profile buttons */
    #             }
    #             .switch-button{
    #                background-color: white;
    #                 transition: all 0.3s;
    #                 font-family: 'Fredoka';
    #                 font-size: 16px;
    #                 border: none;
    #                 border-radius: 50px;
    #                 cursor: pointer;
    #                 width: 150px;
    #                 height: 38px;

    #               }
    #             .switch-button:hover{
    #               background-color: #e7e7e7;
    #               }
    #             .profile-button{

    #             }
    #             .profile-button-ui{
    #                 width: 70px;
    #                 height: 38px;
    #                 border-radius: 50px;
    #                 border-color: #e7e7e7;

    #                 border-width:1px;
    #                 transition: all 0.2s ease-in-out;
    #                 font-size: 20px;
    #                 font-family: Verdana, Geneva, Tahoma, sans-serif;
    #                 font-weight: 600;
    #                 display: flex;
    #                 align-items: center;
    #                 justify-content:center;
    #                 background: white;
    #                 color: #f5f5f5;
    #             }
    #             .profile-button-ui:hover{

    #                 box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);

    #             }

    #             .gray-line{
    #               background-color: #ededed;
    #                 height: 1px; /* Set the height of the gray line */
    #                 width: 100%; /* Make the gray line span the full width */
    #                 margin: 0;
    #                 padding: 0;
    #               }

    #             .welcome-section{
    #                 width:auto;
    #                 display:flex;
    #                 justify-content:center;
    #                 align-items:center;
    #                 flex-direction:column;
    #                 padding:0px 80px;
    #             }
    #             .in-welcome-text{

    #                 width:100%;
    #                 display:flex;
    #                 flex-direction:column;
    #                 padding:20px 20px;

    #             }
    #             .welcome-text{
    #                 padding:20px 0px;
    #                 font-weight:bold;
    #                 font-size:35px;
    #             }
    #             .your-reservation-text{
    #                 font-weight: normal;
    #                 padding:20px 0px;
    #                 font-size:26px;

    #             }
    #             .currently-hosting-container{
    #                 width:auto;
    #                 display:flex;
    #                 justify-content:center;
    #                 flex-direction:column;
    #                 padding:0px 80px;
    #                 gap:20px;
    #             }
    #             .currently-hosting-text{
    #                 font-size:20px;
    #             }
    #             .currently-hosting-box{

    #                 display:flex;
    #                 align-items:center;
    #                 justify-content:center;
    #                 flex-direction:column;
    #                 border-style: solid;
    #                 border-weight:50px;
    #                 border-color:#e0e0e0;
    #                 gap:10px;
    #                 background-color:#f7f7f7;
    #                 padding:10px;
    #                 border-radius:20px;
    #                 overflow-y: auto;

    #             }
    #             .card-hosting{
    #                 width:90%;
    #                 border-radius:20px;
    #                 background-color:white;
    #                 padding:20px;
    #                 width:auto
    #                 gap:10px;

    #             }
    #             .review-container{
    #                 width:auto;
    #                 display:flex;
    #                 justify-content:center;
    #                 flex-direction:column;
    #                 padding:20px 80px;
    #                 gap:20px;
    #             }
    #             .review-box{
    #                 display:flex;
    #                 align-items:center;
    #                 justify-content:center;
    #                 flex-direction:column;
    #                 border-style: solid;
    #                 border-weight:50px;
    #                 border-color:#e0e0e0;
    #                 gap:10px;
    #                 background-color:#f7f7f7;
    #                 padding:10px;
    #                 border-radius:20px;
    #                 overflow-y: auto;
    #             }
    #             .card-review{
    #             width:90%;
    #             border-radius:20px;
    #             background-color:white;
    #             padding:20px;
    #             width:auto
    #             gap:10px;
    #             }
    #             .review-text{
    #                 font-size:20px;
    #             }
    #             .blank-space{
    #                 width:100%;
    #                 padding:90px;
    #             }
    #                         """
    #             ),
    #         ),  # Set the tab title
    #         Body(
    #             Div(
    #                 Div(
    #                     A(
    #                         Button(
    #                             Img(
    #                                 src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/800px-Airbnb_Logo_B%C3%A9lo.svg.png",
    #                                 width=90,
    #                             ),
    #                             cls="logo-button",
    #                             # style="background: none; border: none; cursor: pointer; position: absolute; top: 20px; left: 25%; width:50px; height:50px"
    #                         ),
    #                         href="/",
    #                     ),
    #                     Div(
    #                         A(
    #                             Button("Switch to Traveling", cls="switch-button"),
    #                             href="/room",
    #                         ),
    #                         Div(
    #                             Button(
    #                                 Img(
    #                                     src="https://www.freeiconspng.com/thumbs/menu-icon/menu-icon-24.png",
    #                                     width=20,
    #                                 ),
    #                                 cls="profile-button-ui",
    #                             ),
    #                             cls="profile-button",
    #                         ),
    #                         cls="right-button",  # group switch button and profile button
    #                     ),
    #                     cls="header-container",
    #                 ),
    #                 cls="header",
    #             ),
    #             # grey line
    #             Div(cls="gray-line"),
    #             Div(
    #                 Div(
    #                     Div("Welcome back Bro ur Phone lingin!", cls="welcome-text"),
    #                     Div("Your reservations", cls="your-reservation-text"),
    #                     cls="in-welcome-text",
    #                 ),
    #                 cls="welcome-section",
    #             ),
    #             Div(
    #                 Div("Currently hosting :", cls="currently-hosting-text"),
    #                 Div(
    #                     *[
    #                         Div(
    #                             f"Accommodation: {accom['name']}, Address: {accom['address']}",
    #                             cls="card-hosting",
    #                         )
    #                         for accom in listmyaccom  # Looping through real data
    #                     ],
    #                     # *[
    #                     #     Div(
    #                     #         f"Accommodation: House {accom}, Address: {accom} Street, City",
    #                     #         cls="card-review",
    #                     #     )
    #                     #     for accom in range(1, 10)
    #                     # ],
    #                     cls="currently-hosting-box",
    #                 ),
    #                 cls="currently-hosting-container",
    #             ),
    #             Div(
    #                 Div("Reviews :", cls="review-text"),
    #                 Div(
    #                     *[
    #                         Div(
    #                             f"Accommodation: {review["accommodation"]}, Rating: {review["rating"]}, Name: {review["user"]}, Message: {review["message"]}",
    #                             cls="card-review",
    #                         )
    #                         for review in listreview
    #                     ],
    #                     cls="review-box",
    #                 ),
    #                 cls="review-container",
    #             ),
    #             Div(cls="blank-space"),
    #         ),
    #     )

    def get_html_price_summary(self, user_id, accom_id, form_data):
        controlsystem = self
        print(f"accom id in price = {accom_id}")
        accom_name = controlsystem.search_accomodation_by_id(accom_id).get_acc_name
        accom_address = controlsystem.search_accom_by_id(accom_id).get_address
        # print(accom_name)

        # ✅ Extract values from the form
        price_per_night = form_data.get("price-per-night")
        check_in = form_data.get("check-in")
        check_out = form_data.get("check-out")
        guests = form_data.get("guest-count")
        check_in_date = datetime.strptime(form_data.get("check-in"), "%Y-%m-%d")
        check_out_date = datetime.strptime(form_data.get("check-out"), "%Y-%m-%d")
        guests_int = int(form_data.get("guest-count"))

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
                            Input(
                                type="hidden", name="check_out", value=f"{check_out}"
                            ),
                            Input(type="hidden", name="accom_id", value=f"{accom_id}"),
                            Input(
                                type="hidden",
                                name="total_price",
                                value=f"{total_price}",
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

    def get_html_create_booking(
        self, user_id, check_in, check_out, accom_id, total_price, guests
    ):
        controlsystem = self
        print(
            f"Received data: user_id={user_id}, check_in={check_in}, check_out={check_out}, accom_id={accom_id}, total_price={total_price}, guests={guests}"
        )
        print(type(guests))
        print(type(total_price))
        try:

            guests = int(guests)  # Ensure it's an integer
            total_price = float(total_price)  # Ensure price is an integer
        except ValueError:
            return "Invalid data received", 400
        booking_item = controlsystem.create_booking(
            user_id, check_in, check_out, accom_id, guests
        )
        print(booking_item)
        if isinstance(booking_item, str):
            return P(booking_item)
        booking_id = booking_item.get_booking_id
        return booking_id

        # redirect to booking
        # return Redirect(f"/booking/{booking_id}")

        # return Div(Form(
        #     # Input(type="hidden", name="user_id", value=f"{user_id}"),
        #     # Input(type="hidden", name="booking_id", value=f"{booking_id}"),
        #     Button("Pay", type="submit", cls="reserve-shit"),
        #     method = "get",
        #     action = f"/booking/{booking_id}",
        # ))

    def show_accom_to_update(self):
        accom_to_update = []
        for accom in self.get_accommodation_list:
            detail = []
            detail.append(accom.get_id)
            detail.append(accom.get_status)
            accom_to_update.append(detail)

        return accom_to_update

    def approve_accommodation(self, accom_id):
        accom = self.search_accom_by_id(accom_id)
        result = accom.update_status()

        return result

    def get_member_id(self, name, email, phone_number, password):
        for i in self.__member_list:
            text, bool_check = i.login(name, email, phone_number, password)
            if bool_check == False:
                for i in self.__host_list:
                    text, bool_check = i.login(name, email, phone_number, password)
            if bool_check:
                return text
        return text

    def create_account(
        self, name: str, email: str, password: str, phone: str, age: int
    ):  # dew
        try:
            from .User import Member

            acount = Member(
                name=name, email=email, password=password, phone_num=phone, age=age
            )
            self.add_member(acount)
            return "Success"
        except:
            return "Fail to Sign Up"
        pass

    def deduction_period(self):
        for payment in self.get_payment_list:
            for period in payment.get_period_list:
                if period.get_status == False:
                    payment.get_pay_med.deduction(period.get_price)
                    period.update_status(True)
                    break

        return "Success"

    def create_accommodation(
        self, host_id, accom_type, name, address, info, price=None, **kwargs
    ):
        host = self.search_host_by_id(int(host_id))

        # Extract room details if it's a hotel
        rooms = []
        if accom_type == "Hotel":
            room_index = 1
            while f"room_type_{room_index}" in kwargs:
                room_type = kwargs[f"room_type_{room_index}"]
                room_price = int(kwargs[f"room_price_{room_index}"])
                room_count = int(kwargs[f"room_count_{room_index}"])
                rooms.append([room_type, room_price, room_count])
                room_index += 1
        print(rooms)
        # Create accommodation based on type
        if accom_type == "House":
            a = host.create_house(name, address, info, price)
            self.add_accommodation(a)

        else:  # Hotel
            a = host.create_hotel(
                name, address, info, rooms
            )  # Assuming create_hotel handles room lists
            self.add_accommodation(a)
        print(a)
        return "Success"
