import os
import json
import datetime
from discord import Intents, Client, message

token = "MTA3MjE0MTk2MjU0NDY5MzI1OA.GkqYf0.mBT5mQ-wP0gggIPGdWCn9yFJJS6LUYV9sQBrS4"

intents = Intents.default()
intents.members = True
intents.message_content = True

client = Client(intents=intents)

w_data = dict()


def initialize(ID):
    w_data[ID] = dict()


def office_in(message, ID):
    if not ("in_flag" in w_data[ID]) or (w_data[ID]["in_flag"] == False):
        w_data[ID]["in_flag"] = True
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        add_in_role(message, ID)
        add_in_count(ID)
        set_in_time(ID, today)
        update_json()

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} in")
        else:
            return (f"<@{message.author.id}> {hour}:{minute} in")
    else:
        return ("多重inを検知しました!")


def add_in_count(ID):
    if ("in_count" in w_data[ID]):
        w_data[ID]["in_count"] += 1
    else:
        w_data[ID]["in_count"] = 1


def set_in_time(ID, today):
    t1 = int(datetime.datetime.timestamp(today))
    w_data[ID]["in_time"] = t1


def update_json():
    with open('sample.json', mode='w') as f:
        json.dump(w_data, f, indent=4)
        print('updated:')
        print(w_data)


def read_json():
    with open('sample.json', mode='r') as f:
        r_data = json.load(f)
        print('read:')
        print(r_data)


def office_out(message, ID):
    if ("in_flag" in w_data[ID]) and (w_data[ID]["in_flag"] == True):
        w_data[ID]["in_flag"] = False
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        add_stay_time(ID, today)
        update_json()
        read_json()

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} out")
        else:
            return (f"<@{message.author.id}> {hour}:{minute} out")
    else:
        return ("まだinしていません")


def add_stay_time(ID, today):
    t2 = int(datetime.datetime.timestamp(today))
    if ("stay_time" in w_data[ID]):
        w_data[ID]["stay_time"] += t2 - w_data[ID]["in_time"]
    else:
        w_data[ID]["stay_time"] = t2 - w_data[ID]["in_time"]

def add_in_role(message, ID):
    user = message.guild.get_member(ID)
    ROLE_ID = 1040160934959783946
    role = message.guild.get_role(ROLE_ID)
    user.add_roles(role)


@client.event
async def on_ready():
    def func():
        for guild in client.guilds:
            for member in guild.members:
                yield member
    print(f"Darkey が起動しました")
    for member in func():
        initialize(member.id)
    else:
        update_json()


@client.event
async def on_member_join(member):
    initialize(member.id)


@client.event
async def on_message(message):

    if (message.author == client.user):
        return

    if (message.content == "!in"):
        await message.channel.send(office_in(message, message.author.id))

    if (message.content == "!out"):
        await message.channel.send(office_out(message, message.author.id))

client.run(token)
