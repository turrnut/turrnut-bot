import discord
from discord.ext.commands import Bot
intents = discord.Intents.all()
client = Bot(command_prefix='?', intents=intents)
tree = client.tree
@tree.command(name="help", description="Help command")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, I am <@{str(client.id)}>\n")

token = ""
with open("token.token") as t:
    token = t.read()

if token != None:
    client.run(token)