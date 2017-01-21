# -*- coding: utf-8 -*-
# IMPORTS
import asyncio
import json


from resource_handler import Controller, PersonHandler
from http_server import HttpServer

try:
    import signal
except ImportError:
    signal = None

def create_controller():
    global controller
    handler = PersonHandler()
    controller = Controller()
    controller.add_handler('person', handler)

def create_loop():
    global loop

    loop = asyncio.get_event_loop()
    if signal is not None:
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    create_http_server()
    http_server.run()

def create_http_server():
    global http_server
    http_server = HttpServer(controller)

def run_service():
    global loop
    loop.run_forever()

# MAIN
if __name__ == "__main__":
    global loop
    global controller
    global http_server

    create_controller()
    create_loop()
    run_service()
