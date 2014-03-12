__author__ = 'PHPMatt'

from lib.WebSocket.Frame import Frame
import struct


class Builder:
    """WebSocket Frame Builder

    This class is overkill at the moment but is ready for expansion
    """

    _frame = None
    _buffer = ''

    @staticmethod
    def build(payload):
        """Build a frame for the given payload

        Parameters
        ----------
        payload : string

        Returns
        -------
        String
        """
        s = Builder(payload)
        return s._return()

    def __init__(self, payload):
        """Setup the builder environment

        Parameters
        ----------
        payload : String
        """
        self._frame = Frame()

        self._frame.payload = payload

    def _first_byte(self):
        """Set the first byte of the frame"""
        self._buffer = 0x81

    def _length_byte(self):
        """Set the length byte(s) of the frame"""
        self._frame.length = len(self._frame.payload)

        if self._frame.length < 126:
            self._buffer += struct.pack("B", self._frame.length)
        elif self._frame.length <= 0xFFFF:
            self._buffer += struct.pack("!BH", 126, self._frame.length)
        else:
            self._buffer += struct.pack("!BQ", 127, self._frame.length)

    def _payload(self):
        """Add the payload data to the frame"""
        self._buffer += self._frame.payload

    def _return(self):
        """return the completed frame

        Returns
        -------
        String
        """
        return self._buffer