import os
import discord
from dotenv import load_dotenv
from sqlitedict import SqliteDict
from fuzzywuzzy import process

mydict = SqliteDict('./my_db.sqlite', autocommit=True)

load_dotenv()
lwe={}
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    cnt=1
    if message.content.startswith("!coreo"):
        if len(message.content)<8:
            return
        xo = message.content[7:]
        x=''
        channelList = []
        channelmention = {}
        for channel in  message.guild.channels:
            if type(channel) != discord.channel.TextChannel:
                continue
            channelList.append(channel.name)
            channelmention[channel.name] = channel.mention
        for channel,weight in process.extract(xo, channelList):
            x += (f"{cnt} {channel}  {str(weight)} {channelmention[channel]}\n")
            cnt+=1
        if len(x)>0:
            sent=await message.channel.send(x)
            await sent.add_reaction('\N{THUMBS UP SIGN}')
            mydict[sent.id]=xo
        else:
            sent=await message.channel.send(f"No results. Hit like to create channel '{xo}'.")
            await sent.add_reaction('\N{THUMBS UP SIGN}')
            mydict[sent.id]=xo

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message.id not in mydict:
        return
    await reaction.message.guild.create_text_channel(mydict[reaction.message.id])

client.run(TOKEN)
