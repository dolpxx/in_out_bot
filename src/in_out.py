import os
import json
import datetime
from dotenv import load_dotenv
from discord import Intents, Client

load_dotenv()

token = os.environ["BOT_TOKEN"]
print(token)

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


client = Client(intents=intents)

member_data = dict()


def initialize(ID):
    today = datetime.datetime.now()
    member_data[ID] = dict()
    member_data[ID]["in_flag"] = False
    member_data[ID]["in_count"] = 0
    member_data[ID]["in_time"] = int(datetime.datetime.timestamp(today))
    member_data[ID]["stay_time"] = 0


def office_in(message, ID):
    if (member_data[ID]["in_flag"] == False):
        can_in = True
    if (member_data[ID]["in_flag"] == True):
        can_in = False

    if (can_in):
        member_data[ID]["in_flag"] = True
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        hour = (hour + 9) % 24
        add_in_count(ID)
        set_in_time(ID, today)
        update_json()
        read_json()

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} in")
        if (minute >= 10):
            return (f"<@{message.author.id}> {hour}:{minute} in")
    return ("**多重inを検知しました:(**")


def add_in_role(message):
    guild_id = 824630338692317244
    guild = client.get_guild(guild_id)
    role = guild.get_role(1040160934959783946)
    return (message.author.add_roles(role))


def add_in_count(ID):
    member_data[ID]["in_count"] += 1


def set_in_time(ID, today):
    t1 = int(datetime.datetime.timestamp(today))
    member_data[ID]["in_time"] = t1


def update_json():
    with open("src/sample.json", 'w') as f:
        json.dump(member_data, f, indent=4)
        print('updated:')


def read_json():
    with open("src/sample.json", 'r') as f:
        read_data = json.load(f)
        print('read:')
        print(read_data)


def office_out(message, ID):
    if (member_data[ID]["in_flag"] == True):
        can_out = True
    if (member_data[ID]["in_flag"] == False):
        can_out = False

    if (can_out):
        member_data[ID]["in_flag"] = False
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        hour = (hour + 9) % 24
        add_stay_time(ID, today)
        update_json()
        read_json()

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} out")
        if (minute >= 10):
            return (f"<@{message.author.id}> {hour}:{minute} out")
    return ("**多重outを検知しました!**")


def remove_in_role(message):
    guild_id = 824630338692317244
    guild = client.get_guild(guild_id)
    role = guild.get_role(1040160934959783946)
    return (message.author.remove_roles(role))


def add_stay_time(ID, today):
    t2 = int(datetime.datetime.timestamp(today))
    subtraction = t2 - member_data[ID]["in_time"]
    member_data[ID]["stay_time"] += subtraction


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
        if (member_data[ID]["stay_time"] is not 0):
            temporary.append(([ID, member_data[ID]["stay_time"]]))

    if (temporary == []):
        return ("**表示するデータがありません!**")

    temporary = sorted(temporary, reverse=True, key=lambda x: x[1])
    member_count = len(temporary)
    for i in range(member_count):
        info = temporary[i]
        member_ID = info[0]
        day, hour, minute, second = 0, 0, 0, 0
        if (info[1] > 86400):
            day = info[1] // 86400
        if (info[1] > 3600):
            hour = (info[1] % 86400) // 3600
        if (info[1] > 60):
            minute = (info[1] % 3600) // 60
        if (info[1] >= 0):
            second = info[1] % 60
        result += (
            f'**<@{member_ID}> 総in時間**: {day} 日 {hour} 時間 {minute} 分 {second} 秒, **{i+1}位**\n'
        )
    return (result)


def get_my_data(ID):
    ret = (f"<@{ID}>: {member_data[ID]}")
    print(ret)
    return (ret)


@client.event
async def on_ready():
    print(f"Darkey が起動しました")
    for member in func_members():
        initialize(member.id)
    update_json()
    read_json()


@client.event
async def on_member_join(member):
    initialize(member.id)


@client.event
async def on_message(message):
    is_bot_channel = (message.channel.name == "bot動作確認")
    # or (message.channel.name == "対面活動報告"))
    if (is_bot_channel):
        inlike_words = {"in", "いn", "un", "on", "im",
                        "いｎ", "ｉｎ", "いん", "イン"}

        outlike_words = {"out", "put", "iut", "おうt",
                         "おうｔ", "our", "ｏｕｔ", "あうと", "アウト"}
        if (message.author == client.user):
            return

        if (message.content.lower() in inlike_words):
            await message.channel.send(office_in(message, message.author.id))
            await add_in_role(message)

        if (message.content.lower() in outlike_words):
            await message.channel.send(office_out(message, message.author.id))
            await remove_in_role(message)

        if (message.content.lower() == "enum"):
            await message.channel.send(enum(message.author.id))

        if (message.content.lower() == "get_my_data"):
            await message.channel.send(get_my_data(message.author.id))

        if (message.content.lower() == "update_data"):
            await update_json(member_data)

        if (message.content.lower() == "read_data"):
            await read_json(member_data)

client.run(token)
