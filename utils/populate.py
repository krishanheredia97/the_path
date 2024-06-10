import importlib
import os
from utils.message_sender import send_default_messages
from utils.lurker_overwrites import get_lurker_overwrites
from utils.store_ids import store_ids
from utils.server_mapping import save_server_mapping
from tusk.buttons.create_quest import initialize_create_quest_channel
from arminio.arminio_bot import bot1

async def populate(ctx, guild, language, role_ids, bot):
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f'discord_messages/{language}')
    category_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    created_categories = []

    for category_dir in category_dirs:
        # Import the configuration module dynamically based on the language and category
        config_module = importlib.import_module(f'discord_messages.{language}.{category_dir}.config')

        channels = config_module.CHANNELS

        if category_dir == "no_category":
            # Create channels without a category
            created_channels = []
            for channel_config in channels:
                channel_name = channel_config["name"]
                channel_overwrites_type = channel_config["overwrite"]
                base_role = channel_config.get("base_role", "Peasant")  # Default to "Peasant" if not specified

                # Get the overwrite function for each channel
                if channel_overwrites_type == "lurker":
                    channel_overwrites = get_lurker_overwrites(guild, role_ids, base_role)

                # Create the channel with the specified overwrites
                channel = await guild.create_text_channel(channel_name, overwrites=channel_overwrites)
                # Add the channel ID and object to the configuration
                channel_config["id"] = channel.id
                channel_config["channel_obj"] = channel
                created_channels.append(channel_config)

            # Store the IDs of the created channels
            channel_ids = [channel["id"] for channel in created_channels]
            store_ids(channel_ids=channel_ids)

            # Send default messages to the channels
            await send_default_messages(guild, "Main Dashboard", created_channels, language)

            await ctx.send(f"Channels created in the main dashboard with specified permissions.")
        else:
            category_name = config_module.CATEGORY_NAME
            category_overwrites_type = config_module.CATEGORY_OVERWRITES

            # Get the overwrite function based on the type
            if category_overwrites_type == "lurker":
                category_overwrites = get_lurker_overwrites(guild, role_ids, "Peasant")  # Default to "Peasant" for category

            # Create the category with the specified overwrites
            category = await guild.create_category(category_name, overwrites=category_overwrites)

            created_channels = []
            for channel_config in channels:
                channel_name = channel_config["name"]
                channel_overwrites_type = channel_config["overwrite"]
                base_role = channel_config.get("base_role", "Peasant")  # Default to "Peasant" if not specified

                # Get the overwrite function for each channel
                if channel_overwrites_type == "lurker":
                    channel_overwrites = get_lurker_overwrites(guild, role_ids, base_role)

                # Create the channel with the specified overwrites
                channel = await guild.create_text_channel(channel_name, category=category, overwrites=channel_overwrites)
                # Add the channel ID and object to the configuration
                channel_config["id"] = channel.id
                channel_config["channel_obj"] = channel
                created_channels.append(channel_config)

            # Store the IDs of the created channels
            channel_ids = [category.id] + [channel["id"] for channel in created_channels]
            store_ids(channel_ids=channel_ids)

            # Collect category and channels info for the server mapping
            created_categories.append({
                "name": category_name,
                "id": category.id,
                "channels": created_channels
            })

            # Send default messages to the channels
            await send_default_messages(guild, category_name, created_channels, language)

            await ctx.send(f"Category '{category.name}' and channels created with specified permissions.")

    # Save the server mapping to Firebase
    await save_server_mapping(guild, role_ids, created_categories)

    import asyncio
    await asyncio.sleep(0.1)

    server_id = guild.id
    await initialize_create_quest_channel(bot, server_id)
    await bot1(ctx, bot, server_id)
