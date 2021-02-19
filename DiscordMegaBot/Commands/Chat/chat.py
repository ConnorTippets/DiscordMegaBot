import discord
from discord.ext import commands

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currently_playing = False
        self.starter = None
        self.ms = []
    
    @commands.group(brief='Responds to currently running chat', invoke_without_command=True)
    async def chat(self, ctx, *, message:str):
        cmd = self.bot.get_command('chat response')
        await cmd(ctx, message=message)
    
    @chat.command(brief='Starts a chat', aliases=['h'])
    async def host(self, ctx, *, message:str):
        if self.currently_playing:
            return await ctx.send('Theres already a chat active!')
        self.starter = ctx.author
        self.currently_playing = True
        e = discord.Embed(description=f'**Main message**: {message}\n')
        e.set_author(icon_url=self.starter.avatar_url, name='Chat')
        self.m = await ctx.send(embed=e)
        self.ms = [self.m]
        self.mm = message
    
    async def (self, message, embed):
        try:
            await message.edit(embed=embed)
        except discord.HTTPException:
             for m in self.ms:
                m.embeds[0].description = f'**Main message**: {self.mm}\n[jump!]({ctx.message.jump_url}) **{ctx.author.name.title()}**: {message}'
                self.bot.loop.create_task(self.edit(m, m.embeds[0]))
    async def update(self, ctx, message):
        if self.currently_playing is False:
            return await ctx.send('No currently playing chat')
        if self.m.embeds[0].description.endswith('\n'):
            for m in self.ms:
                m.embeds[0].description = f'[jump!]({ctx.message.jump_url}) **{ctx.author.name.title()}**: {message}'
                self.bot.loop.create_task(self.edit(m, m.embeds[0]))
        else:
            for m in self.ms:
                m.embeds[0].description += f'\n[jump!]({ctx.message.jump_url}) **{ctx.author.name.title()}**: {message}'
                self.bot.loop.create_task(self.edit(m, m.embeds[0]))
        
    @chat.command(brief='Responds to currently running chat', aliases=['reply', 'r'])
    async def response(self, ctx, *, message:str):
        self.bot.loop.create_task(self.update(ctx, message))
        
    @chat.command(brief='Stops currently running chat')
    async def stop(self, ctx):
        if self.currently_playing is False:
            return await ctx.send('No currently playing chat')
        self.starter = None
        self.currently_playing = False
        for m in self.ms:
            await m.delete()
        self.ms = []
    
    @chat.command(brief='Shows currently running chat')
    async def show(self, ctx):
        if self.currently_playing is False:
            return await ctx.send('No currently playing chat')
        m = await ctx.send(embed=self.m.embeds[0])
        self.ms.append(m)

def setup(bot):
    bot.add_cog(Chat(bot))
