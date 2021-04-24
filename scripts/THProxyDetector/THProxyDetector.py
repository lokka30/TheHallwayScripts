"""
THProxyDetector 
Version: Build 17
License: MIT License
Author: lokka30
More information: https://github.com/lokka30/TheHallwayScripts
"""
import asyncio
import aiohttp
from twisted.internet import defer, reactor
from twisted.internet.defer import ensureDeferred, Deferred
from piqueserver.utils._async import as_deferred

"""
######################
# USER CONFIGURATION #
######################
"""

"""
Section 1
-> Detection Services
"""

# https://proxycheck.io/ --- a free proxy detection service
# Should the 'proxycheck.io' proxy detector be used?
PROXYCHECK_IO_ENABLED = False
PROXYCHECK_IO_API_KEY = "put key here (required)."

# https://vpnapi.io/ --- a free proxy detection service
# Should the 'vpnapi.io' proxy detector be used?
VPNAPI_IO_ENABLED = False
VPNAPI_IO_KEY = "put key here (required)."

# https://ip.teoh.io/vpn-proxy-api --- a free, key-less proxy detection service
IP_TEOH_IO_ENABLED = False

"""
Section 2
-> Messages
"""

# The reason supplied when a user is kicked for VPN/proxy detection.
KICK_REASON = "VPNs & proxies are prohibited on this server."

"""
Section 3
-> Other
"""

# Should the kick not be broadcasted to everyone? True / False.
KICK_SILENT = False

# Should debug messages be printed to the console?
PRINT_DEBUG_LOGGING = False

"""
##########################
# END USER CONFIGURATION #
##########################
"""

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


# noinspection PyUnusedLocal
def apply_script(protocol, connection, config):
    class PDProtocol(protocol):
        cached_approved_addresses = ["127.0.0.1"]
        cached_denied_addresses = []

    class PDConnection(connection):

        """
        When users log in, this will check their IP address.
        """

        def on_login(self, username):
            if PRINT_DEBUG_LOGGING:
                print("THProxyDetector: " + username + " joined, checking services...")

            if self.address[0] in self.protocol.cached_approved_addresses:
                print("THProxyDetector: " + username + " has a cached address (approved)")
                return

            if self.address[0] in self.protocol.cached_denied_addresses:
                print("THProxyDetector: " + username + " has a cached address (denied)")
                Detectors.kick_player(self)
                return

            if PROXYCHECK_IO_ENABLED:
                if PRINT_DEBUG_LOGGING:
                    print("THProxyDetector: PROXYCHECK_IO enabled, checking " + username + "...")
                ensureDeferred(as_deferred(Detectors.check_player(self, self.address[0], username, "PROXYCHECK_IO")))

            if VPNAPI_IO_ENABLED:
                if PRINT_DEBUG_LOGGING:
                    print("THProxyDetector: VPNAPI_IO enabled, checking " + username + "...")
                ensureDeferred(as_deferred(Detectors.check_player(self, self.address[0], username, "VPNAPI_IO")))

            if IP_TEOH_IO_ENABLED:
                if PRINT_DEBUG_LOGGING:
                    print("THProxyDetector: IP_TEOH_IO enabled, checking " + username + "...")
                ensureDeferred(as_deferred(Detectors.check_player(self, self.address[0], username, "IP_TEOH_IO")))

            return connection.on_login(self, username)

    class Detectors:
        """
        Runs proxy detection functions on player.
        """

        # noinspection PyMethodParameters
        @classmethod
        async def check_player(self, connection, address, username, service) -> None:
            async with aiohttp.ClientSession() as session:

                """
                proxycheck.io
                """
                if service == "PROXYCHECK_IO":
                    if PRINT_DEBUG_LOGGING:
                        print("THProxyDetector: Service " + service + " is checking " + username + "...")
                    url = str("https://proxycheck.io/v2/" + address + "?key=" + PROXYCHECK_IO_API_KEY)
                    async with session.get(url=url, allow_redirects=False, timeout=2, headers=HEADERS) as response:
                        response_json = await response.json(content_type=None)
                        if response_json is not None:
                            if response_json[address]["proxy"] == "yes" or response_json[address]["type"] == "VPN":
                                Detectors.kick_player(connection)
                                print(
                                    "THProxyDetector: Warning for " + service + ": " + username + " was detected for using a VPN or proxy!")
                                return
                            else:
                                print(
                                    "THProxyDetector: Info for " + service + ": " + username + " was NOT detected for using a VPN or proxy.")
                                connection.protocol.cached_approved_addresses.append(address)
                        else:
                            print("THProxyDetector: Error for " + service + ": invalid JSON.")

                """
                vpnapi.io
                """
                if service == "VPNAPI_IO":
                    if PRINT_DEBUG_LOGGING:
                        print("THProxyDetector: Service " + service + " is checking " + username + "...")
                    url = str("https://vpnapi.io/api/" + address + "?key=" + VPNAPI_IO_KEY)
                    async with session.get(url, allow_redirects=False, timeout=2, headers=HEADERS) as response:
                        response_json = await response.json(content_type=None)
                        if response_json is not None:
                            if response_json["security"]["vpn"] == "True" or response_json["security"]["proxy"] == "True":
                                Detectors.kick_player(connection)
                                print(
                                    "THProxyDetector: Warning for " + service + ": " + username + " was detected for using a VPN or proxy!")
                                return
                            else:
                                print(
                                    "THProxyDetector: Info for " + service + ": " + username + " was NOT detected for using a VPN or proxy.")
                                connection.protocol.cached_approved_addresses.append(address)
                        else:
                            print("THProxyDetector: Error for " + service + ": invalid JSON.")

                """
                ip.teoh.io
                """
                if service == "IP_TEOH_IO":
                    if PRINT_DEBUG_LOGGING:
                        print("THProxyDetector: Service " + service + " is checking " + username + "...")
                    url = str("https://ip.teoh.io/api/vpn/" + address)
                    async with session.get(url, allow_redirects=False, timeout=2, headers=HEADERS) as response:
                        response_json = await response.json(content_type=None)
                        if response_json is not None:
                            if response_json["vpn_or_proxy"] == "yes":
                                Detectors.kick_player(connection)
                                print(
                                    "THProxyDetector: Warning for " + service + ": " + username + " was detected for using a VPN or proxy!")
                                return
                            else:
                                print(
                                    "THProxyDetector: Info for " + service + ": " + username + " was NOT detected for using a VPN or proxy.")
                                connection.protocol.cached_approved_addresses.append(address)
                        else:
                            print("THProxyDetector: Error for " + service + ": invalid JSON.")

        @classmethod
        def kick_player(self, connection) -> None:
            if connection.address[0] not in connection.protocol.cached_denied_addresses:
                connection.protocol.cached_denied_addresses.append(connection.address[0])

            if connection.address[0] in connection.protocol.cached_approved_addresses:
                connection.protocol.cached_approved_addresses.remove(connection.address[0])

            reactor.callLater(0.5, connection.kick, KICK_REASON, KICK_SILENT)

    return PDProtocol, PDConnection
