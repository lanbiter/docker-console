from flask import Flask
from flask import render_template
from flask_sockets import Sockets
import docker
import time
import configure 


app = Flask(__name__)
sockets = Sockets(app)
docker_client = docker.Client(base_url=configure.DOCKER_HOST,
         version=configure.DOCKER_API_VERSION,timeout=configure.TIME_OUT)


@app.route('/')
def hello_world():
    return render_template('index.html')

def create_exec():
   command = ["bash"]
   create_exec_options = {
       "tty": True,
       "stdin": True,
   }
   exec_id = docker_client.exec_create(configure.CONTAINER_ID, command, **create_exec_options)
   return exec_id

@sockets.route('/echo')
def echo_socket(ws):
    exec_id = create_exec()
    sock = docker_client.exec_start(exec_id, detach=False, tty=True, stream=False,
                   socket=True)
    while not ws.closed:
        message = ws.receive()
        sock.send(message)
        print message
        time.sleep(0.2)
        resp = sock.recv(1024)
        print 'resp:',resp
        if resp is not None:
            ws.send(resp)


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

