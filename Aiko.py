import discord
from discord.ext import commands as command
import urllib.request as u
import xml.etree.ElementTree as et
import rule34
import random
import time
import asyncio
from discord.ext.commands import Bot
import anekos
import itertools

import functools
import subprocess
import traceback
import io
import os
import string
import sys
import os, re, psutil, platform, time, sys, fnmatch, subprocess, speedtest, json, struct
import math
from async_timeout import timeout
import random
import datetime
import requests
from discord import Embed
from urllib import parse, request
from anekos import NekosLifeClient
import re
from   discord import errors
from   cogs import Utils, Settings, DisplayName, ReadableTime, GetImage, ProgressBar, UserTime, Message, DL
import discord.utils 
import os
from discord.ext.commands import has_permissions, MissingPermissions
import discord
import youtube_dl
import asyncio
import os
import json
import praw
import datetime
from anekos import NekosLifeClient, SFWImageTags, NSFWImageTags
import random
import requests
import aiohttp
from discord.utils import get
import discord
import asyncio
import os
import urllib.parse, urllib.request, re
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext.commands import has_permissions, MissingPermissions
intents = discord.Intents.default()
intents.members = True
nekos = NekosLifeClient()
intents = discord.Intents().all()
ltime = time.asctime(time.localtime())
guild = discord.Guild
client = command.Bot(command_prefix = '&')
Client = discord.Client()
nekos = NekosLifeClient()
client.remove_command('help')
r = rule34.Rule34
reddit = praw.Reddit(client_id='9M3LEKA2h9dVhA',
                     client_secret='NRxi4kOuRDBTnH8qj3DoWKeAAMSevQ',
                     user_agent='BL4CK98')

def xmlparse(str):
	root = et.parse(u.urlopen(str))
	for i in root.iter('post'):
		fileurl = i.attrib['file_url']
		return fileurl
def xmlcount(str):
	root = et.parse(u.urlopen(str))
	for i in root.iter('posts'):
		count = i.attrib['count']
		return count
def pidfix(str):
	ye = int(xmlcount(r.urlGen(tags=str,limit=1)))
	ye = ye - 1
	return ye
def rdl(str,int):
	print(f'[INFO {ltime}]: integer provided: {int}')

	if int > 2000:
		int = 2000
	if int == 0:
		int == 0
		print(f'[INFO {ltime}]: Integer is 0, accommodating for offset overflow bug. ')
	elif int != 0:
		int = random.randint(1,int)
	print(f'[INFO {ltime}]: integer after randomizing: {int}')
	xurl = r.urlGen(tags=str,limit=1,PID=int)
	print(xurl)
	wr = xmlparse(xurl)

	if 'webm' in wr:
		if 'sound' not in str:
			if 'webm' not in str:
				print(f'[INFO {ltime}]: We got a .webm, user didnt specify sound. Recursing. user tags: {str}')
				wr = rdl(str,pidfix(str))
		else:
			pass
	elif 'webm' not in wr:
		print(f'[INFO {ltime}]: Not a webm, dont recurse.')
	return wr
async def statuschange():
	while True:
		await client.change_presence(activity=discord.Game(name='discord games'))
		await asyncio.sleep(10)
		await client.change_presence(activity=discord.Game(name='&help'))
		await asyncio.sleep(10)
client.sniped_messages = {}
def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

async def update_totals(member):
    invites = await member.guild.invites()

    c = datetime.today().strftime("%Y-%m-%d").split("-")
    c_y = int(c[0])
    c_m = int(c[1])
    c_d = int(c[2])

    async with client.db.execute("SELECT id, uses FROM invites WHERE guild_id = ?", (member.guild.id,)) as cursor: # this gets the old invite counts
        async for invite_id, old_uses in cursor:
            for invite in invites:
                if invite.id == invite_id and invite.uses - old_uses > 0: # the count has been updated, invite is the invite that member joined by
                    if not (c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7): # year can only be less or equal, month can only be less or equal, then check days
                        print(invite.id)
                        await client.db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
                        await client.db.execute("INSERT OR IGNORE INTO joined (guild_id, inviter_id, joiner_id) VALUES (?,?,?)", (invite.guild.id, invite.inviter.id, member.id))
                        await client.db.execute("UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    else:
                        await client.db.execute("UPDATE totals SET normal = normal + 1, fake = fake + 1 WHERE guild_id = ? and inviter_id = ?", (invite.guild.id, invite.inviter.id))

                    return
    
# Definitions of bot events starts here
# ================================================================================================================
token = open("token.txt").read()
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print("----------------------------------------")
    await client.change_presence(activity=discord.Game(name='&help'))

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename}')
            except Exception as e:
                print(f'Failed to load {filename}')
                print(f'[ERROR] {e}')
    print("----------------------------------------")


@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.event
async def on_member_join(member):
    await update_totals(member)
    await client.db.commit()
        
@client.event
async def on_member_remove(member):
    cur = await client.db.execute("SELECT inviter_id FROM joined WHERE guild_id = ? and joiner_id = ?", (member.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        return
    
    inviter = res[0]
    
    await client.db.execute("DELETE FROM joined WHERE guild_id = ? AND joiner_id = ?", (member.guild.id, member.id))
    await client.db.execute("DELETE FROM totals WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, memebr.id))
    await client.db.execute("UPDATE totals SET left = left + 1 WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, inviter))
    await client.db.commit()

@client.event
async def on_invite_create(invite):
    await client.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (invite.guild.id, invite.inviter.id, invite.uses, 0, 0))
    await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
    await client.db.commit()
    
@client.event
async def on_invite_delete(invite):
    await client.db.execute("DELETE FROM invites WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
    await client.db.commit()

@client.event
async def on_guild_join(guild): # add new invites to monitor
    for invite in await guild.invites():
        await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses), VAlUES (?,?,?)", (guild.id, invite.id, invite.uses))
        
    await client.db.commit()
    
@client.event
async def on_guild_remove(guild): # remove all instances of the given guild_id
    await client.db.execute("DELETE FROM totals WHERE guild_id = ?", (guild.id,))
    await client.db.execute("DELETE FROM invites WHERE guild_id = ?", (guild.id,))
    await client.db.execute("DELETE FROM joined WHERE guild_id = ?", (guild.id,))

    await client.db.commit()
# Definitions of bot commands starts here
# ================================================================================================================
@client.command()
async def invites(ctx, member: discord.Member=None):
    if member is None: member = ctx.author

    # get counts
    cur = await client.db.execute("SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?", (ctx.guild.id, member.id))
    res = await cur.fetchone()
    if res is None:
        normal, left, fake = 0, 0, 0

    else:
        normal, left, fake = res

    total = normal - (left + fake)
    
    em = discord.Embed(
        title=f"Invites for {member.name}#{member.discriminator}",
        description=f"{member.mention} currently has **{total}** invites. (**{normal}** normal, **{left}** left, **{fake}** fake).",
        timestamp=datetime.now(),
        colour=discord.Colour.orange())

    await ctx.send(embed=em)

# ================================================================================================================
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.UserInputError):
        await ctx.send("You messed up writing the command.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        if hasattr(error, "original"):
            error = error.original
        await ctx.send(discord.utils.escape_mentions(
             f"Something went wrong. ``{type(error).__name__}: {discord.utils.escape_markdown(str(error))}``"
        ))
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# ================================================================================================================
@client.command()
async def snipe(ctx):
    try:

        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    except:

        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)
# ================================================================================================================
@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):

    
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')
# ================================================================================================================
@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):

    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel unlocked.')
# ================================================================================================================
@client.command()
async def vote(ctx):
    embed=discord.Embed(title="Your bots vote page", description="If u vote i give 1 candy", color=0xff80ff)
    embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name="**Vote Link:**",value="https://top.gg/bot/yourbotspage/vote")
    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
@commands.guild_only()
async def ping(ctx):
    start= time.time()
    async with ctx.message.channel.typing(): 
        end_time = time.time()
        result = end_time - start
        result1 = round(result * 1000)
        apiresult=round(client.latency*1000)
        embed=discord.Embed(title="Pong!", description=f"My ping is `{result1}ms`\nApi ping is `{apiresult}ms`", color=0xff80ff)
        embed.color=0xff80ff
        await asyncio.sleep(0.1)
        message = await ctx.send(embed=embed)
       
# ================================================================================================================
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Aiko help", description="The prefix is &", color=0xff80ff, inline=False)
    
    embed.add_field(name="😂Fun",value="`yeet`,`wallpaper`,`baka`,`kiss`,`avatar`,`tickle`,`bird`,`slap`,`hug`,`poke`,`cat`,`dc`,`feed`,`lizard`,`coin`,`cuddle`,`pat`")
    embed.add_field(name="📻Music",value="`play`,`skip`,`pause`,`volume`,`join`,`repeat`,`resume`,`songinfo`,`download`,`leave`")
    embed.add_field(name="🚨Admin",value="`addaccess <role_id>`,`delaccess <role_id>`,`addpingedrole <role_id>`,`delpingedrole <role_id>`,`addadminrole <role_id>`,`deladminrole <role_id>`")
    embed.add_field(name="🔞Nsfw",value="`pussy`,`solo`,`anal`,`hneko`,`neko`,`trap`,`cum`,`cumpic`,`feet`,`kuni`,`gwank`,`yuri`,`bj`,`spank`") 
    embed.add_field(name="🚨Moderation",value="`ban`,`unban`,`purge`,`say`,`kick`,`mention`,`snipe`")   
    embed.add_field(name="🌡️Level",value="`stats`,`leaderboard`")
    embed.add_field(name="🎫Tickets",value="`new`, `close`") 
    embed.add_field(name="✉️InviteManager",value="`invites`")
    embed.add_field(name="⚒️Utils",value="`uuid`,`info`")
    embed.add_field(name="🎉Giveaway",value="`gstart`") 

    embed.set_image(url=f'https://cdn.discordapp.com/attachments/735563678879055934/810473460844986378/standard.gif')

    embed.set_footer(text=f'Requested by {ctx.author.display_name}. ')
    await ctx.send(embed=embed)
# ================================================================================================================

# ================================================================================================================

# ================================================================================================================
@client.command()
@has_permissions(administrator=True)
async def deladminrole(ctx, role_id=None):
    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        admin_roles = data["verified-roles"]

        if role_id in admin_roles:
            index = admin_roles.index(role_id)

            del admin_roles[index]

            data["verified-roles"] = admin_roles

            with open('data.json', 'w') as f:
                json.dump(data, f)
            
            em = discord.Embed(title="Aiko", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0xff80ff)

            await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Aiko", description="That role isn't getting pinged when new tickets are created!", color=0xff80ff)
            await ctx.send(embed=em)

    except:
        em = discord.Embed(title="Aiko", description="That isn't a valid role ID. Please try again with a valid role ID.")
        await ctx.send(embed=em)
# ================================================================================================================
@client.command()
@has_permissions(administrator=True)
async def addadminrole(ctx, role_id=None):

    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        data["verified-roles"].append(role_id)

        with open('data.json', 'w') as f:
            json.dump(data, f)
        
        em = discord.Embed(title="Aiko", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0xff80ff)
        await ctx.send(embed=em)

    except:
        em = discord.Embed(title="Aiko", description="That isn't a valid role ID. Please try again with a valid role ID.")
        await ctx.send(embed=em)
# ================================================================================================================
@client.command()
async def delpingedrole(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            pinged_roles = data["pinged-roles"]

            if role_id in pinged_roles:
                index = pinged_roles.index(role_id)

                del pinged_roles[index]

                data["pinged-roles"] = pinged_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Aiko", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0xff80ff)
                await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title="Aiko", description="That role already isn't getting pinged when new tickets are created!", color=0xff80ff)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Aiko", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Aiko", description="Sorry, you don't have permission to run that command.", color=0xff80ff)
        await ctx.send(embed=em)
# ================================================================================================================
@client.command()
async def addpingedrole(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:

        role_id = int(role_id)

        if role_id not in data["pinged-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["pinged-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Aiko", description="You have successfully added `{}` to the list of roles that get pinged when new tickets are created!".format(role.name), color=0xff80ff)

                await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Aiko", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
            
        else:
            em = discord.Embed(title="Aiko", description="That role already receives pings when tickets are created.", color=0xff80ff)
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Aiko", description="Sorry, you don't have permission to run that command.", color=0xff80ff)
        await ctx.send(embed=em)
# ================================================================================================================
@client.command()
async def delaccess(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            valid_roles = data["valid-roles"]

            if role_id in valid_roles:
                index = valid_roles.index(role_id)

                del valid_roles[index]

                data["valid-roles"] = valid_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Auroris Tickets", description="You have successfully removed `{}` from the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)
            
            else:
                
                em = discord.Embed(title="Auroris Tickets", description="That role already doesn't have access to tickets!", color=0x00a8ff)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Auroris Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Auroris Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)        
# ================================================================================================================
@client.command()
async def addaccess(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:
        role_id = int(role_id)

        if role_id not in data["valid-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["valid-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)
                
                em = discord.Embed(title="Aiko", description="You have successfully added `{}` to the list of roles with access to tickets.".format(role.name), color=0xff80ff)

                await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Aiko", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Aiko", description="That role already has access to tickets!", color=0xff80ff)
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Aiko", description="Sorry, you don't have permission to run that command.", color=0xff80ff)
        await ctx.send(embed=em)
# ================================================================================================================
@client.command()
async def close(ctx):
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(title="Aiko", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0xff80ff)
        
            await ctx.send(embed=em)
            await client.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
        
        except asyncio.TimeoutError:
            em = discord.Embed(title="Aiko", description="You have run out of time to close this ticket. Please run the command again.", color=0xff80ff)
            await ctx.send(embed=em)
# ================================================================================================================
@client.command()
async def new(ctx, *, args = None):

    await client.wait_until_ready()

    if args == None:
        message_content = "Please wait, we will be with you shortly!"
    
    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)

    ticket_number = int(data["ticket-counter"])
    ticket_number += 1

    ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0xff80ff)

    await ticket_channel.send(embed=em)

    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data.json", 'w') as f:
        json.dump(data, f)
    
    created_em = discord.Embed(title="Aiko", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0xff80ff)
    
    await ctx.send(embed=created_em)


# ================================================================================================================
@client.command()
async def yeet(ctx, user : discord.Member):
        embed=discord.Embed(title="", description=f"**{ctx.message.author.mention}yeeted{user.mention}**", color=0xff80ff)
        embed.set_image(url=f'https://cdn.discordapp.com/attachments/803152602673184768/803158079847006218/YEET.gif')
        await ctx.send(embed = embed)
# ================================================================================================================

@client.command(pass_context=True)
@command.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    embed=discord.Embed(title="", description=f"**Cleared by {ctx.message.author.mention}**", color=0xff80ff)
    embed.set_image(url=f'https://i.pinimg.com/originals/47/12/89/471289cde2490c80f60d5e85bcdfb6da.gif')
    await ctx.channel.purge(limit=limit)
    await ctx.send(embed=embed)
    await ctx.message.delete()
# ================================================================================================================
@client.command()
async def wallpaper(ctx):
    image = await nekos.image("wallpaper")
    embed = Embed()
    embed=discord.Embed(description=f"**Here have a wallpaper**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def baka(ctx):
    image = await nekos.image("baka")
    embed = Embed()
    embed=discord.Embed(description=f"**Baka!**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def kuni(ctx):

    if ctx.channel.is_nsfw():
        image = await nekos.image("kuni")
        embed = Embed()
        embed=discord.Embed(description=f"**Here have some kuni hentai!**")
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def feet(ctx):

    if ctx.channel.is_nsfw():
        image = await nekos.image("feet")
        embed = Embed()
        embed=discord.Embed(description=f"**Here have some feet!**")
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def gwank(ctx):

    if ctx.channel.is_nsfw():
        image = await nekos.image("pwankg")
        embed = Embed()
        embed=discord.Embed(description=f"**Here have a gif of a girl wanking!**")
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def lizard(ctx):
    image = await nekos.image("lizard")
    embed = Embed()
    embed=discord.Embed(description=f"**Here have a lizard!**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)



# ================================================================================================================
@client.command()
@commands.has_role("Giveaways")
async def gstart(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

    questions = ["Which channel should it be hosted in?", 
                "What should be the duration of the giveaway? (s|m|h|d)",
                "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


    embed = discord.Embed(title = "🎉Giveaway!🎉", description = f"{prize}", color=0x8B0000, inline=True )

    embed.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")
# ================================================================================================================
@client.command()
@commands.has_role("Giveaways")
async def greroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}.!")    
# ================================================================================================================

# ================================================================================================================

# ================================================================================================================

# ================================================================================================================

# ================================================================================================================

# ================================================================================================================

# ================================================================================================================

# ================================================================================================================

# ================================================================================================================

# ================================================================================================================



@client.command()
async def role(ctx, * role: discord.Role):
  user = ctx.message.author
  await user.add_roles(role)
# ================================================================================================================

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, command.MissingPermissions):
        await ctx.send("You cant do that!")
# ================================================================================================================
@client.command()
async def shutup(ctx, user : discord.Member):
        embed=discord.Embed(title="", description=f"**Shut up!!!{user.mention}**", color=0xff80ff)
        embed.set_image(url=f'https://cdn.kapwing.com/final_6011b5876dfaad00787b2687_253255.mp4')
        await ctx.send(embed = embed)

# ================================================================================================================
@client.command()
async def heal(ctx, user : discord.Member):
        embed=discord.Embed(title="", description=f"**{ctx.message.author.mention}HEALED{user.mention}**", color=0xff80ff)
        embed.set_image(url=f'https://media1.tenor.com/images/7a1bc74cf91eedfb0ea7027dacdc9e59/tenor.gif?itemid=20036165')
        await ctx.send(embed = embed)
# ================================================================================================================

# ================================================================================================================
@client.command()
@command.has_permissions(ban_members=True)
async def ban(self, ctx, member: discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'**{user.mention} has banned**')
# ================================================================================================================
@client.command()
@command.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if member == user.name+"#"+user.discriminator or member == str(user.id):
            await ctx.guild.unban(user)
            await ctx.send(f'**{user.mention} has been unbanned**')
            return
# ================================================================================================================
@client.command()
@command.has_permissions(kick_members=True)
async def kick(self, ctx, member: discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'**{user.mention} has been kicked**')
# ================================================================================================================
@client.command()
async def neko(ctx, user: discord.Member):
    if ctx.channel.is_nsfw():
        image = await nekos.image("neko")
        embed = Embed()
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def slap(ctx, user: discord.Member):
    image = await nekos.image("slap")
    embed = Embed()
    embed=discord.Embed(description=f"**{ctx.message.author.mention}slapped{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def waifu(ctx):
    image = await nekos.image("waifu")
    embed = Embed()
    embed=discord.Embed(description=f"**Here have some waifu pics**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def spank(ctx, user: discord.Member):
    if ctx.channel.is_nsfw():

        image = await nekos.image("spank")
        embed = Embed()
        embed=discord.Embed(description=f"**{ctx.message.author.mention}spanked{user.mention}**")
        embed.set_image(url=image.url)

        await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def trap(ctx):

    if ctx.channel.is_nsfw():
        image = await nekos.image("trap")
        embed = Embed()
        embed=discord.Embed(description=f"**Here have some trap hentai!**")
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def hneko(ctx):

    if ctx.channel.is_nsfw():
        image = await nekos.image("nsfw_neko_gif")
        embed = Embed()
        embed=discord.Embed(description=f"**Here have some neko hentai!**")
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def cum(ctx):

	if ctx.channel.is_nsfw():
		image = await nekos.image("cum")
		embed = Embed()
		embed=discord.Embed(description=f"**Here have some cum!**")
		embed.set_image(url=image.url)
		await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def bj(ctx):

	if ctx.channel.is_nsfw():
		image = await nekos.image("bj")
		embed = Embed()
		embed=discord.Embed(description=f"**Here have some bj!**")
		embed.set_image(url=image.url)
		await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def yuri(ctx):

	if ctx.channel.is_nsfw():
		image = await nekos.image("yuri")
		embed = Embed()
		embed=discord.Embed(description=f"**Here have a yuri gif!**")
		embed.set_image(url=image.url)
		await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def anal(ctx):

	if ctx.channel.is_nsfw():
		image = await nekos.image("cum_jpg")
		embed = Embed()
		embed=discord.Embed(description=f"**Here have a anal gif!**")
		embed.set_image(url=image.url)
		await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def solo(ctx):

	if ctx.channel.is_nsfw():
		image = await nekos.image("solo")
		embed = Embed()
		embed=discord.Embed(description=f"**Here have a solo gif!**")
		embed.set_image(url=image.url)
		await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def pussy(ctx):

	if ctx.channel.is_nsfw():
		image = await nekos.image("pussy")
		embed = Embed()
		embed=discord.Embed(description=f"**Here have some pussy!**")
		embed.set_image(url=image.url)
		await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def hug(ctx, user: discord.Member):
    image = await nekos.image("hug")
    embed = Embed()
    embed=discord.Embed(description=f"**{ctx.message.author.mention}hugged{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================

@client.command()
async def cuddle(ctx, user: discord.Member):
    image = await nekos.image("cuddle")
    embed = Embed()
    embed=discord.Embed(description=f"**{ctx.message.author.mention}cuddle{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def kiss(ctx, user: discord.Member):
    image = await nekos.image("kiss")
    embed = Embed()
    embed=discord.Embed(title="",description=f"**{ctx.message.author.mention}kissed{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def mention(ctx, user : discord.Member):
	await ctx.send(user.mention)
# ================================================================================================================
@client.command()
async def pat(ctx, user: discord.Member):
    image = await nekos.image("pat")
    embed = Embed()
    embed=discord.Embed(title="",description=f"**{ctx.message.author.mention}pat{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command(pass_context=True, no_pm=True)
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed(description='\n{0}'.format(ctx.author))
    embed.set_thumbnail(url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def tickle(ctx, user: discord.Member):
    image = await nekos.image("tickle")
    embed = Embed()
    embed=discord.Embed(title="",description=f"**{ctx.message.author.mention}tickled{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = [
  discord.Embed(title='It is certain.'),
  discord.Embed(title='It is decidedly so.'),
  discord.Embed(title='Without a doubt.'),
  discord.Embed(title='Yes - definitely.'),
  discord.Embed(title='You may rely on it.'),
  discord.Embed(title='Most likely.'),
  discord.Embed(title='Outlook good.'),
  discord.Embed(title='Yes.'),
  discord.Embed(title='Signs point to yes.'),
  discord.Embed(title='Reply hazy, try again.'),
  discord.Embed(title='Ask again later.'),
  discord.Embed(title='Better not tell you now.'),
  discord.Embed(title='Cannot predict now.'),
  discord.Embed(title='Concentrate and ask again.'),
  discord.Embed(title="Don't count on it."),
  discord.Embed(title='My reply is no.'),
  discord.Embed(title='My sources say no.'),
  discord.Embed(title='Outlook not very good.'),
  discord.Embed(title='Very doubtful.')
    ]
  responses = random.choice(responses)
  await ctx.send(content=f'Question: {question}\nAnswer:', embed=responses)







# ================================================================================================================
@client.command(name="say")
@command.has_permissions(manage_messages=True)
async def say(ctx, *,message):
	await ctx.message.delete()
	embed = discord.Embed(color=ctx.author.color,timestamp=ctx.message.created_at)
	embed.set_author(name="Announcement!", icon_url=ctx.author.avatar_url)
	embed.add_field(name=f"Sent by {ctx.message.author}", value=str(message))
	embed.set_thumbnail(url=ctx.author.avatar_url)
	await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def av(ctx):
    image = await nekos.image("avatar")
    embed = Embed()
    embed=discord.Embed(title="",description=f"**Here have an avatar**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def feed(ctx, user: discord.Member):
    image = await nekos.image("feed")
    embed = Embed()
    embed=discord.Embed(title="",description=f"**{ctx.message.author.mention}fed{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def poke(ctx, user: discord.Member):
    image = await nekos.image("poke")
    embed = Embed()
    embed=discord.Embed(title="",description=f"**{ctx.message.author.mention}poked{user.mention}**")
    embed.set_image(url=image.url)

    await ctx.send(embed=embed)
# ================================================================================================================

# ================================================================================================================
@client.command()
async def coin(ctx):
	side = random.randint(1,100)
	if side == 50 or side > 50:
		await ctx.channel.send('***The coin landed on heads***')
	if side < 50:
		await ctx.channel.send('***The coin landed on tails.***')
# ================================================================================================================

# ================================================================================================================

# ================================================================================================================
#@client.command()
#async def FUN(ctx):
#	embed=discord.Embed(title="FUN category help", description="[2]", color=0xff80ff)
#	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
#   embed.add_field(name="**>coinflip*",value="Used to coinflip")
#	embed.add_field(name="**>dc**",value="Used to get an random number")
#
#	await ctx.send(embed=embed)
# ================================================================================================================
#@client.command()
#async def SFW(ctx):
#	embed=discord.Embed(title="SFW category help", description="[10]", color=0xff80ff)
#	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
#    embed.add_field(name="**>kiss**",value="Used to kiss a special person to you")
#	embed.add_field(name="**>hug**",value="Used to hug a person")
#	embed.add_field(name="**>shibe**",value="Used to get an shibe pic")
#	embed.add_field(name="**>cat**",value="Used to get an cat pic")
#	embed.add_field(name="**>bird**",value="Used to get an bird pic")
#	embed.add_field(name="**>yeet**",value="Used to yeet someone")
#	embed.add_field(name="**>heal**",value="Used to heal someone")
#	embed.add_field(name="**>spank**",value="Used to spank an naughty person")
#	embed.add_field(name="**>waifu**",value="Used to get an waifu pic")
#	embed.add_field(name="**>slap**",value="Used to slap the shit out of someone")
#	embed.add_field(name="**>av**",value="Used to get an random avatar")
#	embed.add_field(name="**>feed**",value="Used to feed someone")
#	embed.add_field(name="**>poke**",value="Used to poke someone")
#
#
#	await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def dc(ctx,arg1,arg2 = 1):

	a = str(arg1)
	if str(arg2) != '':
		b = str(arg2)

	print('a is equal to' + a)
	print('b is equal to' + b) # it is really this simple.
	if b == '':
		dside = str(random.randint(1,int(a)))
		await ctx.channel.send(f'You rolled:' + ' ' + dside)
	else:
		mx = int(a) * int(b)
		print('max is:' + str(mx))
		total = str(random.randint(1,mx))
	await ctx.channel.send(f'You rolled a total of:' + ' ' + total)
# ================================================================================================================
#@client.command()
#async def help(ctx):
#	embed=discord.Embed(title="Aiko help", description="Prefix is >", color=0xff80ff)
#	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
#   embed.add_field(name="**>NSFW**",value="Nsfw category help")
#	embed.add_field(name="**>SFW**",value="SFW catergory help")
#	embed.add_field(name="**>Moderation**",value="Moderation category help")
#	embed.add_field(name="**>FUN**",value="Fun category help")
#	await ctx.send(embed=embed)
# ================================================================================================================
#@client.command()
#async def NSFW(ctx):
#	embed=discord.Embed(title="NSFW category help", description="[9]", color=0xff80ff)
#	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
#    embed.add_field(name="**>anal**",value="Used to get an anal gif")
#	embed.add_field(name="**>bj**",value="Used to get an blow job pic/gif")
#	embed.add_field(name="**>yuri**",value="Used to get lesbian hentai")
#	embed.add_field(name="**>cum**",value="Used to get an cum gif")
#	embed.add_field(name="**>cumpic**",value="Used to get an cum pic")
#	embed.add_field(name="**>solo**",value="Used to get an solo pic")
#	embed.add_field(name="**>pussy**",value="Used to get an pussy gif")
#	embed.add_field(name="**>hneko**",value="Used to get an neko gif")
#	embed.add_field(name="**>trap**",value="Used to get an trap gif")
#
#	await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def shibe(ctx):
	r = requests.get('https://shibe.online/api/shibes?count=1')
	y = r.json()
	embed= discord.Embed(title='Have a shibe.',color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar_url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
	await ctx.send(embed=embed)

# ================================================================================================================
@client.command()
async def cat(ctx):
	r = requests.get('https://shibe.online/api/cats?count=1')
	y = r.json()
	embed = discord.Embed(title='Have a kitty.',color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar_url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
	await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def bird(ctx):
	r = requests.get('https://shibe.online/api/birds?count=1')
	y = r.json()
	embed= discord.Embed(title='Have a bird.',color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar_url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
	await ctx.send(embed=embed)
# ================================================================================================================
async def setup():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect("inviteData.db")
    await client.db.execute("CREATE TABLE IF NOT EXISTS totals (guild_id int, inviter_id int, normal int, left int, fake int, PRIMARY KEY (guild_id, inviter_id))")
    await client.db.execute("CREATE TABLE IF NOT EXISTS invites (guild_id int, id string, uses int, PRIMARY KEY (guild_id, id))")
    await client.db.execute("CREATE TABLE IF NOT EXISTS joined (guild_id int, inviter_id int, joiner_id int, PRIMARY KEY (guild_id, inviter_id, joiner_id))")
    
    # fill invites if not there
    for guild in client.guilds:
        for invite in await guild.invites(): # invites before client was added won't be recorded, invitemanager/tracker don't do this
            await client.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
            await client.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (guild.id, invite.inviter.id, 0, 0, 0))
                                 
    await client.db.commit()
#client.load_extension('cogs.maincog')
client.loop.create_task(setup())
client.run(token)
asyncio.run(client.db.close())
