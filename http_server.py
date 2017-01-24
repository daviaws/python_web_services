import asyncio
import aiohttp.server
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp import web
import aiohttp
import json

class HttpServer(object):

    def __init__(self, controller, ip="127.0.0.1", port=80):
        self.controller = controller
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
        
        self.app.router.add_route(
            '*',
            '/db/{resource}',
            self.handle_resource)

        self.app.router.add_route(
            '*',
            '/db/{resource}/{id}',
            self.handle_resource)

        self.app.router.add_route(
            'GET',
            '/server_available',
            self.server_available)
        
        response = web.StreamResponse()
        self.app.router.add_static(prefix='/', path='web/')

    @asyncio.coroutine
    def handle_resource(self, request):
        method = request.method
        res = ''
        if method == 'GET':
            res = self.handle_select(request)
        elif method == 'DELETE':
            res = self.handle_delete(request)
        elif method == 'PUT':
            res = yield from self.handle_insert(request)
        return web.json_response(res)

    def handle_select(self, request):
        resource = request.match_info.get('resource', None)
        r_id = request.match_info.get('id', None)
        if r_id is None:
            return self.controller.get_all(resource)
        else:
            return self.controller.get(resource, r_id)

    def handle_delete(self, request):
        resource = request.match_info.get('resource', None)
        r_id = request.match_info.get('id', None)
        if r_id is None:
            return self.controller.delete_all(resource)
        else:
            return self.controller.delete(resource, r_id)

    @asyncio.coroutine
    def handle_insert(self, request):
        resource = request.match_info.get('resource', None)
        representation = yield from request.json()
        return  self.controller.insert(resource, representation)

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
