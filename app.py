import discord
import tensorflow as tf
import numpy as np
import os
import datetime
import json
import bruh
import random

from tensorflow import keras
from discord.ext import commands

from discord.ext.commands import Bot

# Features:
#   1. randomly send greeting messages
#   2. predict grade
#   3. logs
#   4. spam
#   5. SuS
#   6. say something
#
#
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# intents = discord.Intents.default()
# intents.message_content = True
intents = discord.Intents.all()
client = Bot(command_prefix="", intents=intents)
mensaje = None
logflag = True
spamhalt = False
SERVER_NAME = ""
MYSERVER = "Turrnut Republic(拖鞋社)"


def pathify(path):
    return path.replace('|', os.sep)


with open(pathify("models|grades|possibilites.json"), "r") as fobj:
    possibilities = json.load(fobj)


def log(msg,):
    try:
        global mensaje
        if logflag:
            SERVER_NAME = str(mensaje.guild.name)
            if bool(os.path.exists(pathify(f"log|{SERVER_NAME}|log.log"))) == False:
                bruh.bruh(pathify(f"log|{SERVER_NAME}|log.log"), "\n", pathify(
                    f"log|{SERVER_NAME}"))

            with open(pathify(f"log|{SERVER_NAME}|log.log"), "a") as fobj:
                fobj.write(msg)
                fobj.write(" | ")
                fobj.write(str(datetime.datetime.now()))
                fobj.write("\n")
    except AttributeError as e:
        return
    except UnicodeEncodeError as e:
        return
    except UnicodeDecodeError as e:
        return


def plog(msg, ):
    SERVER_NAME = str(mensaje.author)
    if bool(os.path.exists(pathify(f"json|dm|{SERVER_NAME}|log.log"))) == False:
        bruh.bruh(pathify(f"json|dm|{SERVER_NAME}|log.log"), "\n", pathify(
            f"json|dm|{SERVER_NAME}"))

    with open(pathify(f"json|dm|{SERVER_NAME}|log.log"), "a") as fobj:
        fobj.write(msg)
        fobj.write(" | ")
        fobj.write(str(datetime.datetime.now()))
        fobj.write("\n")


def validMessage(mes):
    return str(mes.author) in ("turrnut#9727", "Nickels#8378", "a-fork-in-soup#2611", "Nickels#3069", "Comte de Monte Cristo#4077")


async def cant(mes):
    await mes.channel.send("You don't have proper permissions!")


async def dostuff(instructions, message):
    global myid
    global possibilities
    global spamhalt
    global logflag
    instruction = []
    for i in instructions:
        instruction.append(i)
    print(instruction)
    if len(instruction) > 2:
        if instruction[1].lower() == "get":
            await message.channel.send(str(instruction[2]).replace("<", "").replace(">", "").replace("@", ""))
        if instruction[1].lower() in ("send", "send_delete"):
            if validMessage(message):
                m = ""
                i = 3
                while i < len(instruction):
                    m += instruction[i]
                    m += ' '
                    i += 1
                info = {
                    "message": str(m),
                    "userid": int(instruction[2])
                }
                themsg = info["message"]
                plog(f"the bot says to {str(message.author)} -> {themsg}")
                if instruction[1].lower() == "send_delete":
                    await message.delete()

                await client.get_user(info["userid"]).send(themsg)
            else:
                await message.channel.send("YOU DONT HAVE PROPER PERMISSIONS!!!")

        if instruction[1].lower() in ("say", "say_delete"):
            say_delete = False
            if instruction[1].lower() == "say_delete":
                say_delete = True
            say = ''
            i = 2
            while i < len(instruction):
                say += instruction[i]
                say += ' '
                i += 1
            if validMessage(message):
                # LOG
                log(str(message.author) + "let the bot to say \'" + say + "\'")
                await message.channel.send(say)
                if say_delete:
                    await message.delete()
            else:
                # LOG
                log(str(message.author) + "tries to use let the bot to say \'" +
                    say + "\' but has no proper permission")

                await cant(message)

    if len(instruction) == 6:
        if instruction[1].lower() == "grade" and instruction[2].lower() == "predict":
            await message.channel.send('ok, processing...')
            try:
                first = float(instruction[3])
                second = float(instruction[4])
                third = float(instruction[5])
                model = keras.models.load_model(pathify("models|grades"))
                if first > 100 or first < 0 or second > 100 or second < 0 or third > 100 or third < 0:

                    await message.channel.send("Please make sure all the numbers are between 0 and 100!")
                    return
                else:
                    predictions = model.predict(np.asarray([
                        [first, second, third]
                    ]))
                # LOG
                log(str(message.author) + " predict the grade as " +
                    str(first) + " " + str(second) + " " + str(third))
                if first == second == third:
                    await message.channel.send("The turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(first) + "%")
                    await message.channel.send("100.0% Confidence")
                else:
                    await message.channel.send("The turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(round(possibilities[np.argmax(predictions[0])], 2)) + "%")
                    await message.channel.send(str(round(predictions[0][np.argmax(predictions[0])] * 100, 2)) + "% Confidence")
            except ValueError as e:
                print(e)
                await message.channel.send('one of the parameters is not a number!')
                return
    if len(instruction) == 2:
        if instruction[1].lower() == "help":
            # LOG
            log(str(message.author) + " Used the help command")
            await message.channel.send("Hello, I am Turrnut Bot, a bot created by turrnut. I am currently serving ** " + str(len(client.guilds)) + " servers!** My pronouns are *it/its*")
            await message.channel.send("Visit our website for details of the bot: https://turrnut.github.io/discordbot")
            print("servers the bot is in: ", end="")
            for server in client.guilds:
                print(server, ",", end="")
            print("\b  ")
    if len(instruction) >= 3:
        if instruction[1] in ("spam", "spam_delete"):
            delete = False
            if instruction[1] == "spam_delete":
                delete = True
            if validMessage(message):
                if instruction[2] == "halt":
                    # LOG
                    log(str(message.author) + " halted the spam")
                    spamhalt = True
                else:
                    if not spamhalt:
                        count = int(instruction[2])
                        # LOG
                        spammessage = ""
                        j = 3
                        while j < len(instruction):
                            spammessage += str(instruction[j])
                            spammessage += ' '
                            j += 1
                        log(str(message.author) +
                            " used the spam command, count=" + str(count))
                        if delete:
                            await message.delete()
                        i = 0
                        while i < count and not spamhalt and spammessage != "":
                            k = str(i+1)
                            await message.channel.send(f"{spammessage} ( { k } )")
                            i += 1
                    else:
                        spamhalt = False
                        return
            else:
                # LOG
                log(str(message.author) +
                    " tries to use spam command but has no proper permission, count=" + str(instruction[2]))
                await cant(message)

        elif instruction[1] == "log":
            if validMessage(message):
                if instruction[2] == "enable":
                    # LOG
                    logflag = True
                    log(str(message.author) + " Enabled Logging")
                    await message.channel.send("Logging enabled")
                if instruction[2] == "disable":
                    log(str(message.author) + " Disabled Logging")
                    # LOG
                    logflag = False
                    await message.channel.send("Logging disabled")
                if instruction[2] == "check":
                    # LOG
                    log(str(message.author) + " Check logged, it is" + str(logflag))
                    if logflag:
                        await message.channel.send("Logging is currently enabled.")
                    else:
                        await message.channel.send("Logging is currently disabled.")

            else:
                # LOG
                log(str(message.author) +
                    "tries to use use log but has no proper permission")

                await cant(message)


@client.command(pass_context=True)
async def getguild(ctx):
    return ctx.message.guild.id


@client.event
async def on_ready():
    # await tree.sync(guild=discord.Object(id=977378215360335952))
    print(f'We have logged in as {client.user}')
    print(f"servers the bot is in ( {len(client.guilds) } ): ", end="")
    for server in client.guilds:
        print(server, ",", end=" ")
    print("\b  ")


@client.command()
async def test(ctx):
    await ctx.send('test')


@client.event
async def on_member_join(member):
    global SERVER_NAME
    global MYSERVER
    if True:
        print('new member!')
        await member.send('!!!!!!!!!!!!!!!!!\nHello! Welcome to the Offical Turrnut Republic Discord Server! In this server you can chat, socialize and play games with other people.\nTo customize your experience at our server, please pick your pronoun roles and ping roles in the #roles channel\nAlso, it\'s good to read the #server-rules channel because it contains useful information about what to do and not to do in our server\n\nGoodbye, have fun!')
        await member.send('https://tenor.com/view/morgan-freeman-gif-24496452')


@client.event
async def on_message(message):
    global mensaje
    mensaje = message
    # print(message.guild.id)
    if message.author == client.user:
        return
    print(message.author,
          f"( { str(message.author.id) } ) : ", message.content, sep="", end="")
    if mensaje.guild == None:
        plog(f"{str(mensaje.author)} says -> {str(mensaje.content)}")
        print(" {DIRECT MESSAGE}")
    else:
        print()
    if message:

        randomnumber = random.Random().choice(seq=range(100))
        if randomnumber < 5:
            # LOG
            log(str(message.author) + " got greeted by the random greeting system")
            at = "<@" + str(message.author.id) + ">"
            await message.channel.send(random.Random().choice(seq=("Heyyy," + at + " . Whats Up?", "Hello, " + at, at + " hi, how are you?", f"yo {at}")))

    authorinfo = {"username": str(message.author),
                  "userid": int(message.author.id)}
    theusername = authorinfo["username"]
    if bool(os.path.exists(pathify(f"json|userinfo|{theusername}.json"))) == False:
        bruh.bruh(pathify(f"json|userinfo|{theusername}.json"), "\n")

    with open(pathify(f"json|userinfo|{theusername}.json"), "w") as fobj:
        json.dump(authorinfo, fobj, indent=6)
    if message.content.lower() == 'what is my userid':
        await message.channel.send(str(message.author.id))
    if message.content.lower() in ('amogus', 'sus', 'sussy baka'):
        log(str(message.author) + " is sus. Ewww. ")
        await message.channel.send(random.Random().choice(seq=('sus', 'AMOGUS', 'dun dun dun dun', 'yo sussy baka')))

    instructions = message.content.split(' ')
    i = 0
    for instruction in instructions:
        if not instruction.strip(' ').strip('\t').strip('\r').strip('\n'):
            instructions.pop(i)
        i += 1
    if len(instructions) > 0 and instructions[0].lower() == 'turrnut':
        await dostuff(instructions, message)
token = ""
with open("token.token") as t:
    token = t.read()

if token != None:
    client.run(token)
