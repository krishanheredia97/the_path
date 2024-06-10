import os
from utils.lurker_overwrites import get_lurker_overwrites

BOT_ROLE = 1248715938627325993


async def create_getting_started(ctx, guild, store_ids, base_role_id):
    bot_role = guild.get_role(BOT_ROLE)
    base_role = guild.get_role(base_role_id)
    if bot_role is None or base_role is None:
        await ctx.send(f"One or both roles not found.")
        return

    overwrites = get_lurker_overwrites(guild, base_role_id)

    category = await guild.create_category("GETTING STARTED", overwrites=overwrites)

    channel_1 = await guild.create_text_channel("📈│level-system", category=category, overwrites=overwrites)
    channel_2 = await guild.create_text_channel("🏅│roles", category=category, overwrites=overwrites)
    channel_3 = await guild.create_text_channel("🌟│tips", category=category, overwrites=overwrites)

    channel_ids = [category.id, channel_1.id, channel_2.id, channel_3.id]
    store_ids(channel_ids=channel_ids)
    print(f'created: {channel_ids}')

    messages_dir = os.path.dirname(os.path.abspath(__file__))
    for channel in [channel_1, channel_2, channel_3]:
        channel_name = channel.name.split("│")[1].lower()
        message_file = os.path.join(messages_dir, f"{channel_name}.txt")
        if os.path.exists(message_file):
            with open(message_file, "r", encoding="utf-8") as file:
                message_content = file.read()
            await channel.send(message_content)

    await ctx.send(f"Category '{category.name}' and channels created with specified permissions.")
