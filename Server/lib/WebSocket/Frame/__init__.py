__author__ = '4423'

OPCODE_CONTINUATION = 0x0
OPCODE_TEXT = 0x1
OPCODE_BINARY = 0x2
OPCODE_CLOSE = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xa

class Frame:

    fin = 0
    rsv1 = 0
    rsv2 = 0
    rsv3 = 0
    mask = 0
    mask_key = 0
    opcode = 0
    length = 0
    payload = 0