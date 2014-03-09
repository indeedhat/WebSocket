__author__ = '4423'

from lib.WebSocket.Room import Room


class Handler:
    """Send Manager For WebSockets"""

    @staticmethod
    def send_to_singe(client_session, message_frame):
        """Send a message to a single client

        Parameters
        ----------
        client_session : lib.WebSocket.Client.Client
        message_frame : String
        """
        client_session.send_bytes(message_frame)

    @staticmethod
    def send_to_room(room_id, message_frame):
        """Send a message to every member of a room

        Parameters
        ----------
        room_id : String
        message_frame : String
        """
        clients = Room.get_room_clients(room_id)

        for client in clients:
            client.send_bytes(message_frame)