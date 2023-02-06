import os
import json
import datetime
from discord import Intents, Client, message

token = "MTA3MjE0MTk2MjU0NDY5MzI1OA.GkqYf0.mBT5mQ-wP0gggIPGdWCn9yFJJS6LUYV9sQBrS4"

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

w_data = dict()

def office_in(message, ID):
    if not ("in_flag" in w_data):
        w_data[ID] = {"in_flag": True}
        today = datetime.datetime.now()
        hour, minute = today.hour, today.minute
        add_in_count(ID)
        set_in_time(ID, today)
        update_json()
        read_json()

        if (minute < 10):
            return (f"<@{message.author.id}> {hour}:0{minute} in")
        else:
            return (f"<@{message.author.id}> {hour}:{minute} in")
    else:
        return ("多重inを検知しました!")

def add_in_count(ID):
        if (ID in w_data):
            w_data[ID]["in_count"] += 1
        else:
            w_data[ID]["in_count"] = 1

def set_in_time(ID, today):
    t1 = int(datetime.datetime.timestamp(today))
    w_data[ID]["in_time"] = t1


def office_out(message, ID):
    if ("in_flag" in w_data[ID]):
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

        
def update_json():
    with open('sample.json', mode='w') as f:
        json.dump(w_data, f, indent=4)
        print('WRITE:')
        print(w_data)

def read_json():
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

    if (message.content == "!in"):
        await message.channel.send(office_in(message, message.author.id))

    if (message.content == "!out"):
        await message.channel.send(office_out(message, message.author.id))

client.run(token)
