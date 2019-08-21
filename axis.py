import os
import sanic
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from tools import parse_url

# The authentication redirection URLs
AUTH_GITHUB = "https://github.com/login/oauth/authorize?client_id={0}&redirect_uri={1}"  # noqa: E501

# Load the .env and unload the lib
load_dotenv()
del load_dotenv

# Create the basic Sanic application
APP = sanic.Sanic()
# If there is a MongoDB URL on the env. variables
if "MONGO_URL" not in os.environ:
    # Create the instance and make sure that is valid
    MONGO = AsyncIOMotorClient(os.environ["MONGO_URL"])
    MONGO.admin.command("ismaster")
else:
    # Otherwise, just set the instance to None
    MONGO = None


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

    # Format the URL that we are going to redirect to
    redirect = "{0}/github/callback".format(parse_url(request.url))
    url = AUTH_GITHUB.format(os.environ["GITHUB_CLIENT"], redirect)
    # And return a 301 with the correct URL
    return sanic.response.redirect(url, status=301)
