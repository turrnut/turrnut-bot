# Copyright (c) 2025 TURRNUT
# Under the MIT license

import os


def bruh(bro, bro2, bro3=None, bro4="BRO"):
    if bro3 != None:
        os.makedirs(bro3)
    with open(bro, "w") as f:
        f.write(bro2)


async def parselinktomsg(client, link):
    link = link.split('/')
    server_id = int(link[4])
    channel_id = int(link[6])
    msg_id = int(link[5])

    server = client.get_guild(server_id)
    channel = server.get_channel(channel_id)
    message = await channel.fetch_message(msg_id)
    return server, channel, message
    mesg.author.timeout(datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute + 10).astimezone())


async def react(message, emoji):
    await message.add_reaction(emoji)
