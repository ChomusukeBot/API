import sanic


# Create the basic Sanic application
APP = sanic.Sanic()


@APP.route("/")
async def home(request):
    """
    Basic endpoint that redirects to the GitHub organization.
    """
    return sanic.response.redirect("https://github.com/ChomusukeBot",
                                   status=302)
