__author__ = '4423'


class Room:
    """Session management class for socket server"""

    _rooms = {}

    @staticmethod
    def add_to_room(room_id, client):
        """Add a new client to the given room

        Parameters
        ----------
        room_id : string
        client : lib.WebSocket.Client.Client
        """
        if not room_id in Room._rooms:
            Room._rooms[room_id] = []

        if Room._rooms[room_id].count(client) == 0:
            Room._rooms[room_id].append(client)

    @staticmethod
    def remove_from_room(room_id, client):
        """Remove a client from the given room

        Parameters
        ----------
        room_id : string
        client : lib.WebSocket.Client.Client
        """
        if room_id in Room._rooms and Room._rooms[room_id].count(client) > 0:
            Room._rooms[room_id].remove(client)

    @staticmethod
    def get_room_clients(room_id):
        """Return all the clients in a room

        Returns
        -------
        List
        """
        if room_id in Room._rooms:
            return Room._rooms[room_id]

        return []