import os
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ACTIVITY = discord.Game(name="With Mayo")
COPYPASTAS = {
    "almonds": "I like my almonds any way I can get them, whether it be from strangers, from my house, or off the street. But I would have to say my favorite type of almonds are the almonds I find in public restrooms. I find these almonds on the floor, in the sink, and in the soap dispenser. Whenever there is an almond nearby, I have to find it, and keep it with me,\nI would say my house is full of about 112,382 almonds by now. Everyday I find around 22 almonds, and store them in my pocket, or in my purse until I get home. Then, I put them in my almond room.\nMy almond room is a very special place to me, it has almonds all over the floor, and some on the walls also. I spend all the time I can in my almond room. I sleep in there, I do schoolwork in there, and sometimes, I just roll around in there for hours and hours on end.\nMy addiction started when I was born. My parents were almond fanatics as well, and from a very young age I was taught to seek almonds out and keep them for my own. And throughout the years, my obsession with almonds has just kept growing. I love them. I devote my life to finding them. Sometimes I skip school just to go to a public place and hunt for almonds. Almonds are just really appealing to me, from their nutty smell to their beautiful brown shell.",
    "seal": "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo."
    }

client = discord.Client()

async def nuke(channel):
    deleted = await channel.purge(limit=1000000)
    await channel.send(f'deleted {len(deleted)} messages')

async def countdown(num, action, channel):
    if(num!=0):
        if('cancel' in channel.last_message.content):
            pass
        else:
            await channel.send(f'{num} seconds remaining')
            num-=1
            await asyncio.sleep(1)
            await countdown(num, action, channel)
    else:
        await action(channel)

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')

    for guild in client.guilds:
        print(f'{client.user} is conected to guild: {guild} (id: {guild.id})')

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    await client.change_presence(status=discord.Status.online, activity=ACTIVITY)

@client.event
async def on_message(message):
    content = message.content
    author = message.author
    channel = message.channel
    if(("league" in content.lower()) or ("LoL" in content)):
        await channel.send(f'Please shut the fuck up {author.mention}')
    if(("who's on" in content.lower()) or ("whos on" in content.lower())):
        guild = channel.guild
        members = [member for member in guild.members]
        activities = {}
        for member in members:
            activities.update({member : member.activity})
        for i,v in activities.items():
            if(v != None):
                if(not (i.bot)):
                    await channel.send(f'{i.name}: {v.name}')
    if('almonds' in content.lower() and author.bot == False):
        await channel.send(COPYPASTAS["almonds"])
    if('threaten' in content.lower() and author.bot == False):
        for member in message.mentions:
            if(member.dm_channel == None):
                await member.create_dm()
                await member.dm_channel.send(content=COPYPASTAS["seal"])
            else:
                await member.dm_channel.send(content=COPYPASTAS["seal"])
    if('oleg' in content.lower() and author.bot == False):
        await channel.send("Stop Playing Tarkov")
    if(content.lower().startswith('nuke') and author.bot == False):
        await channel.send('nuking...')
        await countdown(10, nuke, channel)


client.run(TOKEN)