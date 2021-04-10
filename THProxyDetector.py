"""
THProxyDetector 
Version: Build 14
License: MIT License
Author: lokka30
More information: https://github.com/lokka30/TheHallwayScripts
"""
from twisted.internet import defer, reactor
import asyncio
import json
import aiohttp

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
IP_TEOH_IO_ENABLED = True

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

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


def apply_script(protocol, connection, config):

    class ProxyDetectorConnection(connection):  
    
        """
        When users log in, this will check their IP address.
        """
        def on_login(self, username):
            #Detectors.debug("%s joined." % username) # python thinks we're giving it 2 arguments. lmao
        
            loop = asyncio.get_event_loop()
            if PROXYCHECK_IO_ENABLED:
                #Detectors.debug(username + " - PROXYCHECK_IO enabled, checking player...")
                ensureDeferred(as_deferred(Detectors.check_player(self, username, "PROXYCHECK_IO")))
                
            if VPNAPI_IO_ENABLED:
                #Detectors.debug(username + " - VPNAPI_IO enabled, checking player...")
                ensureDeferred(as_deferred(Detectors.check_player(self, username, "VPNAPI_IO")))
                
            if IP_TEOH_IO_ENABLED:
                #Detectors.debug(username + " - IP_TEOH_IO enabled, checking player...")
                ensureDeferred(as_deferred(Detectors.check_player(self, username, "IP_TEOH_IO")))
                
            return connection.on_login(self, username)
    
    class Detectors:
        """
        Runs proxy detection functions on player.
        """
        @classmethod
        async def check_player(self, username, service) -> None:
            #Detectors.debug(username + " - Checking with service " + service + "...")
       
            async with aiohttp.ClientSession() as session:
                
                """
                proxycheck.io
                """
                if service == "PROXYCHECK_IO":
                    Detectors.log("INFO", service, "Checking status of " + username + "...")
                    url = str("https://proxycheck.io/v2/" + address + "?key=" + PROXYCHECK_IO_API_KEY)
                    async with session.get(url, allow_redirects=False, timeout=2, headers=HEADERS) as response:
                        json = await response.json()
                        if json is not None:
                            if json[address]["proxy"] == "yes" or json[address]["type"] == "VPN":
                                Detectors.kick_player(self, service)
                                Detectors.log("WARNING", service, username + " was detected for using a VPN or proxy.")
                                return
                            else:
                                Detectors.log("INFO", service, username + " was not detected for using a VPN or proxy.")
                        else:
                            Detectors.log("ERROR", service, "Invalid JSON.")
                    
                """
                vpnapi.io
                """    
                if service == "VPNAPI_IO":
                    Detectors.log("INFO", service, "Checking status of " + username + "...")
                    url = str("https://vpnapi.io/api/" + address + "?key=" + VPNAPI_IO_KEY)
                    async with session.get(url, allow_redirects=False, timeout=2, headers=HEADERS) as response:
                        json = await response.json()
                        if json is not None:
                            if json["security"]["vpn"] == "True" or json["security"]["proxy"] == "True":
                                Detectors.kick_player(self, service)
                                Detectors.log("WARNING", service, username + " was detected for using a VPN or proxy.")
                                return
                            else:
                                Detectors.log("INFO", service, username + " was not detected for using a VPN or proxy.")
                        else:
                            Detectors.log("ERROR", service, "Invalid JSON.")
                    
                """
                ip.teoh.io
                """  
                if service == "IP_TEOH_IO":
                    Detectors.log("INFO", service, "Checking status of " + username + "...")
                    url = str("https://ip.teoh.io/api/vpn/" + address)
                    async with session.get(url, allow_redirects=False, timeout=2, headers=HEADERS) as response:
                        json = await response.json()
                        if json is not None:
                            if json["vpn_or_proxy"] == "yes":
                                Detectors.kick_player(self, service)
                                Detectors.log("WARNING", service, username + " was detected for using a VPN or proxy.")
                                return
                            else:
                                Detectors.log("INFO", service, username + " was not detected for using a VPN or proxy.")
                        else:
                            Detectors.log("ERROR", service, "Invalid JSON.")
            
        @classmethod
        def kick_player(self, service) -> None:
            reactor.callLater(0.5, self.kick, KICK_REASON, KICK_SILENT)
        
        @classmethod
        def log(severity, service, message) -> None:
            print("[THProxyDetector] [" + severity + "] [" + service + "]: " + message)
            
        @classmethod
        def debug(message) -> None:
            if(PRINT_DEBUG_LOGGING):
                print("[THProxyDetector] [DEBUG] " + message)
    
    return protocol, ProxyDetectorConnection
