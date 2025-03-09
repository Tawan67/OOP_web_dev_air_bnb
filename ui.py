from merge.accomodation import *
from merge.control import *
from merge.booking_class import *
from merge.payment import *
from merge.user import *

from fasthtml.common import *
app, rt = fast_app()
# from merge.accomodation import *
# from merge.booking_class import *
# from merge.control import *
# from merge.payment import *
# # from merge.user import *

# from .testModule import add_data


# def add_data():
#     control_system = ControlSystem()

#     # Creating 10 Members
#     members = [
#         Member(name=f"Member{i}", email=f"member{i}@example.com", password=f"pass{i}",
#                phone_num=f"12345678{i}", age=20 + i) for i in range(1, 11)
#     ]

#     # Creating 10 Hosts
#     hosts = [
#         Host(name=f"Host{i}", email=f"host{i}@example.com", password=f"hostpass{i}",
#              phone_num=f"98765432{i}", age=30 + i) for i in range(1, 11)
#     ]

#     # Creating 5 Houses & 5 Hotels (10 Accommodations)
#     accommodations = [
#         House(name=f"House{i}", address=f"{i} Street, City",
#               info=f"A cozy house {i}", price=100 + (i * 10))
#         for i in range(1, 6)
#     ] + [
#         Hotel(name=f"Hotel{i}", address=f"{i * 10} Avenue, City",
#               info=f"A luxury hotel {i}")
#         for i in range(6, 11)
#     ]

#     # Creating 10 Rooms and assigning them to Hotels
#     rooms = [
#         Room(room_id=i, room_floor=(i % 5) + 1, price=150 + (i * 5),
#              hotel_address=f"{(i % 5) * 10} Avenue, City", hotel_name=f"Hotel{6 + (i % 5)}")
#         for i in range(1, 11)
#     ]

#     # Assigning Rooms to Hotels
#     for i, room in enumerate(rooms):
#         accommodations[5 + (i % 5)].add_room(room)

#     # Creating 10 Bookings
#     bookings = [
#         Booking(accom=accommodations[i % 10], date=f"2025-03-{10 + i}",
#                 guess=(i % 4) + 1, member=members[i % 10])
#         for i in range(1, 11)
#     ]

#     # Creating 5 Debit & 5 Credit Payment Methods
#     payments = [
#         Debit(bank_id=f"1234{i}", user=members[i % 10],
#               balance=5000 + (i * 500), password=f"debitpass{i}")
#         for i in range(1, 6)
#     ] + [
#         Credit(bank_id=f"5678{i}", user=members[i % 10],
#                balance=7000 + (i * 300), password=f"creditpass{i}")
#         for i in range(6, 11)
#     ]

#     # Creating 10 Reviews
#     reviews = [
#         Review(rating=(i % 5) + 1,
#                user=members[i % 10], message=f"Review {i}: Great place!")
#         for i in range(1, 11)
#     ]

#     # Assigning Reviews to Accommodations
#     for i, review in enumerate(reviews):
#         accommodations[i % 10].add_review(review)

#     # Creating 10 Payments linked to Bookings
#     payment_instances = [
#         Payment(period=(i % 3) + 1,
#                 pay_med=payments[i % 10], price=300 + (i * 50))
#         for i in range(1, 11)
#     ]

#     # Creating 10 Booked Dates
#     booked_dates = [
#         BookedDate(checkindate=f"2025-04-{5 + i}",
#                    checkoutdate=f"2025-04-{10 + i}")
#         for i in range(1, 11)
#     ]

#     # Adding Everything to Control System
#     for member in members:
#         control_system.add_member(member)

#     for host in hosts:
#         control_system.add_host(host)

#     for accom in accommodations:
#         control_system.add_accommodation(accom)

#     for booking in bookings:
#         control_system.add_booking(booking)

#     return control_system


# # control_system = add_data()

con_2 = ControlSystem()

member_A = Member("Tawan", "kajuYai@jmail.com",
                  "JuuKodYai", "0901234567", 23)
member_B = Member("Natthakorn", "kajuLagMag@jmail.com",
                  "JuuKodLAKE", "0911234567", 23)
accom_A = Accommodation("JeawLeg", "add_dda",
                        "accom for some one who has a big HEART", 123)
accom_B = Accommodation("Accom_B", "america", "none", 200)
host_B = Host("B", "B@gmail.com", "any", "0201234567", 97)
host_A = Host("tord", "tod@jmail.com", "abcdefg", "0907654321", 23)
host_B.add_accommodation(accom_B)
result = host_A.add_accommodation(accom_A)

accom_A.add_accom_pics(
    "https://i.pinimg.com/236x/b4/7f/a3/b47fa3f0501e1978d8b195d79ef2c5fa.jpg")
accom_B.add_accom_pics(
    "https://thomaskinkade.com/cdn/shop/collections/Harry_Potter__Hogwarts__Castle.jpg?v=1708955739&width=800")
accom_B.create_review(2, member_A, "Ohhh")
accom_A.create_review(5, member_A, "fuck bro")
accom_A.create_review(3, member_B, "fuck -bro")
print(accom_A.get_accom_pics)
print(f"add accom's result is {result}")

con_2.add_member(member_A)
con_2.add_accommodation(accom_A)
con_2.add_host(host_A)

con_2.add_member(member_B)
con_2.add_accommodation(accom_B)
con_2.add_host(host_B)

mem_id = str(member_A.get_user_id)
# mem_id = str(mem_id)
start_date = "2025-03-02"
end_date = "2025-03-07"
booked_date = start_date + '+'+end_date
guest_amount = '3'
accom_id2 = str(accom_B.get_id)
accom_id = str(accom_A.get_id)
price = 4*accom_A.get_one_price
price = str(price)
price_B = 4*accom_B.get_one_price
price_B = str(price_B)
reset = Booking("a", 2, 3, 4)
reset.reset_id
book_item = con_2.create_booking(
    booked_date, guest_amount=guest_amount, accom_id=accom_id, price=price, menber_id=mem_id)
book_item_B = con_2.create_booking(
    booked_date, guest_amount=guest_amount, accom_id=accom_id2, price=price_B, menber_id=mem_id)

book_item.create_booked_date(start=start_date, end=end_date)
book_item_B.create_booked_date(start=start_date, end=end_date)
print(f"/booking/{mem_id}/{start_date}/{guest_amount}/{accom_id}")

book_id = book_item.get_booking_id
book_id2 = book_item_B.get_booking_id
print(book_id2)


@rt('/')
def get():

    book_id = "1"
    book_id2 = "2"
    return Div(P('Airbnb พ่อทุกสภาบัน'), P(f"{book_id}", P(f"{book_id2}")),
               Form(Button("reserve"), method='get',
                    action=f"/booking/{book_id}"),
               Form(Button("reserve"), method='get',
                    action=f"/booking/{book_id2}"),
               )


@rt('/booking/{book_id}')
def get(book_id: str):

    if not book_id:
        return Titled("ข้อผิดพลาด", P("ไม่พบหมายเลขการจอง กรุณาลองใหม่"))
    pay_div = None
    if (pay_div != None):
        pay_div = Div(
            H3("Pay With"),

            Form(  # start FORM
                Label("Choose Payment:"),
                Select(
                    Option("One Time", value="one_time", id="one_time"),
                    Option("Parts", value="parts"),
                    id="payment",
                    name="payment",
                    onchange="toggleInstallments()"
                ),
                Div(
                    Label("Choose Period:"),
                    Select(
                        Option("2", value="2"),
                        Option("4", value="4"),
                        Option("6", value="6"),
                        id="installments",
                        name="period"
                    ),
                    id="installmentsDiv",
                    name="period_div",
                    style="display: none;"
                ),
                Label("Debit or Credit:"),
                Select(
                    Option("Debit", value="debit"),
                    Option("Credit", value="credit"),
                    id="paymed",
                    name="paymed"
                ),
                Label("Card Number:"),
                Input(type="text", id="card_number", name="card_num",
                      placeholder="Enter your card number"),
                Label("Expiration Date:"),
                Input(type="date", id="expiration_date",
                      name="expiration_date"),
                Label("Password:"),
                # Input(type="text", id="cvv", placeholder="Enter CVV"),
                Input(type="password", id="cvv", name="password",
                      placeholder="Enter Password"),
                Input(type="hidden", name="user_id",
                      value="{{user_id}}"),
                Input(type="hidden", name="booking_id",
                      value=f"{book_id}"),
                Button("Confirm and Pay", type="submit"),
                method="post",
                action="/create_pay"

            ),  # endform
            style="width:50%"
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
                """),
                href="/"),

            style="""
        padding: 15px;
        height:80px;
        align-items: center;
        """
        ),  # head

        Hr(),
        # back button
        Div(

            A(
                Button("<", style="""
                    background-color:white;
                    color:black;
                    border: 2px solid black;
                    border-radius: 8px;
                    font-size:20px"""
                       ),
                href="/back"
            ),
            H1(
                "Confirm and pay", style=""" color:black;"""
            ),

            style="""
        padding-left: 15px;
        width:400px;
        height : 100px ;
        background-color: white;
        display:flex;
        justify-content: space-between;
        
        """
        ),
        Hr(
            style=""" padding: 10 px;
          background-color: blue px;"""),

        # main block
        Div(
            Div(  # left side
                Div(H3("Your trip", style=""" color:black;""")),
                Div(
                    H6("Dates", style="color:black;"),
                    Div(
                        P(con_2.details_date_by_booking_id(book_id),
                          style="flex:1; text-align:left;color:black;"),
                        A(P("Edit", style="text-align:right;color:black;"),
                          href=f"/edit_date_guest/{book_id}"),
                        style="display:flex; justify-content: space-between; align-items: center;height:20px; "
                    ),
                    Div(
                        H6("Guest", style="color:black;"),
                        Div(
                            P(f"{con_2.get_guest_amount(book_id)} guest",
                              style="flex:1; text-align:left;color:black;"),
                            A(P("Edit", style="text-align:right;color:black;gap:30px; "),
                              href=f"/edit_date_guest/{book_id}"),
                            style="display:flex; justify-content: space-between; align-items: center;height:20px;"
                        )
                    ),
                    style="width:400px"
                ),  # Pay and Post
                pay_div,
                Script("""
                function toggleInstallments() {
                    let paymentSelect = document.getElementById("payment");
                    let installmentsDiv = document.getElementById("installmentsDiv");
                    if (paymentSelect.value === "parts") {
                        installmentsDiv.style.display = "block";
                    } else {
                        installmentsDiv.style.display = "none";
                    }
                }
            """),
                style="width: 50%; background-color: white; padding: 20px;color:black;overflow-y: auto;"

            ),  # end post

            # right
            Div(
                Div(
                    Div(
                        Div(
                            Img(src=con_2.get_pic_from_book_id(book_id),
                                style="width:100%; height:auto; border-radius:8px;"),
                            style="width:30%;"
                        ),
                        Div(
                            H4(con_2.get_accom_name(book_id),
                               style="margin: 0; padding-left: 10px;"),
                            P("Rating :"+con_2.get_av_rating(book_id)+"⭐",
                              style="margin: 0; padding-left: 10px;"),
                            style="width:70%; display:flex; flex-direction:column; justify-content:center;"
                        ),
                        style="""display:flex;
                    align-items:center; 
                    gap:10px; 
                    background-color: white; 
                    padding: 10px; 
                    border-radius:8px;
                    width:500px"""
                    ),
                    Card(
                        Table(
                            Tr(Td("$"+con_2.get_price_per_night(book_id)+" x "+con_2.get_night(book_id)+" nights",
                                  style="background-color:white;color:black;"),
                               Td("$"+con_2.get_total_price_to_show(book_id),
                                  style="background-color:white;color:black;")
                               ),
                            Tr(Td("fee",
                                  style="background-color:white;color:black;"),
                               Td("$"+con_2.get_fee(book_id),
                                  style="background-color:white;color:black;")
                               ),
                            style="background-color:white;"
                        ),
                        header=H4("Price Details",
                                  style="background-color:white;color:black;"),
                        footer=Div(Div(H6("Total Price"), style="text-align:left"),
                                   Div(H6("$"+con_2.get_all_price(book_id)),
                                   style="text-align:right"),
                                   style="""background-color:white;
                            color:black;
                            display:flex;
                            justify-content: space-between""",
                                   #    style="display:flex; justify-content: space-between; align-items: center"
                                   ),
                        style="background-color:white;padding:15px;width:500px"
                    ),
                    style="""width: 100%;
            background-color: white;
            items-align:center;
            padding:50px;
            border: 2px solid black;
            border-radius: 8px;
            padding-left:10px"""
                )),


            style="display: flex; flex-direction: row; height: 100vh;padding-right: 15px;padding-left: 15px;"

        ),
        Hr(
            style=""" padding: 10 px;
          background-color: blue px;"""),
        style=""" padding: 0px;
    background-color : white;
    
    """

    )


@rt('/create_pay')
def post(payment: str, period: str,
         paymed: str, card_num: str, expiration_date: str, password: str, booking_id: str):
    if con_2.check_expiraion_date(expiration_date):
        result = con_2.post_payment(payment, paymed, booking_id, card_num, password,
                                    period, balance=1000.00)
    else:
        return Div(H2("Can't Booking Your Card has Gone I'm sorry but you have to move on to a New Card",
                      style="padding : 30px;color:black;"),
                   A(Button("Go back", style="padding:30px"),
                     href=f"/booking/{booking_id}"),
                   style="""padding: 20px; 
                   text-align: center;
                   background-color: #f4f4f4;
                   height: 100vh;
                   color:black;
                   font-size:16;
                   flex-direction: column;
                    display:flex;
                    align:center;
                   """)

    return Div(
        H3(f"Payment Confirmation for Booking {booking_id}"),
        P(f"Payment Method: {paymed}"),
        P(f"Card Number: {card_num}"),
        P(f"Total Amount: {con_2.get_all_price(booking_id)}"),
        Button("Back to Home", action="/"),
        style="padding: 20px;"
    )
    pass


@rt('/back')
def get(): return Img(src="https://img.salehere.co.th/p/1200x0/2021/06/07/ukl94htmsyja.jpg")


@rt('/edit_date_guest/{book_id}')
def get(book_id: str):
    return Div(
        Div(H1("Edit Booking Date & Guests",
               style="text-align: center; color: black; margin-bottom: 20px;")),
        Div(Form(
            Div(Label("Start Date:", style="color: black;"),
                Input(type="date", id="start", name="start"),
                style="padding-bottom: 10px; display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;"
                ),
            Div(Label("End Date:", style="color: black;"),
                Input(type="date", id="end", name="end"),
                style="padding-bottom: 10px; display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;"
                ),
            Div(Label("Guest Amount:", style="color: black;"),
                Input(type="number", id="guest_amount",
                      name="guest_amount", min="1", max="10"),
                style="padding-bottom: 10px; display: flex; flex-direction: column; align-items: center; margin-bottom: 15px;"
                ),
            Button("Confirm", type="submit",
                   style="background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px;"),
            method="post",
            action=f"/update_date_guest/{book_id}",
            style="""
            display: flex; flex-direction: column; align-items: center; 
            background-color: white; padding: 20px; width: 100%; 
            margin: auto; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            """
        )),
        style="""display: flex;
        flex-direction: column;
        justify-content: center; 
        align-items: center;
        height: 100vh;
        background-color: #f4f4f4;"""
    )


@rt('/update_date_guest/{book_id}')
def update(start: str, end: str, guest_amount: str, book_id: str):
    # อัปเดตวันที่และจำนวนแขกใน booking
    # return P(f"{book_id}")
    date_result = con_2.update_date(book_id, start, end)
    guest_result = con_2.update_guest(book_id, guest_amount)
    return Redirect(f"/booking/{book_id}")  # ส่งผู้ใช้กลับไปยังหน้าจอง
    return Div(
        H1(f"Booking updated successfully!",
           style=""" text-align: center; background-color: #f4f4f4;color:black;"""
           ),
        H1(f"Booking updated date is {date_result}!", style=""" text-align: center; background-color: #f4f4f4;color:black;"""
           ),
        H1(f"Booking updated guest amount is {guest_result}!",
           style=""" text-align: center; background-color: #f4f4f4;color:black;"""),
        A(Button("Go back to Booking",
                 style=""" text-align: center;
                 background-color:#88E788;
                 color:black;"""), href=f"/booking/{book_id}",
          style=""" text-align: center; background-color: #f4f4f4;color:black;"""),
        style="""padding: 20px; text-align: center; background-color: #f4f4f4;height: 100vh;"""
    )


serve(port=9008)  # ใส่เลขพอร์ตเข้าไปได้ defalt อยู่ทืี 5001
