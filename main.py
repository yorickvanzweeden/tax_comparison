from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler

from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from dashboard import dashboard

io_loop = IOLoop.current()

bokeh_app = Application(FunctionHandler(dashboard))

server = Server({'/': bokeh_app}, io_loop=io_loop, debug=True, autoreload=True)
server.start()

if __name__ == '__main__':
    print("Autoreload")
    io_loop.start()
