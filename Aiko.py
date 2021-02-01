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
import functools
import itertools
import math
from async_timeout import timeout
import random
import datetime
import requests
from discord import Embed
from urllib import parse, request
from anekos import NekosLifeClient
import re
import discord
import youtube_dl
import asyncio
import os
import praw
from anekos import NekosLifeClient, SFWImageTags, NSFWImageTags
import random
import requests
import aiohttp
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
nekos = NekosLifeClient()

ltime = time.asctime(time.localtime())
client = command.Bot(command_prefix='&')
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
		await client.change_presence(activity=discord.Game(name='with my pussy'))
		await asyncio.sleep(10)
		await client.change_presence(activity=discord.Game(name='&help'))
		await asyncio.sleep(10)
# Definitions of bot events starts here
# ================================================================================================================
@client.event
async def on_ready():
	print(f'[INFO {ltime}]: Logged in as {client.user.name}!')
	await statuschange()

@client.event
async def on_member_join(ctx, member):
    channel = get(ctx.guild.channels,name="welcome")
    embed=discord.Embed(title="",description=f"**{member.mention} has joined**")
    await channel.send(embed=embed)
# Definitions of bot commands starts here
# ================================================================================================================
@client.command()
async def yeet(ctx, user : discord.Member):
        embed=discord.Embed(title="", description=f"**{ctx.message.author.mention}yeeted{user.mention}**", color=0xff80ff)
        embed.set_image(url=f'https://cdn.discordapp.com/attachments/803152602673184768/803158079847006218/YEET.gif')
        await ctx.send(embed = embed)

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
@client.command()
async def info(ctx):
	embed=discord.Embed(title="Info about the bot", description=" ")
	embed=add_field(name="This bot is open source and BL4CK#9878 shall be credited for the making of this bot.", value=" ")
	await ctx.send(embed = embed)
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
@client.command()
async def FUN(ctx):
	embed=discord.Embed(title="FUN category help", description="[2]", color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name="**&coin**",value="Used to coinflip")
	embed.add_field(name="**&dc**",value="Used to get an random number")

	await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def SFW(ctx):
	embed=discord.Embed(title="SFW category help", description="[10]", color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name="**&kiss**",value="Used to kiss a special person to you")
	embed.add_field(name="**&hug**",value="Used to hug a person")
	embed.add_field(name="**&shibe**",value="Used to get an shibe pic")
	embed.add_field(name="**&cat**",value="Used to get an cat pic")
	embed.add_field(name="**&bird**",value="Used to get an bird pic")
	embed.add_field(name="**&yeet**",value="Used to yeet someone")
	embed.add_field(name="**&heal**",value="Used to heal someone")
	embed.add_field(name="**&spank**",value="Used to spank an naughty person")
	embed.add_field(name="**&waifu**",value="Used to get an waifu pic")
	embed.add_field(name="**&slap**",value="Used to slap the shit out of someone")
	embed.add_field(name="**&av**",value="Used to get an random avatar")
	embed.add_field(name="**&feed**",value="Used to feed someone")
	embed.add_field(name="**&poke**",value="Used to poke someone")


	await ctx.send(embed=embed)
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
@client.command()
async def help(ctx):
	embed=discord.Embed(title="Aiko help", description="Prefix is &", color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name="**&NSFW**",value="Nsfw category help")
	embed.add_field(name="**&SFW**",value="SFW catergory help")
	embed.add_field(name="**&Moderation**",value="Moderation category help")
	embed.add_field(name="**&FUN**",value="Fun category help")
	await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def NSFW(ctx):
	embed=discord.Embed(title="NSFW category help", description="[9]", color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name="**&anal**",value="Used to get an anal gif")
	embed.add_field(name="**&bj**",value="Used to get an blow job pic/gif")
	embed.add_field(name="**&yuri**",value="Used to get lesbian hentai")
	embed.add_field(name="**&cum**",value="Used to get an cum gif")
	embed.add_field(name="**&cumpic**",value="Used to get an cum pic")
	embed.add_field(name="**&solo**",value="Used to get an solo pic")
	embed.add_field(name="**&pussy**",value="Used to get an pussy gif")
	embed.add_field(name="**&hneko**",value="Used to get an neko gif")
	embed.add_field(name="**&trap**",value="Used to get an trap gif")

	await ctx.send(embed=embed)
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


client.run('NzQ2MzM0NTMyOTY1NDk4OTgx.Xz-0Mg.5UPcWAcYUoDpR40tIvKjo0xHrik')
