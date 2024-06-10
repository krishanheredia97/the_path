import discord
from discord.ui import Button, View




class AddViceButton(Button):
    def __init__(self):
        super().__init__(label="Add Vice", style=discord.ButtonStyle.blurple, custom_id="dummy_add_vice")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction silently


class RelapseButton(Button):
    def __init__(self):
        super().__init__(label="Relapse", style=discord.ButtonStyle.red, custom_id="dummy_relapse")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction silently


class QuitButton(Button):
    def __init__(self):
        super().__init__(label="Quit", style=discord.ButtonStyle.green, custom_id="dummy_quit")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction silently


class MyVicesButton(Button):
    def __init__(self):
        super().__init__(label="My Vices", style=discord.ButtonStyle.gray, custom_id="dummy_my_vices")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction silently


async def instructions(channel):
    message_content_5 = """
    # What are Vices?

    Vices are habits or behaviors that you are trying to quit or manage. Our server focuses on tracking vices instead of "good habits" because it is easier to manage abstinence from bad habits than constant instances of successfully doing good habits. In the future, the server will include functionality for administering good habits as well.

    ## Steps to Manage Your Vices

    ### Step 1
    Go to the channel <#1238187584434339957> for administering vices.
    """
    await channel.send(message_content_5)

    # Message 2 with Add Vice button
    message_content_6 = """
    ### Step 2
    Add a new vice by using the button below.
    """
    view_4 = View()
    view_4.add_item(AddViceButton())
    await channel.send(message_content_6, view=view_4)

    # Message 3 with Relapse button
    message_content_7 = """
    ### Step 3
    Register a relapse as soon as it occurs using the button below.
    """
    view_5 = View()
    view_5.add_item(RelapseButton())
    await channel.send(message_content_7, view=view_5)

    # Message 4 with Quit button
    message_content_8 = """
    ### Step 4
    Quit an existing habit after a relapse using the button below.
    """
    view_6 = View()
    view_6.add_item(QuitButton())
    await channel.send(message_content_8, view=view_6)

    # Message 5 with My Vices button
    message_content_9 = """
    ### My Vices
    Use this button to view your current and past vices.
    """
    view_7 = View()
    view_7.add_item(MyVicesButton())
    await channel.send(message_content_9, view=view_7)
