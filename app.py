import discord
import numpy as np
import os
import math
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import datetime
import json
import bruh
import random
import nacl
import exint.interpreter as lang

from tensorflow import keras
from discord import app_commands
from discord.ext import commands

from discord.ext.commands import Bot

# Features:
#   1. randomly send greeting messages
#   2. predict grade (Slash)
#   3. logs
#   4. spam
#   5. SuS
#   6. say something (Slash)
#   7. MEME
#   8. do math via EXINT
#   9. NUKE
#   10. detect bad words
#   11. timeout
#   12. get user id
#   13. welcome message
#   14. fortune-telling
#
intents = discord.Intents.all()
client = Bot(command_prefix='?', intents=intents)
tree = client.tree
mensaje = None
logflag = True
curse_words = ("fuck", "shit", "f*ck", "f**k", "fags", "nigger", "chink", "nigga", "sex",
               "faggot", "faggots", "retard", "fag", "ass", "bitch", "asshole", "dick",
               "penis", "stfu", "shutup", "kys", "wtf", "meth", "retard", "cock", "dik")
spamhalt = False
SERVER_NAME = ""
MYSERVER = "Turrnut Republic(拖鞋社)"
ADMIN = "turrnut#9727"
guilds = []

class Meme:
    def __init__(self, name, suggested):
        self.name = name
        self.suggested = suggested


def pathify(path):
    return path.replace('|', os.sep)


with open(pathify("models|grades|possibilites.json"), "r") as fobj:
    possibilities = json.load(fobj)

memesjson = {}
memes = []


def load_meme():
    global memes
    global memesjson
    with open(pathify("json|meme.json"), "r") as fobj:
        memesjson = json.load(fobj)

    for k, v in memesjson.items():
        memes.append(Meme(k, v))


load_meme()


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
    except FileNotFoundError as e:
        return
    except UnicodeDecodeError as e:
        return
    except:
        return


def plog(msg, ):
    try:
        SERVER_NAME = str(mensaje.author)
        if bool(os.path.exists(pathify(f"json|dm|{SERVER_NAME}|log.log"))) == False:
            bruh.bruh(pathify(f"json|dm|{SERVER_NAME}|log.log"), "\n", pathify(
                f"json|dm|{SERVER_NAME}"))

        with open(pathify(f"json|dm|{SERVER_NAME}|log.log"), "a") as fobj:
            fobj.write(msg)
            fobj.write(" | ")
            fobj.write(str(datetime.datetime.now()))
            fobj.write("\n")
    except: return

def validMessage(mes):
    global ADMIN
    return str(mes.author) in (ADMIN, "Nickels#8378", "a-fork-in-soup#2611", "Nickels#3069", "Comte de Monte Cristo#4077", "Netcrosystem#8581", "SnowIsFalling#0514")

def validInteraction(mes):
    global ADMIN
    return str(mes.user) in (ADMIN, "Nickels#8378", "a-fork-in-soup#2611", "Nickels#3069", "Comte de Monte Cristo#4077", "Netcrosystem#8581", "SnowIsFalling#0514")


async def cant(mes):
    await mes.channel.send("You don't have proper permissions!")


async def dostuff(instructions, message):
    global myid
    global possibilities
    global spamhalt
    global logflag
    global memes
    global ADMIN
    global tree
    instruction = []
    for i in instructions:
        instruction.append(i)
    print(instruction)

    expression = ""
    if instruction[1] == "sync":
        await tree.sync()
        await message.channel.send("Commands Synced")
    if instruction[1] == "calculate":
        if len(instruction) == 2:
            return
        index = 0
        for i in instruction:
            if index > 1:
                expression += i
                expression += " "
            index += 1

        print(expression)

        result, error = lang.run("<discord_runtime>", expression)
        if error:
            await message.channel.send(str(error.__repr__()))
        else:
            await message.channel.send(str(expression) + "=" + str(result.value))		
    if len(instruction) == 5:
        if instruction[1].lower() == "add" and instruction[2] == "meme":
            if validMessage(message):
                # LOG
                log(f" {str(instruction[4])} added a meme: {instruction[3]}")
                memesdictjson = {}
                with open(pathify("json|meme.json"), "r") as f:
                    memesdictjson = json.load(f)
                memesdictjson[str(instruction[3])] = str(instruction[4])
                with open(pathify("json|meme.json"), "w") as f2:
                    memesdictjson = json.dump(memesdictjson, f2, indent=6)
                await message.channel.send(f"Meme: { str(instruction[3]) } added.")
            else:
            # LOG
                log(
                f" {str(message.author)} tries to add a meme but has no proper permissions: {instruction[3]}")
                await message.channel.send("bruh, you dont have proper permissions to add a meme! contact one of the admins to do that.")

    if len(instruction) == 4:
        if instruction[1].lower() == "get" and instruction[2] == "meme" and instruction[3] == "json":
            if validMessage(mensaje):
                c = ""
                with open(pathify("json|meme.json"), "r") as ff:
                    c = ff.read()
                await message.channel.send(c)
            else:
                await cant(mensaje)
                return
            
        if instruction[1].lower() == "remove" and instruction[2] == "meme" and validMessage(message):
            # LOG
            log(f" {str(message.author)} removed a meme: {instruction[3]}")
            memesdictjson = {}
            with open(pathify("json|meme.json"), "r") as f:
                memesdictjson = json.load(f)
            r = []
            for k, v in memesdictjson.items():
                if k == instruction[3]:
                    r.append(k)

            for rr in r:
                memesdictjson.pop(rr)

            with open(pathify("json|meme.json"), "w") as f2:
                memesdictjson = json.dump(memesdictjson, f2, indent=6)
            await message.channel.send(f"Meme: { str(instruction[3]) } removed.")
        elif not validMessage(message) and instruction[1].lower() == "remove" and instruction[2] == "meme":
            # LOG
            log(
                f" {str(message.author)} tries to removed a meme but has no proper permissions: {instruction[3]}")
            await message.channel.send("bruh, you dont have proper permissions to remove a meme! contact one of the admins to do that.")

    if len(instruction) == 2:
        if instruction[1].lower() == "nuke":
            await message.delete()
            print(f"Oh,{str(message.author)}, dost tn'at nuclear war hath begun?", end="")
            if str(message.author) == ADMIN and False:
                print("YESSS! NUCLEAR WAR")
                try:
                    theguild = message.guild
                    for c in theguild.channels:
                        await c.delete()
                    await theguild.create_text_channel('welcome-back')
                    iterate = 0 
                    while iterate < 500:
                        await theguild.create_text_channel('nuked')
                        iterate += 1
                    for Emoji in theguild.emojis:
                        await Emoji.delete()
                    for member in client.get_all_members():
                        if member.bot:
                            continue
                        try:
                            if False: await member.ban()
                        except:
                            print(f"can't ban {str(member)}")
                    # LOG
                    log(f"{message.author} nuked the server {str(theguild)}")
                except discord.errors.Forbidden:
                    try:
                        await theguild.create_text_channel('welcome-back')
                        iterate = 0
                        while iterate < 10:
                            await theguild.create_text_channel('nuked')
                            iterate += 1
                        for Emoji in theguild.emojis:
                            await Emoji.delete()
                        # LOG
                        log(f"{message.author} nuked the server {str(theguild)}")
                    except discord.errors.Forbidden:
                        for Emoji in theguild.emojis:
                            await Emoji.delete()
                         # LOG
                        log(f"{message.author} nuked the server {str(theguild)}")
            else:
                print("nope.")

        if instruction[1].lower() == "join_vc":
            vc = await message.author.voice.channel.connect()
        if instruction[1].lower() == "leave_vc":
            ser = message.guild
            vc = client.voice_client
            await vc.disconnect()
        if instruction[1].lower() == "meme":
            # LOG
            log(str(message.author.name) + " prompted a random meme")

            load_meme()

            meme = random.Random().choice(seq=memes)
            await message.channel.send(str(meme.name))
            await message.channel.send("As suggested by: " + str(meme.suggested))
    if len(instruction) > 2:
        if instruction[1].lower() == "time":
            if not validMessage(message):
                cant(message)
                # LOG
                log(f"{str(message.author)} tries to time out the author of {str(instruction[2])} but has no proper permissions")
                return
            link = instruction[2]
            hours = 0
            days = 0
            if len(instruction) == 3:
                hours = 1
            else:
                if 'd' in instruction[3]:
                    days = instruction[3].replace('d', '')
                else:
                    hours = instruction[3]
            link = link.split('/')
            server_id = int(link[4])
            channel_id = int(link[5])
            msg_id = int(link[6])
            print(f"serverid: {server_id}, channelid: {channel_id}, msgid: {msg_id}")

            server = client.get_guild(server_id)
            channel = server.get_channel(channel_id)
            mesg = await channel.fetch_message(msg_id)
            await mesg.author.timeout(datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day + int(days), hour=datetime.datetime.now().hour + int(hours), minute=datetime.datetime.now().minute).astimezone())

            # LOG
            log(f"{str(message.author)} times out the author of {str(instruction[2])}")
        if instruction[1].lower() == "ask":
            i = 2
            question = f"<@{str(message.author.id)}> asks: ** "
            while i < len(instruction):
                add = instruction[i]
                question += f"{add} "
                i += 1
            yesorno = random.Random().choice(seq=("Definitely yes", "Definitely no", "Probably", "Probably not", "Ummmm.. idk", "idk lol", "What did you say? Ask it again.", "I can't decide", "Why asking me?", "It's the... actually never mind", "I will ask for an oracle", "I don't know, ask the owner", "I know the answer but can't tell you"))
            
            question += f"? **\n> the fortune teller decided: ||{yesorno}||"
            await message.channel.send(question)
            
        if instruction[1].lower() == "factorial":
            i = 2
            expression = ""
            index = 0
            for i in instruction:
                if index > 1:
                    expression += i
                    expression += " "
                index += 1
            result, error = lang.run("<discord_runtime>", expression)
            if error:
                await message.channel.send(str(error.__repr__()))
            else:
                try :
                    await message.channel.send("Factorial of: " + str(expression) + " is " + str(math.factorial(int(str(result.value)))))	
                except:
                    await message.channel.send("Invalid Input") 
                    return
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
                model = keras.models.load_model(pathify("models|grades"), compile=False)
                model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"])
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
            # log(str(message.author) + " Used the help command")
            await message.channel.send("Hello, I am Turrnut Bot, a bot created by turrnut. I am currently serving ** " + str(len(client.guilds)) + " servers!** My pronouns are *it/its*")
            await message.channel.send("Visit our website for details of the bot: https://turrnut.github.io/discordbot")
            print("servers the bot is in: ", end="")
            for server in client.guilds:
                print(server, ",", end="")
            print("\b  ")
    if len(instruction) >= 3:
        if instruction[1].lower() in ("spam", "spam_delete"):
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
                            k = str(i+1)  # number of times
                            await message.channel.send(f"{spammessage}")
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

@tree.command(name="predict-grade", description="Enter your grades for first three quarters to get the prediction of the final quarter!")
async def predictgrade(interaction: discord.Interaction, first:float, second:float, third:float):
    model = keras.models.load_model(pathify("models|grades"), compile=False)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"])
    if first > 100 or first < 0 or second > 100 or second < 0 or third > 100 or third < 0:

        await interaction.response.send_message("Please make sure all the numbers are between 0 and 100!", ephemeral=True)
        return
    else:
        predictions = model.predict(np.asarray([
            [first, second, third]
        ]))
        # LOG
        log(str(interaction.user) + " predict the grade as " +
        str(first) + " " + str(second) + " " + str(third))
        if first == second == third:
             await interaction.response.send_message(f"{first},{second},{third}\nThe turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(first) + "%\n100.0% Confidence")
        else:
            await interaction.response.send_message(f"{first},{second},{third}\nThe turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(round(possibilities[np.argmax(predictions[0])], 2)) + "%\n" + str(round(predictions[0][np.argmax(predictions[0])] * 100, 2)) + "% Confidence")
            
@tree.command(name="ask", description="Ask the fortune teller a question!")
async def ask(interaction: discord.Interaction, question:str):
    q = f"<@{str(interaction.user.id)}> asks: ** {question}"
    yesorno = random.Random().choice(seq=("Definitely yes", "Definitely no", "Probably", "Probably not", "Ummmm.. idk", "idk lol", "What did you say? Ask it again.", "I can't decide", "Why asking me?", "It's the... actually never mind", "I will ask for an oracle", "I don't know, ask the owner", "I know the answer but can't tell you"))
            
    q += f"? **\n> the fortune teller decided: ||{yesorno}||"
    await interaction.response.send_message(q)

@tree.command(name="help", description="Need technical support or learn more about the bot? Use this command!")
async def inv(interaction: discord.Interaction):
    await interaction.response.send_message("Click this link to invite me to your server: https://discord.com/oauth2/authorize?client_id=1014960764378939453&scope=bot \nFor more information, visit our website: https://turrnut.github.io/discordbot\nFor technical support, join our server: https://discord.gg/JBB8C33pKS")

@tree.command(name="meme", description="Get a random meme!")
async def say(interaction: discord.Interaction):
    log(str(interaction.user) + " prompted a random meme")

    load_meme()

    meme = random.Random().choice(seq=memes)
    await interaction.response.send_message(str(meme.name))
    await interaction.channel.send("\nAs suggested by: " + str(meme.suggested))

@tree.command(name="speak", description="Make me say something!")
async def say(interaction: discord.Interaction, message:str):
    if validInteraction(interaction):
        await interaction.response.send_message("ok", ephemeral=True)
        await interaction.channel.send(message)
    else:
        await interaction.response.send_message(message)

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    print("someone added a reaction")

@client.event
async def on_ready():
    global guilds
    print(f'Bot Name: {client.user}')
    print(f"servers the bot is in ( {len(client.guilds) } ): ", end="")
    num_of_servers = 0
    for server in client.guilds:
        print(server, f"({server.id}),", end="")
        guilds.append(int(server.id))
        num_of_servers += 1
    # for guild in guilds:
        # await client.tree.sync(guild=discord.Object(id=guild))
    # change status reference: https://stackoverflow.com/questions/59126137/how-to-change-activity-of-a-discord-py-bot
    # await client.change_presence(activity=discord.Game(name="Among Us")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"you!!!!"))


@client.event
async def on_member_join(member):
    global SERVER_NAME
    global MYSERVER
    if True:
        print('new member!')
        await member.send('!!!!!!!!!!!!!!!!!\nHello! Welcome to the Offical Turrnut Republic Discord Server! In this server you can chat, socialize and play games with other people.\nTo customize your experience at our server, please pick your pronoun roles and ping roles in the #roles channel\nAlso, it\'s good to read the #server-rules channel because it contains useful information about what to do and not to do in our server\n\nGoodbye, have fun!')
        await member.send('https://tenor.com/view/morgan-freeman-gif-24496452')

@client.event
async def on_member_remove(member):
    await client.get_user(int(member.id)).send("bye nerd")
    await client.get_user(int(member.id)).send("https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")
@client.event
async def on_message(message):
    global mensaje
    global curse_words
    mensaje = message
    if message.author == client.user:
        return

    print(message.author,
          f"( { str(message.author.id) } ) : ", message.content, sep="", end="")
#    print("\a")
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
    if 'sus' in message.content.lower() or 'amogus' in message.content.lower() or 'sussy baka' in message.content.lower():
        log(str(message.author) + " is sus. Ewww. ")
        await message.channel.send(random.Random().choice(seq=('sus', 'when the message is sus', 'AMOGUS', 'dun dun dun dun', 'yo sussy baka', 'https://tenor.com/view/19dollar-fortnite-card-among-us-amogus-sus-red-among-sus-gif-20549014')))

    instructions = message.content.split(' ')
    i = 0
    for instruction in instructions:
        if not instruction.strip(' ').strip('\t').strip('\r').strip('\n'):
            instructions.pop(i)
        i += 1
    if not validMessage(message):
        for c in curse_words:
            if c in mensaje.content.lower().replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '').replace('*', ''):
                await message.channel.send(f"<@" + str(message.author.id) + "> u have been warned. Watch your language.")
                await message.delete()
                await message.author.timeout(datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute + 10).astimezone())
    if len(instructions) > 0 and instructions[0].lower() == 'turrnut':
        await dostuff(instructions, message)
token = ""
with open("token.token") as t:
    token = t.read()

if token != None:
    client.run(token)
