from flask import Flask
from flask_socketio import SocketIO

import logging

from flask_socketio import emit, send, ConnectionRefusedError
from flask import request, session


application: Flask = Flask(__name__, instance_relative_config=True)

socketio = SocketIO(application, logger=True, engineio_logger=True)
socketio.init_app(application, cors_allowed_origins="*")

socket_connections = {}


@socketio.on("connect")
def on_connect():
    token = request.args.get('token')
    if token is None:
        logging.info("Canceled connection without a token.")
        raise ConnectionRefusedError("JWT access token required in query parameters.")

    # Mocked use auth for testing purposes
    if token != "TOKEN":
        logging.info("User tried to connect with expired token.")
        return False
        raise ConnectionRefusedError("JWT access token has expired.")

    user_id = 1

    socket_connections[user_id] = request.sid
    session["user_id"] = user_id
    session["sid"] = request.sid

    logging.info(f"SocketIO Auth success for user {user_id}.")
    send(f"Connection for user {user_id} is successful.")
    emit("ack", "Connection successfully received.")


@socketio.on("disconnect")
def on_disconnect():
    if 'user_id' in session:
        logging.info(f"User {session['user_id']} disconnected.")
        del socket_connections[session["user_id"]]


@socketio.on("message")
def handle_message(data):
    logging.info(f"Got message {data} with session {session} and request {request}.")
    logging.warning(socket_connections)


@socketio.on_error()
def error_handler(e):
    logging.warning(e)


@socketio.on_error_default
def default_error_handler(e):
    logging.warning(request.event["message"])
    logging.warning(request.event["args"])
    logging.warning(e)


if __name__ == "__main__":
    socketio.run(application, debug=True, port=5000, allow_unsafe_werkzeug=True)
