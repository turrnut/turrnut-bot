import discord
from discord import app_commands
from discord.ext.commands import Bot
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f'Bot Name: {bot.user}')
    for server in bot.guilds:
        await tree.sync(guild=discord.Object(id=server.id))

@tree.command(name="test", description="Test to see if slash commands are working")
async def test(interaction):
    await interaction.response.send_message("Test")

bot.run('MTAxNDk2MDc2NDM3ODkzOTQ1Mw.GKal72.G8iz3HJMu4ck-oz7IDBYjiCMJR_-t2L3kJxD4c')