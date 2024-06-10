import os
import importlib


async def send_default_messages(guild, category_name, channels, language):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    category_name_corrected = category_name.replace(" ", "_").lower()

    # Adjust the base directory for messages
    if category_name == "Main Dashboard":
        messages_dir = os.path.join(base_dir, "discord_messages", language, "no_category")
    else:
        messages_dir = os.path.join(base_dir, "discord_messages", language, category_name_corrected)

    for channel_config in channels:
        channel = channel_config["channel_obj"]
        channel_name = channel_config["name"].split("│")[1].lower()
        msg_file_type = channel_config.get("msg_file", "none")

        if msg_file_type == ".txt":
            message_file = os.path.join(messages_dir, f"{channel_name}.txt")
            if os.path.exists(message_file):
                with open(message_file, "r", encoding="utf-8") as file:
                    message_content = file.read()
                await channel.send(message_content)
                print(f"Sent message to channel: {channel.name}")
            else:
                print(f"Message file not found for channel: {channel.name}")

        elif msg_file_type == ".py":
            try:
                module_name = f"{language}.{category_name_corrected}.{channel_name}"
                module = importlib.import_module(f"discord_messages.{module_name}")
                func = getattr(module, channel_name)
                await func(channel)
                print(f"Executed {channel_name} function in {module_name}.py")
            except (ImportError, AttributeError) as e:
                print(f"Error importing or calling function {channel_name} from {module_name}: {e}")

        elif msg_file_type == "none":
            print(f"No message file for channel: {channel.name}")
