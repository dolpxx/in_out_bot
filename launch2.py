import os
import json
import datetime
from discord import Intents, Client, message

token = "MTA3MjE0MTk2MjU0NDY5MzI1OA.GkqYf0.mBT5mQ-wP0gggIPGdWCn9yFJJS6LUYV9sQBrS4"

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

class Command:
    def __init__(self):
        self.is_bot_channel = (message.channel.name == "bot動作確認")

    def enum_members(message):
        for guild in client.guilds:
            for member in guild.members:
                return (f"{member}")

    def office_in(message):
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        write(message.author.id)
        read()
        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} in")
        else:
            return (f"<@{message.author.id}> {hour}:{minute} in")

w_data = dict()
def write(ID):
    with open('sample.json', mode='w') as f:
        if (ID in w_data):
            w_data[ID] += 1
        else:
            w_data[ID] = 1

        json.dump(w_data, f, indent=4)
        print('WRITE:')
        print(w_data)

def read():
    with open('sample.json', mode='r') as f:
        r_data = json.load(f)
        print('READ')
        print(r_data)

@client.event
async def on_ready():
    print(f"Darkey が起動しました")

@client.event
async def on_message(message):

    if (message.author == client.user):
        return
        
    if (message.content == "!member"):
        await message.channel.send(Command.enum_members(message))

    if (message.content == "!in"):
        await message.channel.send(Command.office_in(message))


client.run(token)
