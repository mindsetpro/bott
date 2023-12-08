import discord
from discord.ext import commands, tasks
import json
import asyncio
import itertools

# Intents
intents = discord.Intents.all()
intents.members = True

# Bot 
bot = commands.Bot(command_prefix=';', intents=intents)

# Config
with open('config.json') as f:
    config = json.load(f)

bot.muted_users = [] 
bot.banned_words = []
status = itertools.cycle(['W Bot frfr', 'grah', 'You thought i was feeling you'])

# Events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - {bot.user.id}')

    bot.log_channel = bot.get_channel(config["log_channel_id"])
    change_status.start()

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the {member.guild.name} Discord!")
    
    embed = discord.Embed(description=f"**{member}** has joined the server")
    await bot.log_channel.send(embed=embed)
    
@bot.event   
async def on_message(message):
    if message.content.lower() in [word.lower() for word in bot.banned_words] and message.author not in bot.muted_users:
        await message.delete()
        await message.channel.send("You can't use that word!", delete_after=5)

    await bot.process_commands(message)

# Commands
@bot.command()
@commands.is_owner()
async def config(ctx):   
    embed = discord.Embed(title="Config", description="**Prefix:** "+config["prefix"])
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    embed = discord.Embed(description=f"**{member}** was banned by {ctx.author} for {reason}")
    await ctx.send(embed=embed)

@bot.command()   
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    bot.muted_users.append(member.id)

    await member.add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
      
    embed = discord.Embed(description=f"**{member}** was muted by {ctx.author} for {reason}")
    await ctx.send(embed=embed)

# Background Task
@tasks.loop(minutes=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status))) 

bot.run(config["token"])
