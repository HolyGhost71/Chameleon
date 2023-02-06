import asyncio
import discord
from discord.ext import commands
from config import *
from datetime import datetime
import random
import json

bot = commands.Bot(command_prefix=PREFIX, description="Chameleon Bot")

@bot.event
async def on_ready():
    print("Bot is online")

@bot.command(pass_context=True)
async def chameleon(ctx):

    embeded = discord.Embed(
        title="Chameleon",
        description="Welcome to the game Chameleon.\nWhen everyone has reacted by pressing the ✅, press the 🦎 button to begin",
        url="https://bigpotato.co.uk/products/the-chameleon",
        colour=0x03fc90,
        timestamp=datetime.now()
    )

    players = []

    await ctx.channel.purge(limit=1)
    msg = await ctx.send(embed=embeded)
    
    await msg.add_reaction('✅')
    await msg.add_reaction('🦎')

    def check(reaction, user):
        return user != bot.user and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '🦎')

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=120.0, check=check)
        except asyncio.TimeoutError:
            break

        if str(reaction.emoji) == '🦎' and ctx.author == user and len(players) > 0:
            await LoadChameleon(ctx, bot, players, msg)
            return
        elif str(reaction.emoji) == '✅':
            if user not in players:
                players.append(user)

async def LoadChameleon(ctx, bot, players, msg):

    file = open("cards.json")
    cards = json.load(file)
    card = random.choice(cards)

    heading = card["Heading"]
    options = card["List"]
    random.shuffle(options)

    random.shuffle(players)
    firstPerson = random.choice(players)
    cham = players.pop()
    square = random.choice(options)

    working = True
    try:
        await cham.send("You are the chameleon")
    except discord.Forbidden:
        await msg.delete()
        await ctx.send(f"Cannot send a DM to {cham.name} because they have their DMs closed.\nPlease open your DMs by going to User Settings -> Privacy & Safety -> Allow direct messages from server members and making sure it is turned on.")
        working = False
        
    for p in players:
        try:
            await p.send(square)
        except discord.Forbidden:
            await msg.delete()
            await ctx.send(f"Cannot send a DM to {cham.name} because they have their DMs closed.\nPlease open your DMs by going to User Settings -> Privacy & Safety -> Allow direct messages from server members and making sure it is turned on.")
            working = False
            
    if not working: return
    
    players = []
            
    embeded = discord.Embed(
		title=(f"Chameleon - Topic: {heading}"),
        description=(f"You will all be sent the same word that belongs to this topic. One person will be the Chameleon. They will not know the word.\n\nTake it in turns to say a word to let the other players know that you are in on the secret. Chameleon, try to blend in.\n\nWhen you are ready, vote for who you think the Chameleon is. If you are correct, they get one last chance to guess the word and win the game, so keep it secret 🤫.\n\nFirst Person: {firstPerson.name}"),
        colour=0x03fc90,
        timestamp=datetime.now()
    )

    await msg.delete()
    msg = await ctx.send(embed=embeded)

    await msg.add_reaction('❌')

    def check(reaction, user):
        return user != bot.user and (str(reaction.emoji) == '❌')

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=600.0, check=check)
    except asyncio.TimeoutError:
        await msg.delete()
        

    if str(reaction.emoji) == '❌' and ctx.author == user:
        await msg.delete()
        embeded = discord.Embed(
            title=(f"Chameleon - Topic: {heading}"),
            description=(f"{options[0]} | {options[1]} | {options[2]} | {options[3]}\n{options[4]} | {options[5]} | {options[6]} | {options[7]}\n{options[8]} | {options[9]} | {options[10]} | {options[11]}\n{options[12]} | {options[13]} | {options[14]} | {options[15]}"),
            colour=0x03fc90,
            timestamp=datetime.now()
        )
        msg = await ctx.send(embed=embeded)
        
    return

bot.run(TOKEN, bot=True, reconnect=True)