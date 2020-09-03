import discord, random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Economy(commands.Cog, name='Economy'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def balance(self, ctx):
        if not self.bot.usedatabase:
            return await ctx.send('This command requires a running database to work.')
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == self.bot.user.id:
            return await ctx.send('I do not need money, since I\'m a bot.')
        sql = 'SELECT money FROM users WHERE id = $1'
        temp = await self.bot.db.fetchval(sql, user.id)
        money = int(temp)
        if user.id != ctx.message.author.id:
            await ctx.send(f':chicken: **{user.name} has {money} chickens.**')
        else:
            await ctx.send(f':chicken: **You have {money} chickens.**')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def pay(self, ctx, user: discord.User, payment):
        if not self.bot.usedatabase:
            return await ctx.send('This command requires a running database to work.')
        try:
            check = int(payment)
        except Exception:
            return await ctx.send('Please specify an actual amount.')
        if user.id == self.bot.user.id:
            return await ctx.send('You can\'t give me money, since I\'m a bot.')
        sql = 'SELECT money FROM users WHERE id = $1'
        payer = await self.bot.db.fetchval(sql, ctx.message.author.id)
        receiver = await self.bot.db.fetchval(sql, user.id)
        money = int(payer)
        money_two = int(receiver)
        if money < check:
            return await ctx.send('You do not have enough chickens to perform this payment.')
        elif check < 0:
            return await ctx.send('Using negative numbers will not work.')
        paid = money - check
        paid_two = money_two + check
        next_sql = 'UPDATE users SET money = $1 WHERE id = $2'
        await self.bot.db.execute(next_sql, str(paid), ctx.message.author.id)
        await self.bot.db.execute(next_sql, str(paid_two), user.id)
        await ctx.send(f'Successfully paid {payment} chickens to {user.name}!')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.guild_only()
    async def gamble(self, ctx, money):
        if not self.bot.usedatabase:
            return await ctx.send('This command requires a running database to work.')
        try:
            check = int(money)
        except Exception:
            return await ctx.send('Please specify an actual amount.')
        if check < 0:
            return await ctx.send('Gambling a negative amount of chickens, eh? Nice try.')
        sql = 'SELECT money FROM users WHERE id = $1'
        balance = await self.bot.db.fetchval(sql, ctx.message.author.id)
        if balance < money:
            return await ctx.send('You do not have enough chickens for this gamble!')
        raw_chance = 10  # 90% of the time, gamblers will lose their chickens.
        did_i_win = random.randint(1, 100)
        if did_i_win <= raw_chance:
            result = int(balance) + int((check / 2))
            await ctx.send(f'Congrats, you won {int(check / 2)} chickens and got to keep what you bet!')
        else:
            result = int(balance) - check
            await ctx.send(f'You just lost {check} chickens in a gamble! :frowning:')
        next_sql = 'UPDATE users SET money = $1 WHERE id = $2'
        await self.bot.db.execute(next_sql, str(result), ctx.message.author.id)

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    @commands.guild_only()
    async def daily(self, ctx):
        if not self.bot.usedatabase:
            return await ctx.send('This command requires a running database to work.')
        try:
            user = ctx.message.mentions[0]
        except Exception:
            user = ctx.message.author
        if user.id == self.bot.user.id:
            user = ctx.message.author
        sql = 'SELECT money FROM users WHERE id = $1'
        temp = await self.bot.db.fetchval(sql, user.id)
        money = int(temp) + 100
        next_sql = 'UPDATE users SET money = $1 WHERE id = $2'
        await self.bot.db.execute(next_sql, str(money), user.id)
        if user.id != ctx.message.author.id:
            await ctx.send(f'You just gave your {money} chickens to {user.name}!')
        else:
            await ctx.send('You just got 100 chickens.')

    @commands.command()
    @commands.cooldown(1, 300, BucketType.user)
    @commands.guild_only()
    async def raid(self, ctx):
        if not self.bot.usedatabase:
            return await ctx.send('This command requires a running database to work.')
        sql = 'SELECT money FROM users WHERE id = $1'
        tmp = await self.bot.db.fetchval(sql, ctx.message.author.id)
        success = random.randint(1, 10)
        if success > 4:
            award = random.randint(5, 25)
            money = int(tmp) + award
            next_sql = 'UPDATE users SET money = $1 WHERE id = $2'
            await self.bot.db.execute(next_sql, str(money), ctx.message.author.id)
            await ctx.send(f'You successfully raided a farm and got {award} chickens.')
        else:
            await ctx.send('You were attacked by farmers during a raid. :frowning:')

    @commands.command()
    @commands.cooldown(1, 300, BucketType.user)
    @commands.guild_only()
    async def mine(self, ctx):
        if not self.bot.usedatabase:
            return await ctx.send('This command requires a running database to work.')
        sql = 'SELECT money FROM users WHERE id = $1'
        tmp = await self.bot.db.fetchval(sql, ctx.message.author.id)
        success = random.randint(1,10)
        if success > 6:
            award = random.randint(20, 60)
            money = int(tmp) + award
            next_sql = 'UPDATE users SET money = $1 WHERE id = $2'
            await self.bot.db.execute(next_sql, str(money), ctx.message.author.id)
            await ctx.send(f'You mined some minerals and traded them for {award} chickens.')
        else:
            await ctx.send('You couldn\'t find anything valuable while mining. :frowning:')

    @commands.command()
    @commands.cooldown(1, 300, BucketType.user)
    @commands.guild_only()
    async def fish(self, ctx):
        if not self.bot.usedatabase:
            return await ctx.send('This command requires a running database to work.')
        sql = 'SELECT money FROM users WHERE id = $1'
        tmp = await self.bot.db.fetchval(sql, ctx.message.author.id)
        success = random.randint(1,10)
        if success > 6:
            award = random.randint(20, 60)
            money = int(tmp) + award
            next_sql = 'UPDATE users SET money = $1 WHERE id = $2'
            await self.bot.db.execute(next_sql, str(money), ctx.message.author.id)
            await ctx.send(f'You caught some fish and sold them for {award} chickens.')
        else:
            await ctx.send('You couldn\'t find anything while fishing. :frowning:')


def setup(bot):
    bot.add_cog(Economy(bot))