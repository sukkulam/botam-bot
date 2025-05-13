import discord
from discord.ext import commands
from gtts import gTTS
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 점수 저장소
scores = {}

@bot.event
async def on_ready():
    print(f"{bot.user} 봇이 준비되었습니다.")

@bot.command()
async def 점수(ctx, member: discord.Member = None):
    member = member or ctx.author
    score = scores.get(member.id, 0)
    await ctx.send(f"{member.mention}의 점수는 {score}점입니다.")

@bot.command()
async def 점수추가(ctx, member: discord.Member, value: int):
    scores[member.id] = scores.get(member.id, 0) + value
    await ctx.send(f"{member.mention}에게 {value}점을 추가했습니다.")

@bot.command()
async def 점수초기화(ctx, member: discord.Member = None):
    member = member or ctx.author
    scores[member.id] = 0
    await ctx.send(f"{member.mention}의 점수가 초기화되었습니다.")

@bot.command()
async def v(ctx, *, text):
    tts = gTTS(text=text, lang='ko')
    tts.save("say.mp3")
    if ctx.author.voice and ctx.author.voice.channel:
        vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio("say.mp3"))
        while vc.is_playing():
            pass
        await vc.disconnect()
        os.remove("say.mp3")
    else:
        await ctx.send("먼저 음성 채널에 들어가주세요.")

bot.run(TOKEN)
