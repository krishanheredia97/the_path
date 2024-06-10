import discord


async def delete_channels(guild, *channel_ids):
    deleted_channels = []
    for channel_id_str in channel_ids:
        try:
            # Convert channel ID from string to integer
            channel_id = int(channel_id_str)
            # Retrieve the channel object using the channel ID
            channel = guild.get_channel(channel_id)
            if channel:
                # Delete the channel and append its ID to the deleted list
                await channel.delete()
                deleted_channels.append(str(channel_id))
                print(f"Deleted channel: {channel.name} ({channel.id})")
            else:
                # Print a message if the channel ID does not exist
                print(f"Channel with ID {channel_id} not found in this server.")
        except ValueError:
            # Handle the case where the provided channel ID is not a valid integer
            print(f"Invalid channel ID: {channel_id_str}")
        except discord.HTTPException as e:
            # Handle any exceptions that occur during the deletion process
            print(f"Error deleting channel with ID {channel_id_str}: {e}")

    return deleted_channels
