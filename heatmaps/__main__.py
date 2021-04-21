"""Main entrypoint for running the project."""
import os

from dotenv import find_dotenv, load_dotenv

from heatmaps.server import app

load_dotenv(find_dotenv())


HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

if PORT:
    PORT = int(PORT)

# if debug env var is not set, assume it is True
DEBUG = False if os.environ.get("DEBUG") else True
# if DEBUG is false, don't display access_logs either
ACCESS_LOG = DEBUG


app.run(host=HOST, port=PORT, debug=DEBUG, access_log=ACCESS_LOG)
