import discord

BOT_ROLE = 1248715938627325993


def get_lurker_overwrites(guild, role_ids, base_role):
    role_hierarchy = ["Peasant", "Esquire", "Knight", "Noble"]
    base_role_index = role_hierarchy.index(base_role)

    # Filter roles that are above or equal to the base_role
    valid_roles = {role_name: role_id for role_name, role_id in role_ids.items() if role_hierarchy.index(role_name) >= base_role_index}

    # Create a dictionary to store overwrites
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.get_role(BOT_ROLE): discord.PermissionOverwrite(
            view_channel=True,
            manage_channels=True,
            read_message_history=True,
            send_messages=True
        )
    }

    # Iterate through each valid role_id in the role_ids dictionary
    for role_id in valid_roles.values():
        overwrites[guild.get_role(role_id)] = discord.PermissionOverwrite(
            view_channel=True,
            read_message_history=True,
            send_messages=False
        )

    return overwrites
