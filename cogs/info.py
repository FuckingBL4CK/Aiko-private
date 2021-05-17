import json, random, typing, discord, asyncio
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title='Aikos info', description="Here's information about my bot:", color=ctx.me.color)

        # give info about you here
        embed.add_field(name='Author', value='BL4CK#9878', inline=True)

        # Shows the number of servers the bot is member of.
        embed.add_field(name='Server count', value="i'm in " + f'{len(self.bot.guilds)}' + " servers", inline=True)

        # give users a link to invite this bot to their server
        embed.add_field(name='Invite', value='Invite me to your server [here](https://discord.com/api/oauth2/authorize?client_id=746334532965498981&permissions=0&scope=bot)', inline=True)

        embed.add_field(name='Website', value="[Here](Coming soon!)'s my sourcecode", inline=True)

        embed.add_field(name='Support server', value="[Here](https://discord.gg/wyD76A7ytj)'s my support server", inline=True)

        embed.add_field(name='_ _', value='_ _', inline=False)

        embed.add_field(name='Bug report and support:', value= """To give a suggestion and report a bug, typo, issue or anything else go in the suggestion/bug section and make a ticket.
_ _
For further help, join the ✨[support server](https://discord.gg/wyD76A7ytj)✨""", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))
