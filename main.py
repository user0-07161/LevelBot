import discord
from discord import app_commands
from discord.ext import commands
import json
import os

db = {}
client = commands.Bot(intents=discord.Intents.all(), command_prefix="!")

try:
    if os.path.isfile("db.json"):
        with open("db.json", "r") as f:
            db = json.load(f)
except:
    db = {}

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Logged in as {client.user} and synced commands.")

@client.tree.command(name="setchannel")
async def setchannel(interaction):
    if interaction.user.guild_permissions.manage_guild:
        try:
            db[str(interaction.guild.id)]["channel"] = str(interaction.channel.id)
        except:
            db[str(interaction.guild.id)] = {}
            db[str(interaction.guild.id)]["channel"] = str()
            db[str(interaction.guild.id)]["channel"] = str(interaction.channel.id)
        print(db)
        with open("db.json", "w") as f:
            json.dump(db, f, indent = 6)
        await interaction.response.send_message("Channel set successfully")

@client.tree.command(name="unsetchannel")
async def unsetchannel(interaction):
    if interaction.user.guild_permissions.manage_guild:
        try:
            db[str(interaction.guild.id)]["channel"] = str()
        except:
            db[str(interaction.guild.id)] = {}
            db[str(interaction.guild.id)]["channel"] = str()
            db[str(interaction.guild.id)]["channel"] = str()
        print(db)
        with open("db.json", "w") as f:
            json.dump(db, f, indent = 6)
        await interaction.response.send_message("Channel unset successfully")

@client.tree.command(name="custommsg", description="Set a custom level up message. Example: '{author} leveled up to {level}.'")
async def custommsg(interaction, message: str):
    if interaction.user.guild_permissions.manage_guild:
        try:
            db[str(interaction.guild.id)]["lupmsg"] = message
        except:
            db[str(interaction.guild.id)] = {}
            db[str(interaction.guild.id)]["lupmsg"] = message
        await interaction.response.send_message(f"Successfully set new level up message to:\n```py\n{message}\n```")
@client.event
async def on_message(message):
    if not message.author.bot:
        try:
            db[str(message.channel.guild.id)][str(message.author.id)]["xp"] = str(int(db[str(message.channel.guild.id)][str(message.author.id)]["xp"]) + 5)
        except:
            try:
                db[str(message.channel.guild.id)][str(message.author.id)]["xp"] = str(0)
            except:
                try:
                    db[str(message.channel.guild.id)][str(message.author.id)] = {}
                    db[str(message.channel.guild.id)][str(message.author.id)]["xp"] = str(0)
                except:
                    db[str(message.channel.guild.id)] = {}
                    db[str(message.channel.guild.id)][str(message.author.id)] = {}
                    db[str(message.channel.guild.id)][str(message.author.id)]["xp"] = str(0)
                    pass

        try:
            db[str(message.channel.guild.id)][str(message.author.id)]["xp"] = str(int(db[str(message.channel.guild.id)][str(message.author.id)]["xp"]) + 5)
        except:
            pass
        try:
            previouslevel = db[str(message.channel.guild.id)][str(message.author.id)]["level"]
        except:
            try:
                db[str(message.channel.guild.id)][str(message.author.id)] = {}
                db[str(message.channel.guild.id)][str(message.author.id)]["level"] = str(0)
                previouslevel = db[str(message.channel.guild.id)][str(message.author.id)]["level"]
            except:
                db[str(message.channel.guild.id)] = {}
                db[str(message.channel.guild.id)][str(message.author.id)] = {}
                db[str(message.channel.guild.id)][str(message.author.id)]["level"] = str(0)
                previouslevel = db[str(message.channel.guild.id)][str(message.author.id)]["level"]
                pass
        try:
            newlevel = int(int(db[str(message.channel.guild.id)][str(message.author.id)]["xp"]) / 50)
            if str(newlevel) != db[str(message.channel.guild.id)][str(message.author.id)]["level"]:
                db[str(message.channel.guild.id)][str(message.author.id)]["level"] = str(newlevel)
                embed = discord.Embed(title="Level up", color=discord.Color.blurple())
                author = message.author.name
                try:
                    msg = db[str(message.channel.guild.id)]["lupmsg"]
                    msg2 = msg.replace("{author}", author)
                    msg = msg2.replace("{level}", str(newlevel))
                    embed.add_field(name = msg, value = "\n")
                except:
                    embed.add_field(name = f"{message.author.name} leveled up! Their new level is {newlevel}.", value = "\n")
                try:
                    channel = client.get_channel(int(db[str(message.channel.guild.id)]["channel"]))
                    await channel.send(embed=embed)
                except:
                    await message.channel.send(embed=embed)
        except:
            pass
        with open("db.json", "w") as f:
            json.dump(db, f, indent = 6)

@client.tree.command(name="setlevel")
async def setlevel(interaction, level: int, user: discord.User):
    if interaction.user.guild_permissions.manage_guild:
        try:
            db[str(interaction.guild.id)][str(user.id)]["xp"] = str(int(int(level) * 50))
            db[str(interaction.guild.id)][str(user.id)]["level"] = str(level)
        except:
            try:
                db[str(interaction.guild.id)][str(user.id)] = {}
            except:
                db[str(interaction.guild.id)] = {}
                db[str(interaction.guild.id)][str(user.id)] = {}
            db[str(interaction.guild.id)][str(user.id)]["xp"] = str(int(int(level) * 50))
            db[str(interaction.guild.id)][str(user.id)]["level"] = str(level)
    await interaction.channel.send(f"Set {user}'s level to {level}")

client.run("token here")