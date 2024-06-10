import discord


async def delete_all_roles(guild, keep_role_id):
    keep_role = guild.get_role(keep_role_id)
    if keep_role is None:
        raise ValueError(f"The role with ID {keep_role_id} does not exist in this server.")

    deleted_roles = []
    for role in guild.roles:
        if role != keep_role and role != guild.default_role:
            try:
                await role.delete()
                deleted_roles.append(role.name)
            except discord.HTTPException as e:
                print(f"Error deleting role {role.name}: {e}")

    return deleted_roles


async def delete_roles(guild, *role_ids):
    deleted_roles = []
    for role_id in role_ids:
        role = guild.get_role(int(role_id))
        if role is None:
            print(f"Role with ID {role_id} not found in this server.")
            continue

        if role == guild.default_role:
            print(f"Cannot delete the @everyone role.")
            continue

        try:
            await role.delete()
            deleted_roles.append(role.name)
        except discord.HTTPException as e:
            print(f"Error deleting role {role.name}: {e}")


    return deleted_roles