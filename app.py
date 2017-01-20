# -*- coding: utf-8 -*-
# IMPORTS
import asyncio
import json


from http_server import HttpServer
import ssl

try:
    import signal
except ImportError:
    signal = None

def create_http_server():
    global http_server
    http_server = HttpServer()


def create_loop():
    global loop

    loop = asyncio.get_event_loop()
    if signal is not None:
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    create_http_server()
    http_server.run()

def run_service():
    global loop
    loop.run_forever()

# MAIN
if __name__ == "__main__":
    global loop
    global http_server

    create_loop()
    run_service()
