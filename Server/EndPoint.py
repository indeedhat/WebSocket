__author__ = '4423'

import asyncore
from lib.WebSocket.Server import WebSocketServer
from lib.WebSocket.Handler import Handler
from lib.Log import Log

Log.enable_log(True)
WebSocketServer(4423, Handler)
asyncore.loop(timeout=5)