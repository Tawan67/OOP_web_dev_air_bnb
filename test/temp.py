from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("User Registration",
                  Form(Input(type="text", name="username", placeholder="Username"),
                       Button("Register", type="submit"),
                       hx_post="/register",
                       hx_target="#result"),
                  Div(id="result"))

@rt("/register")
async def post(req):
    form_data = await req.form()  # Get form data asynchronously
    username = form_data.get("username", "")
    return Div(f"Registered: {username}", id="result", style="color: green;")

serve()