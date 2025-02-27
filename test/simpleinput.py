from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("User Registration",
                  Form(Input(type="text", name="username", placeholder="Username"),
                       Button("Register", type="submit"),
                       action="/register",  # Standard form action
                       method="post"),      # Standard POST method
    )
    
@rt("/register")
async def post(req):
    form_data = await req.form()  # Get form data asynchronously
    username = form_data.get("username", "")
    return Titled("Registration Success",
                  H1(f"Registered: {username}"),
                  A("Back to registration", href="/"))

serve()