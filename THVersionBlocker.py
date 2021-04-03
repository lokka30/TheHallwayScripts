"""
THVersionBlocker (v3)

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
            client = self.client_string
            
            if client is None or client == "":
                return self, name
            
            print(name + " joined with client '" + client + "'.")
            for players in self.protocol.players.values():
                players.send_chat(name + " joined with client '" + client + "'.")
            
            if client.find("OpenSpades") != -1 and client.find("0.0.12b") != -1:
                reactor.callLater(0.5, self.kick, "OpenSpades 0.0.12b is prohibited on this server.", False)
            
            return self, name

    return protocol, VersionBlockerConnection
