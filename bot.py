import discord
import asyncio
import random
from discord.ext import commands

# Prefix
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Events
@bot.event
async def on_ready():
    print('Bot Started Now!')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity = discord.Game(name=f"!help | Написан на Python. ", url="https://www.youtube.com/channel/UCCKAeranFkyNplPYrrGUGoQ", type=3))

@bot.event
async def on_guild_join(guild):
    role = discord.utils.get(guild.roles, name="Muted")
    if not role:
        role = await guild.create_role(name='Muted')
        for channel in guild.channels:
            await channel.set_permissions(role, send_messages=False, connect=False)


# Commands   
# Help
bot.remove_command("help")
@bot.command(description = 'Помощь по боту')
async def help(ctx, arg = None):
    if arg == None:
        emb = discord.Embed(title="Помощь По боту!", color=0xFF0000)
        # Fun
        emb.add_field(name='Шутка которая меняеться КАЖДЫЙ день 🤡', value='`!joke`')
        emb.add_field(name='Посмотреть аватарку пользователя ❓👤', value='`!avatar`')
        # Moderation
        emb.add_field(name='Мьютит участника 🔇', value='`!mute @member`')
        emb.add_field(name='Размьютит участника', value='`!unmute @member`')
        emb.add_field(name='Банит участника 👤❌', value='`!ban айди-участника`')
        emb.add_field(name='Кикает участника 👤❌', value='`!kick айди-участника`')
        await ctx.send(embed = emb)

# Fun
jokes = [
    '- Название могил двух негров? Twix.',
    '- Пациент: Сколько мне осталось? - Доктор: 1 Минута - Пациент: Дайте телефон позвонить родителям.. - Доктор: МИНУТОЧКУ',
    'Девочка без руки играла в прятки и говорит. - я считаю до пяти, не могу до десяти.',
]

@bot.command(description = '')
async def joke(ctx, arg = None):
    if arg == None:
        emb = discord.Embed(title="Шутка 🤡", color=0xFF0000)
        emb.add_field(name=random.choice(jokes), value='\n')
        await ctx.send(embed = emb)

@bot.command(pass_context=True)
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    url = member.avatar
    emb = discord.Embed(title=f'Аватарка участника @{member.name} 👤', color=0xFF0000)
    emb.set_image(url=url)
    await ctx.send(embed=emb)

# Moderation
###
def convert(time):
    pos = ['s','m','h','d','w']

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: str):
    time = convert(duration)
    if time == -1:
        await ctx.send(f'Вы не ввели правильное обозначение времени. Используйте (s/m/h/d/w) пример: !mute @member 15m❗')
        return
    elif time == -2:
        await ctx.send(f'Время должно быть целым числом. Пожалуйста, введите правильное время.❗')
        return

    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f'{member.mention} был замьючен на {duration}. 🔇')
    await asyncio.sleep(time)
    await member.remove_roles(role)
    await ctx.send(f'{member.mention} был размьючен. 🔊')

###
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} Был забанен. 👤❌')

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} Был кикнут. 👤❌')

# Token
bot.run('')