import os
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

    # def enum_members(message):
    #     for guild in client.guilds:
    #         for member in guild.members:
    #             yield (f"{member}")

    def office_in(message):
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        return (f"<@{message.author.id}> {hour}:{minute} in")

@client.event
async def on_ready():
    print(f"We have logged in as dekai voice")


@client.event
async def on_message(message):

    if (message.author == client.user):
        print("0")
        return

    if (message.content == "!member"):
        print("1")
        await message.channel.send(Command.enum_members(message))

    if (message.content == "in"):
        print("2")
        await message.channel.send(Command.office_in(message))

client.run(token)
