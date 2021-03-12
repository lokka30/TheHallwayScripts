# TheHallway's Scripts
* These are Python scripts created for [piqueserver](https://github.com/lokka30/THProxyDetector/issues), an Ace of Spades 'classic' server implementation.
* These scripts are created by and run on [The Hallway](https://discord.gg/ButndsdGua), a CTF server with the original 'hallway' map by izzy.
* Fellow server owners are free to install these scripts and adapt them as they wish, since all are licensed under the [MIT License](https://github.com/lokka30/TheHallwayScripts/blob/main/LICENSE).

# Script Descriptions

***

## THKickBadNames.py
### About:
* This script kicks players that have usernames beginning with the `#` character, since they make it difficult to use the `/votekick` command for regular users.

### Requirements:
* This script is designed to run on [piqueserver](https://github.com/piqueserver/piqueserver) although should work on PySnip and PySpades.

***

## THProxyDetector.py
### About:
* This is designed to kick players that join with a VPN or proxy.

### Requirements:
* [piqueserver](https://github.com/piqueserver/piqueserver)
* This script should work on most operating systems - ideally use a Linux distro like Ubuntu.
* **Requests**: `pip install requests` - this is installed on most systems anyways

### Warning:
* This script was designed for [piqueserver](https://github.com/piqueserver/piqueserver), it is unlikely to run on PySnip or PySpades. (you should upgrade to piqueserver anyways)

### Contributors:
Thank you very much to the following contributors for improving the script:
* `sByte`

# Support:
- Please create an issue on the [issue tracker](https://github.com/lokka30/THProxyDetector/issues).
