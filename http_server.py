import asyncio
import aiohttp.server
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp import web
import aiohttp
import json

RESOURCE_NAME = 'resource'

class HttpServer(object):

    def __init__(self, ip="10.100.11.12", port=80):
        self.app = None
        self.ip = ip
        self.port = port
        self.loop = asyncio.get_event_loop()
    def set_sslcontext(self, sslcontext):
        self.sslcontext = sslcontext

    def run(self):
        self.app = web.Application()
        self.map_http_routes()
        self.run_loop()

    def run_loop(self):
        handler = self.app.make_handler(
            headers={'server': 'Secured Server Software'})
        server = self.loop.create_server(handler, self.ip, self.port)
        srv = self.loop.run_until_complete(server)
        print('HTTP Server running on {}'.format(
                srv.sockets[0].getsockname()))

    def map_http_routes(self):
        self.app.router.add_route('GET', '/', self.go_to_index)
        
        # self.app.router.add_route(
        #     'GET',
        #     '/person',
        #     self.server_available)

        self.app.router.add_route(
            '*',
            '/{resource}/{id}',
            self.handle_resource, name='resource_handler')

        self.app.router.add_route(
            'GET',
            '/server_available',
            self.server_available)
        
        response = web.StreamResponse()
        self.app.router.add_static(prefix='/', path='web/')

    def handle_values(self, items):
        representation = {}
        for item in items:
            print(item)
            if item[0] != RESOURCE_NAME:
                representation[item[0]] = item[1]
        return representation

    @asyncio.coroutine
    def handle_resource(self, request):
        resource = request.match_info.get('resource', "Anonymous")
        method = request.method
        representation = self.handle_values(request.match_info.items())
        response = json.dumps(representation)
        return web.Response(text=response)

    @asyncio.coroutine
    def handle_with_query(self, request):
        resource = request.match_info.get('resource', "Anonymous")
        method = request.method
        representation = self.handle_values(request.match_info.items())
        response = json.dumps(representation)
        return web.Response(text=response)

    @asyncio.coroutine
    def go_to_index(self, request):
        method = ""
        port = ""
        method = "http"
        msg = '﻿<meta http-equiv="refresh" content="0; url={}://{}:{}/index.html">'.format(
            method, self.ip, self.port)
        return web.Response(text=msg, content_type='text/html')

    @asyncio.coroutine
    def server_available(self, request):
        return web.Response(text=json.dumps({"connected": True}))
