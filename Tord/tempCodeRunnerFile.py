@rt('/')
def home():
    # Format booked dates as a readable string
    booked_dates_str = ""
    booked_dates = my_booking.get_accommodation.get_book_dates
    if booked_dates:
        booked_dates_str = ", ".join(
            f"{bd.get_checkindate().strftime('%Y-%m-%d')} to {bd.get_checkoutdate().strftime('%Y-%m-%d')}"
            for bd in booked_dates
        )
    else:
        booked_dates_str = "No booked dates yet"

    return Html(
        Head(Title('Payment Form'), get_style()),
        Body(
            Div(
                H1('Complete Your Booking Payment'),
                Form(
                    Fieldset(
                        Legend('Booking Summary'),
                        Div(
                            P(f'Accommodation: {accom_name}'),
                            P(f'Address: {accom_address}'),
                            P(f'Booked Dates: {booked_dates_str}'),  # Improved display
                            P(f'Guests: {guess}'),
                            P(f'Check-in: {checkin.strftime("%Y-%m-%d %H:%M")}'),
                            P(f'Check-out: {checkout.strftime("%Y-%m-%d %H:%M")}'),
                            P(f'Total Price: ${booking_price * guess}'),
                            cls='payment-details'
                        )
                    ),
                    # [Rest of the form remains unchanged]
                    Fieldset(
                        Legend('Payment Details'),
                        Div(
                            Label('Payment Method'),
                            Select(
                                Option('Credit Card', value='credit'),
                                Option('Bank Transfer', value='bank'),
                                name='payment_type'
                            ),
                            cls='form-group'
                        ),
                        Div(
                            Label('Card Number'),
                            Input(type='text', name='card_number', placeholder='XXXX-XXXX-XXXX-XXXX', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('Card Holder Name'),
                            Input(type='text', name='card_holder', placeholder='John Doe', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('Expiration Date'),
                            Input(type='month', name='expiry_date', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('CVV'),
                            Input(type='text', name='cvv', placeholder='123', maxlength='4', required=True),
                            cls='form-group'
                        ),
                        Div(
                            Label('Billing Address'),
                            Textarea(name='billing_address', rows='3', placeholder='Enter your billing address', required=True),
                            cls='form-group'
                        )
                    ),
                    P(f'Card Number: {control_system.get_member_list[0].get_payment_method[0].get_id}'),
                    P(f'Current Balance: ${control_system.get_member_list[0].get_payment_method[0].get_balance}'),
                    P(f'Point: {control_system.get_member_list[0].get_payment_method[0].get_point}'),
                    Button('Process Payment', type='submit'),
                    action='/process_payment',
                    method='post'
                ),
                cls='container'
            )
        )
    )
