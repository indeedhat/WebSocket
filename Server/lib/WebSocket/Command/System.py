__author__ = '4423'
from lib.Log import Log
import time

class System:

    @staticmethod
    def test(client, args):
        """Test command"""
        Log.add("THE COMMAND WAS CALLED!!! WOOOOO", Log.NOTICE)
        Log.add(args, Log.NOTICE)

    @staticmethod
    def login(client, args):
        """Perform login"""
        if client._ready_state == "authenticating" and args['name']:
            client._client_name = args['name']
            client._ready_state = "open"

            sys_message = {
                "usr": "__system__",
                "msg": "User \"%s\" has entered the room" % client._client_name,
                "tme": int(time.time())
            }
            client.send_json_object(sys_message)