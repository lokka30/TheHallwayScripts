"""
THProxyDetector 
Version: Build 6
License: MIT License
Author: lokka30
More information: https://github.com/lokka30/TheHallwayScripts
"""
import json
import requests
import asyncio
from requests.exceptions import Timeout
from twisted.internet import reactor

# Set a key to "disabled" to disable it.
PROXYCHECK_IO_KEY = str("disabled") #https://proxycheck.io/ - this API requires a key (Free).
VPNAPI_IO_KEY = str("disabled") #https://vpnapi.io/ - this API requires a key (Free).
IP_TEOH_IO_KEY = str("enabled") #https://ip.teoh.io/vpn-proxy-api - NOTE: this API does not utilise keys. This is only here so you can disable it if you want.

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


def apply_script(protocol, connection, config):
    class PDConnection(connection):  
    
        """
        When users log in, this will check their IP address.
        """
        def on_login(self, username):
            asyncio.run(Detectors.check_player(self, username))
            return connection.on_login(self, username)
    
    class Detectors:
        """
        Runs proxy detection functions on player.
        """
        @classmethod
        async def check_player(self, username):
            detectedByProxyCheckIo = Detectors.check_proxycheck_io(self.address[0], username)
            detectedByVpnApiIo = Detectors.check_vpnapi_io(self.address[0], username)
            detectedByIpTeohIo = Detectors.check_ip_teoh_io(self.address[0], username)
            
            await detectedByProxyCheckIo
            await detectedByVpnApiIo
            await detectedByIpTeohIo
            
            if(detectedByProxyCheckIo or detectedByVpnApiIo or detectedByIpTeohIo):
                reactor.callLater(0.5, self.kick, "VPNs and proxies are prohibited on this server.", False)
            else:
                print("THProxyDetector:  [Info] '%s' does not seem to be using a proxy." % username)
    
        """
        Use proxycheck.io to check if the address is a VPN or proxy.
        Returns True if it is a VPN or proxy.
        """
        @classmethod
        def check_proxycheck_io(self, address, username):
            if(PROXYCHECK_IO_KEY == "disabled"):
                return False
            
            response = None
            try:     
                PROXYCHECK_IO_URL = str("https://proxycheck.io/v2/" + address + "?key=" + PROXYCHECK_IO_KEY)
                response = requests.get(url=(PROXYCHECK_IO_URL), verify=False, timeout=2, headers=HEADERS)
            except Timeout:
                print("THProxyDetector:  [Error: proxycheck.io] Request timed out.")
                return False
            
            if(response):
                result = response.json()[address]
                isProxy = (result["proxy"] == "yes") or (result["type"] == "VPN")
                if isProxy:
                    print("THProxyDetector:  [Warning: proxycheck.io] Address of <name=" + username + ">, <ip=" + address + ">, was detected as a proxy.")
                return isProxy
            else:
                print("THProxyDetector:  [Error: proxycheck.io] Unable to detect proxy status of address '%s', error code: '%s'" % self.address, response.status_code)
                return False
                
        """
        Use vpnapi.io to check if the address is a VPN or proxy.
        Returns True if it is a VPN or proxy.
        """
        @classmethod
        def check_vpnapi_io(self, address, username): 
            if(VPNAPI_IO_KEY == "disabled"):
                return False
        
            response = None
            try:
                response = requests.get(url="https://vpnapi.io/api/" + address + "?key=" + VPNAPI_IO_KEY, verify=False, timeout=2, headers=HEADERS)
            except Timeout:
                print("THProxyDetector:  [Error: vpnapi.io] Request timed out.")
                return False
            
            if(response):
                result = response.json()["security"]
                isProxy = result["vpn"] == "True" or result["proxy"] == "True"
                
                if isProxy:
                    print("THProxyDetector:  [Warning: vpnapi.io] Address of <name=" + username + ">, <ip=" + address + ">, was detected as a proxy.")
                return isProxy
            else:
                print("THProxyDetector:  [Error: vpnapi.io] Unable to detect proxy status of address '%s', error code: '%s'" % self.address, response.status_code)
                return False
                
        """
        Use ip.teoh.io to check if the address is a VPN or proxy.
        Returns True if it is a VPN or proxy.
        """
        @classmethod
        def check_ip_teoh_io(self, address, username):
            if(IP_TEOH_IO_KEY == "disabled"):
                return False
        
            response = None
            try:
                response = requests.get(url="https://ip.teoh.io/api/vpn/" + address, verify=False, timeout=2, headers=HEADERS)
            except Timeout:
                print("THProxyDetector:  [Error: ip.teoh.io] Request timed out.")
                return False
            
            if(response):
                isProxy = response.json()["vpn_or_proxy"] == "yes"
                if isProxy:
                    print("THProxyDetector:  [Warning: ip.teoh.io] Address of <name=" + username + ">, <ip=" + address + ">, was detected as a proxy.")
                return isProxy
            else:
                print("THProxyDetector:  [Error: ip.teoh.io] Unable to detect proxy status of address '%s', error code: '%s'" % self.address, response.status_code)
                return False
    
    return protocol, PDConnection
