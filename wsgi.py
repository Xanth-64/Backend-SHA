# -*- coding: utf-8 -*-
"""Web Server Gateway Interface"""

from os import environ
from src.app import create_app

# Production Mode
app = create_app()

if __name__ == "__main__":
    # Development mode
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", default=False, help="debug mode"
    )
    args = parser.parse_args()
    port = environ.get("PORT") if environ.get("PORT") else args.port
    debug = args.debug
    app = create_app()

    app.run(host="0.0.0.0", port=port, debug=debug)
