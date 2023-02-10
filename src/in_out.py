import os
import json
import datetime
from dotenv import load_dotenv
from discord import Intents, Client

load_dotenv()

token = os.environ["BOT_TOKEN"]
guild_id = int(os.environ["GUILD_ID"])
role_id = int(os.environ["IN_ROLE_ID"])
bot_channel_id = int(os.environ["BOT_CHANNEL_ID"])
attendance_channel_id = int(os.environ["ATTENDANCE_CHANNEL_ID"])

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = Client(intents=intents)

member_data = dict()


def initialize_data(ID):
    member_data[ID] = dict()
    member_data[ID]["in_flag"] = False
    member_data[ID]["in_count"] = 0
    member_data[ID]["in_time"] = 0
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
        update_json("src/sample.json")

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} in")
        if (minute >= 10):
            return (f"<@{message.author.id}> {hour}:{minute} in")
    return ("**多重inを検知しました!**")


def add_in_role(message):
    guild = client.get_guild(guild_id)
    role = guild.get_role(role_id)
    return (message.author.add_roles(role))


def add_in_count(ID):
    member_data[ID]["in_count"] += 1


def set_in_time(ID, today):
    t1 = int(datetime.datetime.timestamp(today))
    member_data[ID]["in_time"] = t1


def update_json(path):
    with open(path, 'w') as f:
        json.dump(member_data, f, indent=4)
        print("updated:", path, datetime.datetime.utcnow() +
            datetime.timedelta(hours=9))
    return ("データを更新しました.")


def read_json(path):
    with open(path, 'r') as f:
        read_data = json.load(f)
        print("read:")
    return (read_data)


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
        update_json("src/sample.json")

        if (minute < 10):
            ret = (f"<@{message.author.id}> {hour}:0{minute} out")
        if (minute >= 10):
            ret = (f"<@{message.author.id}> {hour}:{minute} out")
        return (ret)
    return ("**多重outを検知しました!**")


def remove_in_role(message):
    guild = client.get_guild(guild_id)
    role = guild.get_role(role_id)
    return (message.author.remove_roles(role))


def add_stay_time(ID, today):
    t2 = int(datetime.datetime.timestamp(today))
    subtraction = t2 - member_data[ID]["in_time"]
    member_data[ID]["stay_time"] += subtraction


def func_members():
    for guild in client.guilds:
        for member in guild.members:
            yield (member)


def second_to_time(sec):
    result = []
    day, hour, minute, second = 0, 0, 0, 0
    if (sec > 86400):
        day = sec // 86400
    if (sec > 3600):
        hour = (sec % 86400) // 3600
    if (sec > 60):
        minute = (sec % 3600) // 60
    if (sec >= 0):
        second = sec % 60

    result.append(day)
    result.append(hour)
    result.append(minute)
    result.append(second)

    return (result)


def enum(ID):
    update_json("src/sample.json")
    temporary = []
    result = []
    for member in func_members():
        ID = member.id
        if not (member_data[ID]["stay_time"] == 0):
            temporary.append(([ID, member_data[ID]["stay_time"]]))

    if (temporary == []):
        return ("**表示するデータがありません!**")

    temporary = sorted(temporary, reverse=True, key=lambda x: x[1])
    member_count = len(temporary)
    for i in range(member_count):
        info = temporary[i]
        member_ID = info[0]
        time = second_to_time(info[1])

        day, hour, minute, second = time
        result.append(
            f"**<@{member_ID}> 総in時間**: **{day}** 日 **{hour}** 時間 **{minute}** 分 **{second}** 秒, **{i+1} 位**\n"
        )
        result = "".join(result)
    return (result)


def get_my_data(ID):
    ret = (f"<@{ID}> {member_data[ID]}")
    print(ret)
    return (ret)


@client.event
async def on_ready():
    print(f"Darkey が起動しました")
    for member in func_members():
        initialize_data(member.id)
    update_json("src/sample.json")


@client.event
async def on_member_join(member):
    initialize_data(member.id)


@client.event
async def on_message(message):

    is_bot_channel = (message.channel.id == bot_channel_id)
    is_attendance_channel = (message.channel.id == attendance_channel_id)
    inlike_words = {"in", "いn", "un", "on", "im", "inn",
                    "いｎ", "ｉｎ", "いん", "イン", "ｲﾝ", "ｉｎｎ"}
    outlike_words = {"out", "put", "iut", "おうt", "auto", "ａｕｔｏ",
                     "おうｔ", "our", "ｏｕｔ", "あうと", "アウト", "ｱｳﾄ"}
    enumlike_words = {"enum", "ｅｎｕｍ", "えぬm", "えぬｍ"}

    if (is_bot_channel):

        if (message.author.bot):
            return

        if (message.content.lower() in inlike_words):
            await message.channel.send(office_in(message, message.author.id))
            await add_in_role(message)

        if (message.content.lower() in outlike_words):
            await message.channel.send(office_out(message, message.author.id))
            await remove_in_role(message)

        if (message.content.lower() in enumlike_words):
            await message.channel.send(enum(message.author.id))

        if (message.content.lower() == "get_my_data"):
            await message.channel.send(get_my_data(message.author.id))

        if (message.content.lower() == "update_data"):
            if (message.channel.id == bot_channel_id):
                await message.channel.send(update_json("src/sample.json"))

client.run(token)
