import discord
from discord.ui import View
from backend.data_manager import load_data, save_data, load_quest_data, save_quest_data

CATEGORY_ID_TO_DUPLICATE = 1245263224480202883
CHANNELS_TO_DUPLICATE = {
    1245372881014100099: '🟡│task-check-in',
    1245263225751339088: '📜│quest-info',
    1245371676334489610: '🐎│battlefield',
    1245371990731264010: '🔥│bonfire'
}
BOT_ROLE_ID = 1245506986834001992


async def handle_accepted_quest(bot, guild, quest_id):
    # Fetch the bot's member object
    bot_member = guild.get_member(bot.user.id)
    if not bot_member:
        return

    # Check initial permissions
    permissions = bot_member.guild_permissions
    if permissions.manage_channels and permissions.manage_roles:
        try:
            # Create a new role
            new_role = await guild.create_role(name=f'Role for Quest {quest_id}')
            print(f"Created role ID: {new_role.id}")

            # Fetch the category to duplicate
            original_category = guild.get_channel(CATEGORY_ID_TO_DUPLICATE)
            if not original_category or not isinstance(original_category, discord.CategoryChannel):
                return

            # Duplicate the category with its permissions and rename it
            new_category = await guild.create_category(
                name=f'🏰│{quest_id}',
                overwrites=original_category.overwrites
            )

            # Update permissions to allow the new role to view the category and all channels
            await new_category.set_permissions(new_role, view_channel=True, read_message_history=True)

            # List to hold all new channel IDs
            new_channel_ids = [new_category.id]

            # Duplicate each specified channel inside the new category with the new name
            for original_channel_id, new_channel_name in CHANNELS_TO_DUPLICATE.items():
                original_channel = guild.get_channel(original_channel_id)
                if original_channel and isinstance(original_channel, discord.TextChannel):
                    new_channel = await new_category.create_text_channel(
                        name=new_channel_name,
                        overwrites=original_channel.overwrites,
                        topic=original_channel.topic,
                        nsfw=original_channel.nsfw,
                        slowmode_delay=original_channel.slowmode_delay
                    )
                    new_channel_ids.append(new_channel.id)

                    # Set permissions for the new role
                    if original_channel_id == 1245371990731264010:
                        await new_channel.set_permissions(new_role, send_messages=True, read_message_history=True,
                                                          view_channel=True)
                    else:
                        await new_channel.set_permissions(new_role, send_messages=False, read_message_history=True,
                                                          view_channel=True)

                    # Send buttons to the '🟡│task-check-in' channel
                    if new_channel_name == '🟡│task-check-in':
                        await send_task_check_in_buttons(new_channel, quest_id)

            # Print the list of new channel IDs
            print(f"Created category and channel IDs: {new_channel_ids}")

            # Store the created role and channel IDs
            from utils.store_ids import store_ids
            store_ids(role_ids=[new_role.id], channel_ids=new_channel_ids)

        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass


# Function to send task check-in buttons
async def send_task_check_in_buttons(channel, quest_id):
    class TaskCheckInView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.quest_id = quest_id

        @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
        async def yes_button_callback(self, interaction, button):
            await update_user_progress(interaction.user.id, 'yes', self.quest_id)
            await update_quest_progress(self.quest_id, 'yes')
            await interaction.response.send_message("You clicked Yes!", ephemeral=True)

        @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
        async def no_button_callback(self, interaction, button):
            await update_user_progress(interaction.user.id, 'no', self.quest_id)
            await update_quest_progress(self.quest_id, 'no')
            await interaction.response.send_message("You clicked No!", ephemeral=True)

    view = TaskCheckInView()
    await channel.send("Did you complete your task today?", view=view)


async def update_user_progress(user_id, response, quest_id):
    user_data = load_data(user_id)
    if 'User_Quests' not in user_data:
        user_data['User_Quests'] = {
            'individual_quests': {
                'active_quests': {},
                'finished_quests': {}
            },
            'group_quests': {
                'active_quests': {},
                'finished_quests': {}
            }
        }

    quest_data = load_quest_data(quest_id)
    quest_main = quest_data.get('Quest_Main', {})
    if quest_main.get('quest_type') == 'individual':
        quest_category = user_data['User_Quests']['individual_quests']['active_quests']
    else:  # assuming 'group' for group quests
        quest_category = user_data['User_Quests']['group_quests']['active_quests']

    # Update user success and failure counts
    quest_category[quest_id] = quest_category.get(quest_id, {})
    if response == 'yes':
        quest_category[quest_id]['user_success_count'] = quest_category[quest_id].get('user_success_count', 0) + 1
    elif response == 'no':
        quest_category[quest_id]['user_failure_count'] = quest_category[quest_id].get('user_failure_count', 0) + 1

    save_data(user_data)


async def update_quest_progress(quest_id, response):
    quest_data = load_quest_data(quest_id)
    quest_progress = quest_data.get('Quest_Progress', {})

    if response == 'yes':
        quest_progress['quest_users_success_count'] = quest_progress.get('quest_users_success_count', 0) + 1
    elif response == 'no':
        quest_progress['quest_users_failure_count'] = quest_progress.get('quest_users_failure_count', 0) + 1

    quest_data['Quest_Progress'] = quest_progress
    save_quest_data(quest_data)
