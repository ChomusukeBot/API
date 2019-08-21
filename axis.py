import os

import sanic

from tools import parse_url


# Create the basic Sanic application
APP = sanic.Sanic()


@APP.route("/")
async def home(request):
    """
    Basic endpoint that redirects to the GitHub organization.
    """
    return sanic.response.redirect("https://github.com/ChomusukeBot",
                                   status=302)


@APP.route("/github")
async def github(request):
    """
    Endpoint that handles the GitHub login basics.
    """
    # If there is no GitHub Client or Secret, return a 503 Service Unavailable
    if "GITHUB_CLIENT" not in os.environ or "GITHUB_SECRET" not in os.environ:
        return sanic.response.text("GitHub is not supported at this time.",
                                   status=503)

    # If there is no Discord ID on the query string
    if "id" not in request.args:
        return sanic.response.text("The Discord ID was not specified",
                                   status=400)

    # Otherwise, return a 301 with the correct URL
    return sanic.response.redirect(parse_url(request.url) + "/github/callback",
                                   status=301)
