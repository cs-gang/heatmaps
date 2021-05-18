"""Main entrypoint for running the project."""
import os

from dotenv import find_dotenv, load_dotenv

from heatmaps.server import app

# import index file so the code there is run
# and the route is registered
from heatmaps import index  # noqa: F401


load_dotenv(find_dotenv())


HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8000))


# if debug env var is not set, assume it is True
DEBUG = True if os.environ.get("DEBUG") else False
# if DEBUG is false, don't display access_logs either
ACCESS_LOG = DEBUG

app.run(host=HOST, port=PORT, debug=DEBUG, access_log=ACCESS_LOG)
