import os
import datetime
from discord import message
import discord

token = "MTA3MjE0MTk2MjU0NDY5MzI1OA.GkqYf0.mBT5mQ-wP0gggIPGdWCn9yFJJS6LUYV9sQBrS4"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

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
        return

    if (message.content == "!in"):
        await message.channel.send(office_in(message))

    if (message.content == "!role"):
        guild_id = 824630338692317244
        guild = client.get_guild(guild_id)
        role = guild.get_role(1040160934959783946)
        await message.author.add_roles(role)
        
    if (message.content == "!unrole"):
        guild_id = 824630338692317244
        guild = client.get_guild(guild_id)
        role = guild.get_role(1040160934959783946)
        await message.author.remove_roles(role)
client.run(token)
