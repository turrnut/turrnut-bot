from discord.ext.commands import Bot

client = Bot(command_prefix="")

@client.event
async def on_ready():
    print(f'{client.user} v1.0')
    print('created by turrnut')
    print(f"served in ( {len(client.guilds) } ): ", end="")
    for server in client.guilds:
        print(server, ",", end=" ")
    print("\b     ")
    print()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == 'hi':
        await message.channel.send("hello")

client.run('MTA5NjU3ODU4MDIwNjU5MjAzMA.G2RT6s.SQGHdI_CRkycGPJJvP9idnsVRM5gEtA87ULY6c')
