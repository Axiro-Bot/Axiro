import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
from datetime import datetime
import aiohttp
import random


class Miscellaneous(commands.Cog, name="Miscellaneous"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def news(self, msg):
        config = json.loads(open('config.json', 'r').read())
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://newsapi.org/v2/top-headlines?country=us&pageSize=1&apiKey={}'
                                       .format(config.get('newsapitoken'))) as resp:
                    top_headlines = await resp.json()
        except Exception:
            await msg.send("I was completely unable to read the news. :(")
            return
        embed = discord.Embed(color=discord.Colour.dark_red(), title="Latest from the news.",
                              description="[{}]({})".format(top_headlines['articles'][0]['title'],
                                                            top_headlines['articles'][0]['url']))
        try:
            embed.set_image(url=top_headlines['articles'][0]['urlToImage'])
        except Exception:
            pass
        await msg.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send("I have been up for "f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def winner(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except Exception:
            memberlist = ctx.message.guild.members
            user = memberlist[random.randint(0, len(memberlist))]
        await ctx.send("Congratulations, {}! You're a winner!".format(user.name))

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def loser(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except Exception:
            memberlist = ctx.message.guild.members
            user = memberlist[random.randint(0, len(memberlist))]
        await ctx.send("Sorry, {}! You're a loser!".format(user.name))

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def drumpf(self, ctx, user: discord.Member):
        if not ctx.message.channel.permissions_for(ctx.message.author.guild.me).manage_nicknames:
            await ctx.send(":x: I do not have permission to edit nicknames.")
            return
        try:
            await user.edit(nick="Donald Drumpf")
        except discord.Forbidden:
            await ctx.send("I do not have permission to do that.")
            return
        await ctx.message.delete()
        await ctx.send("Someone has been turned into Donald Drumpf.")

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def wegothim(self, ctx):
        embed = discord.Embed(color=discord.Colour.red(), title="WE GOT HIM!")
        embed.set_image(url="https://media1.tenor.com/images/4a08ff9d3f956dd814fc8ee1cfaac592/tenor.gif?itemid=10407619")
        await ctx.send(embed=embed)

    def repairJSON(self, temp):
        temp = temp.replace("{\'", "{\"")
        temp = temp.replace("\': ", "\": ")
        temp = temp.replace("\": \'", "\": \"")
        temp = temp.replace("\', \'", "\", \"")
        temp = temp.replace(", \'", ", \"")
        temp = temp.replace("\'}", "\"}")
        temp = temp.replace("True", "\"True\"")
        temp = temp.replace("False", "\"False\"")
        temp = temp.replace("None", "\"None\"")
        #temp = temp[1:-1]
        return temp

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
