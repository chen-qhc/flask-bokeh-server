from app import app
from flask import render_template
from bokeh.embed import server_document
from bokeh.server.util import bind_sockets
from threading import Thread

from app.embed_bokeh.bk_server import bk_worker
from app.embed_bokeh.bk_app import add_plot_to_doc

# This is so that if this app is run using something like "gunicorn -w 4" then
# each process will listen on its own port
sockets, port = bind_sockets("localhost", 0)

@app.route('/')
def index():
    script = server_document('http://localhost:%d/bkapp' % port)
    return render_template("embed.html", script=script)

def run_bk_server():
    bk_worker(add_plot_to_doc, sockets)

t = Thread(target=run_bk_server)
t.daemon = True
t.start()
