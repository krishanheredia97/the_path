import discord
from discord.ui import Button, View


class AddRewardButton(Button):
    def __init__(self):
        super().__init__(label="Add Reward", style=discord.ButtonStyle.green, custom_id="dummy_add_reward")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction silently


class RedeemRewardButton(Button):
    def __init__(self):
        super().__init__(label="Redeem Reward", style=discord.ButtonStyle.danger, custom_id="dummy_redeem_reward")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction silently


class MyRewardsButton(Button):
    def __init__(self):
        super().__init__(label="My Rewards", style=discord.ButtonStyle.secondary, custom_id="dummy_my_rewards")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction silently


async def instructions(channel):
    # Message 1
    message_content_1 = """
# What are Rewards?

Rewards are incentives you give to yourself for maintaining good habits. For example, you might reward yourself with 
an ice cream every week you spend without smoking. When you add a reward, you need to give it a name and assign a 
value in GP (the server's currency), which you earn by abstaining from vices.

## Steps to Administer Your Rewards

### Step 1
Determine how much GP your reward will cost (check <#1242954833569382452> for picking a reward category or 
<#1242958133769404466> for calculating a custom reward cost).

### Step 2
Go to the channel <#1238187584434339956> for administering rewards.
"""
    await channel.send(message_content_1)

    # Message 2 with Add Reward button
    message_content_2 = """
### Step 3
Use this button to add a new reward.
"""
    view_1 = View()
    view_1.add_item(AddRewardButton())
    await channel.send(message_content_2, view=view_1)

    # Message 3 with Redeem Reward button
    message_content_3 = """
### Step 4
Use this button to redeem a reward using your earned GP.
"""
    view_2 = View()
    view_2.add_item(RedeemRewardButton())
    await channel.send(message_content_3, view=view_2)

    # Message 4 with My Rewards button
    message_content_4 = """
### My Rewards
Use this button to view your available GP and rewards.
"""
    view_3 = View()
    view_3.add_item(MyRewardsButton())
    await channel.send(message_content_4, view=view_3)