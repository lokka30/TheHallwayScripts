"""
THPlayerList
Version: Build 2
License: MIT License
Author: lokka30
More information: https://github.com/lokka30/TheHallwayScripts
"""
from piqueserver.commands import command


@command("list")
def list_players(connection):
    admins = []
    moderators = []
    guards = []
    trusted = []
    members = []

    can_see_staff = 'guard' in connection.user_types or 'moderator' in connection.user_types or connection.admin

    for player in list(connection.protocol.players.values()):
        label = "(#%s) %s" % (str(player.player_id), player.name)

        if can_see_staff:
            if player.invisible:
                label += " (INV)"

            if player.admin:
                admins.append(label)
                continue

            elif 'moderator' in player.user_types:
                moderators.append(label)
                continue

            elif 'guard' in player.user_types:
                guards.append(label)
                continue

        if player.invisible:
            continue

        if 'trusted' in player.user_types:
            trusted.append(label)
            continue

        members.append(label)

    connection.send_chat("---+ Online Players (%s) +---" % str(
        len(admins) + len(moderators) + len(guards) + len(trusted) + len(members)))
    send_list(connection, "Admins", admins)
    send_list(connection, "Moderators", moderators)
    send_list(connection, "Guards", guards)
    send_list(connection, "Trusted", trusted)
    send_list(connection, "Members", members)


def send_list(connection, list_name, labels):
    if len(labels) != 0:
        connection.send_chat("%s (%s):" % (list_name, str(len(labels))))
        for label in labels:
            connection.send_chat(label)


# noinspection PyUnusedLocal
def apply_script(protocol, connection, config):
    return protocol, connection
