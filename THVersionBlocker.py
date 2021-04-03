"""
THVersionBlocker (v2)

Description:
    Created for server 'The Hallway', this script
    kicks players who have been detected as using
    OpenSpades 0.0.12b, which lacks horizontal
    recoil for SMGs.

License: MIT License
Author: lokka30
More information: More information: https://github.com/lokka30/TheHallwayScripts
"""

def apply_script(protocol, connection, config):

    class VersionBlockerConnection(connection):
        def on_login(self, name):
            full = self.client_string
            
            if full is None or full == "":
                return self, name
            
            for players in self.protocol.players.values():
                players.send_chat(name + " joined with client '" + full + "'.")
            
            split = full.split(" ")
            client = split[0]
            version = split[1].substring(0)
            
            if client == "OpenSpades" and version == "0.0.12b":
                reactor.callLater(0.5, self.kick, "OpenSpades 0.0.12b is prohibited on this server.", False)
            
            return self, name

    return protocol, VersionBlockerConnection
