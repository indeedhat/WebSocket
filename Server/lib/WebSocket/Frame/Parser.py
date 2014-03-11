__author__ = '4423'

from lib.WebSocket.Frame import Frame
from struct import unpack

class Parser:

    _working = False
    _socket = None
    _frame = None

    _continue_frame = False
    _buffer = 0

    @staticmethod
    def parse(socket):
        sel = Parser(socket)
        return sel.get_frame()

    def __init__(self, socket):
        self._working = True
        self._frame = Frame()
        self._socket = socket

        self._parse()

    def get_frame(self):
        while self._working:
            pass

        return self._frame

    def _parse(self):
        self._first_byte()
        self._length_bytes()

        if self._frame.opcode <= 0x7:
            self._mask_bytes()
            self._payload_bytes()

        if self._frame.fin == 0x0:
            self._continue_frame = True
            self._payload_bytes()
        else:
            self._working = False

    def _first_byte(self):
        self._buffer = ord(self._socket.recv(1))

        self._frame.fin = (self._buffer >> 7) & 1
        self._frame.rsv1 = (self._buffer >> 6) & 1
        self._frame.rsv2 = (self._buffer >> 5) & 1
        self._frame.rsv3 = (self._buffer >> 4) & 1
        self._frame.opcode = self._buffer & 0xf

    def _length_bytes(self):
        self._buffer = ord(self._socket.recv(1))

        self._frame.mask = (self._buffer >> 7) & 1
        self._frame.length = self._buffer & 0x7f

        if self._frame.length <= 125:
            pass
        elif self._frame.length == 126:
            new_length = self._socket.recv(2)
            self._frame.length = unpack('!Q', new_length)[0]
        elif self._frame.length == 127:
            new_length = self._socket.recv(8)
            self._frame.length = unpack('!H', new_length)[0]

    def _mask_bytes(self):
        self._frame.mask_key = self._socket.recv(4)

    def _payload_bytes(self):
        if self._continue_frame:
            self._frame.payload += self._socket.recv(self._frame.length)
        else:
            self._frame.payload = self._socket.recv(self._frame.length)