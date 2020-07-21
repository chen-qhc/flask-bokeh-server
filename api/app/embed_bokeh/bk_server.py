from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import asyncio


def bk_worker(bk_app_function, sockets):
	 # can't use shortcuts here, since we are passing to low level BokehTornado
	bkapp = Application(FunctionHandler(bk_app_function))

	asyncio.set_event_loop(asyncio.new_event_loop())

	bokeh_tornado = BokehTornado({'/bkapp': bkapp}, extra_websocket_origins=["localhost:8000"])
	bokeh_http = HTTPServer(bokeh_tornado)
	bokeh_http.add_sockets(sockets)

	server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
	server.start()
	server.io_loop.start()
