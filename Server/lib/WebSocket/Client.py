__author__ = '4423'

import asyncore
import json
import time
from mimetools import Message
from base64 import b64encode
from hashlib import sha1
from StringIO import StringIO
from lib.Log import Log
from lib.WebSocket.Room import Room
from lib.WebSocket.Handler import Handler as RoomManager
from lib.WebSocket.Frame.Parser import Parser
from lib.WebSocket.Frame.Builder import Builder


class Client(asyncore.dispatcher_with_send):
    """Web Socket Client connection"""

    SALT = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    _addr = ()
    _server = None
    _room_id = ""
    _client_name = ""

    _ready_state = "connecting"
    _buffer = ""

    def __init__(self, connection, address, server):
        """Setup Client Object

        Parameters
        ----------
        connection : map
        address : string
        server : lib.WebSocket.Server.Server
        """
        # run parent object
        asyncore.dispatcher_with_send.__init__(self, connection)

        # assign vars
        self._addr = address
        self._server = server

    def client_ready(self):
        """Check if the client is ready to receive messages

        Returns
        -------
        Boolean
        """
        Log.add(self._ready_state == "open", Log.NOTICE)
        return self._ready_state == "open"

    def handle_read(self):
        """Handle incoming data"""
        if self._ready_state == "connecting":
            self._perform_handshake()

        elif self._ready_state == "authenticating":
            frame = Parser.parse(self.socket)
            self._perform_login(frame)

        elif self._ready_state == "open":
            frame = Parser.parse(self.socket)
            Log.add("Decoded Message: %s" % frame.payload)
            self._handle_frame(frame)

    def _handle_frame(self, frame):
        """Direct incoming frames to the appropriate handler

        Parameters
        ----------
        frame : lib.WebSocket.Frame.Frame
        """
        if frame.opcode == 0x0:
            Log.add("We do not yet support continuation frames", Log.NOTICE)
        elif frame.opcode == 0x1:
            self._handle_message(frame)
        elif frame.opcode == 0x2:
            Log.add("We do not yet support binary frames", Log.NOTICE)
        elif frame.opcode == 0x3:
            Log.add("This will be used when i write the client from scratch (login)", Log.NOTICE)
        elif frame.opcode == 0x4:
            Log.add("This will be used when i write the client from scratch (cmd)", Log.NOTICE)
        elif frame.opcode == 0x8:
            self.handle_close()
        elif frame.opcode == 0x9:
            Log.add("pong needs to be added soon", Log.NOTICE)
        else:
            Log.add("unsupported opcode %d" % frame.opcode, Log.NOTICE)

    def _handle_message(self, frame):
        """Handle incoming text frame

        Parameters
        ----------
        frame : lib.WebSocket.Frame.Frame
        """
        json_obj = json.loads(str(frame.payload.strip()))

        if "cmd" in json_obj:
            pass
        elif "msg" in json_obj:
            self.send(json_obj['msg'])
        else:
            Log.add(json_obj, Log.NOTICE)

    def _perform_handshake(self):
        """Perform The WebSocket Handshake"""
        try:
            Log.add("Got To Handshake")
            data = self.recv(1024).strip()
            # Log.add("Data: %s" % data)
            headers = Message(StringIO(data.split('\r\n', 1)[1]))

            Log.add("Parsed Headers:")
            # Log.add(headers)

            if headers.get('Upgrade', None) == 'websocket':
                Log.add("Attempting Handshake")

                # create response key
                key = b64encode(sha1(headers['Sec-WebSocket-Key'] + self.SALT).digest())

                # create response headers
                response = (
                    "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
                    "Upgrade: websocket\r\n"
                    "Connection: Upgrade\r\n"
                    "Sec-WebSocket-Origin: %s\r\n"
                    "Sec-WebSocket-Accept: %s\r\n\r\n" % (headers["Origin"], key)
                )
                if self.send_bytes(response):
                    Log.add("Handshake successful")
                    self._assign_room(data)
                    self._ready_state = "authenticating"

        except Exception as e:
            Log.add(e.args)

    def _perform_login(self, frame):
        """Perform login attempt

        Parameters
        ----------
        frame : lib.WebSocket.Frame.Frame
        """
        try:
            if frame.opcode == 0x1 and frame.length > 0:
                json_obj = json.loads(frame.payload)
                Log.add(json_obj)
                if json_obj['cmd'] == "login" and len(json_obj['name']):
                    self._client_name = json_obj['name']
                    self._ready_state = "open"

                    sys_message = {
                        "usr": "__system__",
                        "msg": "User \"%s\" has entered the room" % self._client_name,
                        "tme": int(time.time())
                    }
                    Log.add(sys_message)
                    RoomManager.send_to_room(self._room_id, Builder.build(json.dumps(sys_message)))
        except Exception as e:
            Log.add(e.args)

    def _assign_room(self, headers):
        """Assign the client to the room they are trying to join

        Parameters
        ----------
        headers : String
        """
        # split room_id from the headers
        room_id = headers.split('\r\n')[0].split(' ')[1].strip()

        Log.add("Room ID: %s" % room_id)

        # assign self to room
        self._room_id = room_id
        Room.add_to_room(room_id, self)

    def send(self, data):
        """Send a message to the room at large

        Parameters
        ----------
        data : String
        """
        if self._ready_state == "open":
            Log.add(data)
            obj = json.dumps({
                "msg": data,
                "usr": self._client_name,
                "tme": int(time.time())
            })

            RoomManager.send_to_room(self._room_id, Builder.build(obj))

    def send_bytes(self, data):
        """Send raw data back to the client

        Parameters
        ----------
        data : string

        Returns
        -------
        Boolean
        """
        try:
            Log.add(data, Log.NOTICE)
            asyncore.dispatcher_with_send.send(self, data)
            self._buffer = ""
            return True
        except:
            Log.add("Error sending bytes with dispatcher")

        return False

    def handle_close(self):
        """Cleanup a closed connection"""
        Log.add("got to close")
        sys_message = {
            "usr": "__system__",
            "msg": "User \"%s\" has left the room" % self._client_name,
            "tme": int(time.time())
        }
        Log.add(sys_message)
        RoomManager.send_to_room(self._room_id, Builder.build(json.dumps(sys_message)))
        Room.remove_from_room(self._room_id, self)
        self.close()
