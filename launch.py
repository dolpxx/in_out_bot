import os
import json
import datetime
from discord import Intents, Client

token = "MTA3MjE0MTk2MjU0NDY5MzI1OA.GkqYf0.mBT5mQ-wP0gggIPGdWCn9yFJJS6LUYV9sQBrS4"

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


client = Client(intents=intents)

member_data = dict()


def initialize(ID):
    member_data[ID] = dict()


def office_in(message, ID):
    is_in = (
        not ("in_flag" in member_data[ID]) or
            (member_data[ID]["in_flag"] == False)
    )

    if (is_in):
        member_data[ID]["in_flag"] = True
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        add_in_count(ID)
        set_in_time(ID, today)
        update_json()

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} in")
        else:
            return (f"<@{message.author.id}> {hour}:{minute} in")
    else:
        return ("**多重inを検知しました!**")


def add_in_role(message):
    guild_id = 824630338692317244
    guild = client.get_guild(guild_id)
    role = guild.get_role(1040160934959783946)
    return (message.author.add_roles(role))


def add_in_count(ID):
    if ("in_count" in member_data[ID]):
        member_data[ID]["in_count"] += 1
    else:
        member_data[ID]["in_count"] = 1


def set_in_time(ID, today):
    t1 = int(datetime.datetime.timestamp(today))
    member_data[ID]["in_time"] = t1


def update_json():
    with open('sample.json', mode='w') as f:
        json.dump(member_data, f, indent=4)
        print('updated:')
        print(member_data)


def read_json():
    with open('sample.json', mode='r') as f:
        r_data = json.load(f)
        print('read:')
        print(r_data)


def office_out(message, ID):
    is_out = (
        ("in_flag" in member_data[ID]) and
        (member_data[ID]["in_flag"] == True)
    )

    if (is_out):
        member_data[ID]["in_flag"] = False
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        add_stay_time(ID, today)
        update_json()

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} out")
        else:
            return (f"<@{message.author.id}> {hour}:{minute} out")
    else:
        return ("**まだinしていません!**")


def remove_in_role(message):
    guild_id = 824630338692317244
    guild = client.get_guild(guild_id)
    role = guild.get_role(1040160934959783946)
    return (message.author.remove_roles(role))


def add_stay_time(ID, today):
    t2 = int(datetime.datetime.timestamp(today))
    subtraction = t2 - member_data[ID]["in_time"]
    if ("stay_time" in member_data[ID]):
        member_data[ID]["stay_time"] += subtraction
    else:
        member_data[ID]["stay_time"] = subtraction


def func_members():
    for guild in client.guilds:
        for member in guild.members:
            yield member


def enum(ID):
    update_json()
    temporary = []
    result = ""
    for member in func_members():
        ID = member.id
        if ("stay_time" in member_data[ID]):
            temporary.append(([ID, member_data[ID]["stay_time"]]))
        else:
            continue

    if (temporary == []):
        return ("**表示するデータがありません!**")
    else:
        temporary = sorted(temporary, reverse=True, key=lambda x: x[1])
        for i in range(len(temporary)):
            info = temporary[i]
            member_ID = info[0]
            day, hour, minute, second = 0, 0, 0, 0
            if (info[1] > 86400 > 0):
                day = info[1] // 86400
            if (info[1] > 3600):
                hour = info[1] // 3600
            if (info[1] > 60):
                minute = info[1] // 60
            if (info[1] > 0):
                second = info[1] % 60
            result += (
                f'**<@{member_ID}>**: **総in時間**: {day} 日 {hour} 時間 {minute} 分 {second} 秒, {i+1}位\n'
            )
        return (result)


@client.event
async def on_ready():
    print(f"Darkey が起動しました")
    for member in func_members():
        initialize(member.id)
    update_json()


@client.event
async def on_member_join(member):
    initialize(member.id)


@client.event
async def on_message(message):
    is_bot_channel = (message.channel.name == "bot動作確認")
    if (is_bot_channel):
        if (message.author == client.user):
            return

        if (message.content == "in"):
            await message.channel.send(office_in(message, message.author.id))
            await add_in_role(message)

        if (message.content == "out"):
            await message.channel.send(office_out(message, message.author.id))
            await remove_in_role(message)

        if (message.content == "enum"):
            await message.channel.send(enum(message.author.id))
    else:
        return

client.run(token)
