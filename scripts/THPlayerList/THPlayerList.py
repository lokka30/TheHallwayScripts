"""
THPlayerList
Version: Build 1
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
    members = connection.protocol.players

    can_see_staff = connection.user_type == 'guard' or connection.user_type == 'moderator' or connection.user_type == 'admin'

    for player in connection.protocol.players:
        if player.user_type == 'trusted':
            trusted += player
            members.remove(player)
        if can_see_staff:
            if player.user_type == 'guard':
                guards += player
                members.remove(player)
            elif player.user_type == 'moderator':
                moderators += player
                members.remove(player)
            elif player.user_type == 'admin':
                admins += player
                members.remove(player)
        else:
            if player.invisible:
                members.remove(player)

    connection.send_chat("---+ Online Players +---")
    send_list(connection, can_see_staff, "Admins", admins)
    send_list(connection, can_see_staff, "Moderators", moderators)
    send_list(connection, can_see_staff, "Guards", guards)
    send_list(connection, can_see_staff, "Trusted", trusted)
    send_list(connection, can_see_staff, "Members", members)


def send_list(connection, can_see_staff, list_name, players):
    if players is not None:
        connection.send_chat("%list_name% (%list_len%):".format(list_name, len(players)))
        for player in players:
            invisible = ""
            if player.invisible and can_see_staff:
                invisible = " (INV)"

            connection.send_chat("(#%player_id%) %player_name% %is_invisible%".format(player.player_id, player.name, invisible))


# noinspection PyUnusedLocal
def apply_script(protocol, connection, config):
    return protocol, connection
