from fasthtml.common import *


app, rt = fast_app()


@rt("/")
def get():
    return Html(
        Head(Title("Airbnb - Home")),  # Set the tab title
        Body(A(Button("Select Room"), href="/room")),
    )


@rt("/room")
def room():
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
                    }
                }

                function decreaseGuests() {
                    if (guestCount > 0) {
                        guestCount--;
                        document.getElementById("guest-count").textContent = guestCount;
                    }
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
                            href="/Hosting",
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
                    Div("Elon Musk's White House Toilet", cls="hotel-name"),
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
                        src="https://i0.wp.com/hyperallergic-newspack.s3.amazonaws.com/uploads/2018/01/IMG_5897-1-768x1024.jpg?resize=768%2C1024&quality=90&ssl=1",
                        cls="big-image",
                    ),
                    Div(
                        Img(
                            src="https://i0.wp.com/hyperallergic-newspack.s3.amazonaws.com/uploads/2018/01/IMG_5897-1-768x1024.jpg?resize=768%2C1024&quality=90&ssl=1",
                            cls="small-image",
                        ),
                        Img(
                            src="https://i0.wp.com/hyperallergic-newspack.s3.amazonaws.com/uploads/2018/01/IMG_5897-1-768x1024.jpg?resize=768%2C1024&quality=90&ssl=1",
                            cls="small-image",
                        ),
                    ),
                    Div(
                        Img(
                            src="https://i0.wp.com/hyperallergic-newspack.s3.amazonaws.com/uploads/2018/01/IMG_5897-1-768x1024.jpg?resize=768%2C1024&quality=90&ssl=1",
                            cls="small-image",
                        ),
                        Img(
                            src="https://i0.wp.com/hyperallergic-newspack.s3.amazonaws.com/uploads/2018/01/IMG_5897-1-768x1024.jpg?resize=768%2C1024&quality=90&ssl=1",
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
                    Div("1600 Pennsylvania Avenue in Washington, D.C", cls="address"),
                    Div(
                        Div("Hosted by", cls="host-by"),
                        Div("Elon Musk", cls="name"),
                        cls="host-by-name",
                    ),
                    cls="info-room",
                ),
                cls="info-section",
            ),
            Div(
                Div("About this place :", cls="about-this-place"),
                Div(
                    "This place is so cozy and peaceful bla bla bla bla o ii a i o i i ia  bla bla bla bla o ii a i o i i ia  bla bla bla bla o ii a i o i i ia  bla bla bla bla o ii a i o i i ia  bla bla bla bla o ii a i o i i ia",
                    cls="about-text",
                ),
                cls="hotel-about-section",
            ),
            Div(
                Form(
                    Div("25,000 night", cls="price-per-night"),
                    Div(
                        Input(type="date", cls="check-in-date", required=True),
                        Input(type="date", cls="check-out-date", required=True),
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
                        Span(
                            "0", id="guest-count", cls="guest-count"
                        ),  # Display guest count
                        Button(
                            "+",
                            cls="plus-btn",
                            onclick="increaseGuests()",
                            type="button",
                        ),
                        cls="guest-selection",
                    ),
                    Div("Total price = 25,000", cls="total-price"),
                    Div(
                        Button("Submit", type="submit", cls="submit-price-button"),
                        cls="submit-button",
                    ),
                    cls="price-box",
                ),
                cls="price-section",
            ),
        ),
    )


@rt("/Hosting")
def get():
    return Html(
        Head(
            Title("Airbnb - Hosting"),
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
                
                .welcome-section{
                    width:auto;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    flex-direction:column;
                    padding:0px 80px;
                }
                .in-welcome-text{
                    
                    width:100%;
                    display:flex;
                    flex-direction:column;
                    padding:20px 20px;
                    
                }
                .welcome-text{
                    padding:20px 0px;
                    font-weight:bold;
                    font-size:35px;
                }
                .your-reservation-text{
                    font-weight: normal;
                    padding:20px 0px;
                    font-size:26px;

                }
                .currently-hosting-container{
                    width:auto;
                    display:flex;
                    justify-content:center;                   
                    flex-direction:column;
                    padding:0px 80px;
                    gap:20px;
                }
                .currently-hosting-text{
                    font-size:20px;
                }
                .currently-hosting-box{
                    border-style: solid;
                    border-weight:50px;
                    border-color:#e0e0e0;
                    padding:20px 20px;
                    background-color:#f7f7f7;
                    height:200px;
                    border-radius:20px;
                }
                .review-container{
                    width:auto;
                    display:flex;
                    justify-content:center;                   
                    flex-direction:column;
                    padding:20px 80px;
                    gap:20px;
                }
                .review-box{
                    border-style: solid;
                    border-weight:50px;
                    border-color:#e0e0e0;
                    padding:20px 20px;
                    background-color:#f7f7f7;
                    height:200px;
                    border-radius:20px;
                }
                .review-text{
                    font-size:20px;
                }
                .blank-space{
                    width:100%;
                    padding:90px;
                }
                            """
            ),
        ),  # Set the tab title
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
                            Button("Switch to Traveling", cls="switch-button"),
                            href="/room",
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
                    Div("Welcome back Bro ur Phone lingin!", cls="welcome-text"),
                    Div("Your reservations", cls="your-reservation-text"),
                    cls="in-welcome-text",
                ),
                cls="welcome-section",
            ),
            Div(
                Div("Currently hosting :", cls="currently-hosting-text"),
                Div(cls="currently-hosting-box"),
                cls="currently-hosting-container",
            ),
            Div(
                Div("Reviews :", cls="review-text"),
                Div(cls="review-box"),
                cls="review-container",
            ),
            Div(cls="blank-space"),
        ),
    )


serve()
