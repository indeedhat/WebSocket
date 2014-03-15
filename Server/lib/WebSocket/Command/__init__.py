__author__ = '4423'

from lib.WebSocket.Command.System import System

rregistry = {
    'System' : System
}

def run_command(class_name, method_name, client, args):
    """Run a command"""
    getattr(rregistry[class_name], method_name)(client, args)