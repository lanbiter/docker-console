from flask import Flask
from flask import render_template
from flask_sockets import Sockets
import docker
import time
import configure 
from thread_send import threadSend


app = Flask(__name__)
sockets = Sockets(app)
docker_client = docker.Client(base_url=configure.DOCKER_HOST,
         version=configure.DOCKER_API_VERSION,timeout=configure.TIME_OUT)


@app.route('/')
def hello_world():
    return render_template('index.html')

def create_exec():
   command = ["/bin/sh","-c",'TERM=xterm-256color; export TERM; [ -x /bin/bash ] && ([ -x /usr/bin/script ] && /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) || exec /bin/sh']
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
    sock.settimeout(600)
    send = threadSend(ws,sock)
    send.start()
    while not ws.closed:
        message = ws.receive()
        if message is not None:
            sock.send(message)

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

