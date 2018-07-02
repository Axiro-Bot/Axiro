import discord
from discord.ext import commands
import time


class General:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def _help(self, beep):
        embed = discord.Embed(title="Hi! I am a bot being built!",
                              description="So here is my current list of commands:")
        embed.add_field(name="General:\n", value="``help`` ``ping`` ``about`` ``user`` ``suggest`` ``report`` ``invite`` ``server`` ``github``", inline=False)
        embed.add_field(name="Anime:\n", value="``danbooru`` ``safebooru`` ``konachan`` ``neko``", inline=False)
        embed.add_field(name="Encryption:\n", value="``encode`` ``decode`` ``hash`` ``encipher`` ``decipher``", inline=False)
        embed.add_field(name="Fun:\n", value="``8ball`` ``ask`` ``kiss`` ``hug`` ``urban``", inline=False)
        embed.add_field(name="Moderation:\n", value="``kick`` ``ban`` ``unban`` ``mute``", inline=False)
        embed.add_field(name="Miscellaneous:\n", value="``math`` ``news``", inline=False)
        embed.set_footer(icon_url=beep.message.author.avatar_url, text="Requested by {}".format(beep.message.author.name))
        await beep.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)
        await ctx.send("Pong! ``Time: {}ms``".format(time_delta))

    @commands.command()
    async def about(self, beep):
        embed = discord.Embed(title="About the Weirdness Bot:", description="This bot was created to do what most "
                                    "bots should do, and then some really weird things.")
        embed.add_field(name="Author: ", value="tangalbert919 (The Freaking iDroid)", inline=False)
        embed.add_field(name="Stats: ", value="Guilds: **{}**\nUnique Players: **{}**\n".format(len(self.bot.guilds),sum(1 for _ in self.bot.get_all_members())), inline=False)
        #embed.add_field(name="Version: ", value=self.bot.version_code)
        embed.set_footer(icon_url=beep.message.author.avatar_url, text="Requested by {}".format(beep.message.author.name))

        await beep.send(embed=embed)

    @commands.command()
    async def user(self, ctx):
        try:
            target = ctx.message.mentions[0]
        except Exception:
            target = ctx.message.author
            await ctx.send("User not found or specified. Collecting information about sender...")
        roles = []
        for x in target.roles:
            roles.append(x.name)
            knownroles = "\n".join(roles)
        embed = discord.Embed(title="Information successfully collected!", description="Here's what we know about {} "
                                    "(also known as {})".format(target.name, target.display_name))
        embed.add_field(name="User ID: ", value=str(target.id), inline=False)
        embed.add_field(name="Current Roles: ", value=knownroles, inline=False)
        embed.add_field(name="Joined Discord on: ", value=target.created_at, inline=False)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_orange(), title="Are you going to invite me to your server?",
                              description="Invite me by clicking [here](https://discordapp.com/api/oauth2/authorize?client_id=458834071796187149&permissions=8&scope=bot).")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_gold(), title="So you want to join my creator's server?",
                              description="Come join the support server by clicking [here](https://discord.gg/NEpsy8h)")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, report: str):
        channel = self.bot.get_channel(460669314933063680)
        color = discord.Colour.blue()
        embed = discord.Embed(color=color, title="Suggestion!", description="We got a suggestion from {}".format(ctx.message.author))
        embed.add_field(name="Suggestion: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your suggestion has been sent.")

    @commands.command()
    async def report(self, ctx, *, report: str):
        channel = self.bot.get_channel(460666448352641026)
        color = discord.Colour.red()
        embed = discord.Embed(color=color, title="Bug report!", description="We got a bug report from {}".format(ctx.message.author))
        embed.add_field(name="Full report: ", value=report)
        await channel.send(embed=embed)
        await ctx.send("Your report has been sent.")

    @commands.command()
    async def github(self, ctx):
        embed = discord.Embed(color=discord.Colour.light_grey(), title="Are you a programmer and want to help?",
                              description="You should click [here](https://github.com/tangalbert919/WeirdnessBot) to see my repository. I am an open-source bot.")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
