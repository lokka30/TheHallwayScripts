'''
THKickBadNames
Version: Build 3
License: MIT License
Author: lokka30
More information: https://github.com/lokka30/TheHallwayScripts
'''
from twisted.internet import reactor

def apply_script(protocol, connection, config):
    class HashtagConnection(connection):
        def on_login(self, name):
            if self.name.startswith('#'):
                reactor.callLater(0.5, self.kick, "Usernames may not start with the 'hashtag' character since they bypass votekicks.", False)
            return connection.on_login(self, name)
    return protocol, HashtagConnection
