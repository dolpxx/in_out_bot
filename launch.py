# This example requires the "message_content" intent.
import datetime
from discord import message
import discord

token = "MTA3MjE0MTk2MjU0NDY5MzI1OA.GkqYf0.mBT5mQ-wP0gggIPGdWCn9yFJJS6LUYV9sQBrS4"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

class Command:
    def __init__(self):
        self.is_bot_channel = (message.channel.name == "bot動作確認")

    async def enum_members(self):
        for guild in client.guilds:
            for member in guild.members:
                await message.channel.send(f"{member}")

    async def office_in(self):
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        await message.channel.send(f"<@{message.author.id}> {hour}:{minute} in")

@client.event
async def on_ready():
    print(f"We have logged in as dekai voice")
    
@client.event
async def on_message(message):
    
    if (message.author == client.user):
        return

    if (message.content == "!member"):
        Command.enum_members()

    if (message.content == "!in"):
        Command.office_in()

client.run(token)