import discord
from utils.store_ids import store_ids


async def create_default_roles(guild):
    role_configs = {
        "Noble": {"color": discord.Color(int("800080", 16))},
        "Knight": {"color": discord.Color(int("00008b", 16))},
        "Esquire": {"color": discord.Color(int("add8e6", 16))},
        "Peasant": {"color": discord.Color(int("582e05", 16))}
    }

    role_ids = {}

    for role_name, config in role_configs.items():
        role = await guild.create_role(name=role_name, color=config["color"])
        role_ids[role_name] = role.id
        print(f"Created role: {role.name} (ID: {role.id})")

    print("Role IDs created in the following order:")
    for role_name, role_id in role_ids.items():
        print(f"{role_name}: {role_id}")

    store_ids(role_ids=role_ids.values())

    base_role_id = role_ids["Peasant"]
    return role_ids, base_role_id
