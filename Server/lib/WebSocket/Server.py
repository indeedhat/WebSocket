__author__ = '4423'

import asyncore
import socket
from lib.Log import Log
from lib.WebSocket.Handler import Handler
from lib.WebSocket.Client import Client


class WebSocketServer(asyncore.dispatcher):
    """Websocket connection handler"""

    _handler = None
    _port = 4423

    def __init__(self, port=4423, handler=Handler):
        """Create a websocket server

        Parameters
        ----------
        port : int
        handler : Object
        """
        Log.add("Server starting")

        # start parent
        asyncore.dispatcher.__init__(self)

        # assign variables
        self._port = port
        self._handler = handler

        # setup server
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("", port))
        self.listen(1)

    def handle_accept(self):
        """Manage new connections"""
        Log.add("New Connection")

        conn, addr = self.accept()
        Client(conn, addr, self)