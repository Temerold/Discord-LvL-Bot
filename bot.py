import time
import discord
from discord.ext import commands
import random
from auth import *
from random import randint
import json


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    global guild

    guild = bot.get_guild(727588974658322442)


# Globals and redefinition


def neededXpToLvlUp(lvl, rebirths):
    return round((0.5 * (lvl ** 2) + lvl * 2) * 25 + (rebirths ** 1.1))


def neededLvlsForRebirth(rebirths):
    return round(rebirths ** 0.4) + 5


def rebirthBonus(rebirths):
    return round(rebirths ** 1.25)


def xpAdded(rebirths, boosts):
    return round((randint(5, 20) + rebirthBonus(rebirths)) * boosts)


@bot.command()
async def level(ctx):
    userID = ctx.message.author.id

    with open("data.json", "r") as file:
        data = json.load(file)
        lvl = data[str(userID)]["lvl"]
        xp = data[str(userID)]["xp"]
        rebirths = data[str(userID)]["rebirths"]

    await ctx.send(
        f"""{ctx.message.author.mention}, dina stats lyder som följande:
    LvL: {lvl}
    XP: {xp}/{neededXpToLvlUp(lvl, rebirths)}
    Rebirths: {rebirths}
    
    Rebirth-bonus: +{rebirthBonus(rebirths)} XP/msg"""
    )


@bot.command()
async def rebirth(ctx):
    userID = ctx.message.author.id
    with open("data.json", "r+") as file:
        data = json.load(file)
        lvl = data[str(userID)]["lvl"]

        lvl = data[str(userID)]["lvl"]
        rebirths = data[str(userID)]["rebirths"]

        channel = bot.get_channel(727588975681863731)

        if lvl >= neededLvlsForRebirth(rebirths):
            data[str(userID)]["lvl"] = 1
            data[str(userID)]["xp"] = 0
            data[str(userID)]["rebirths"] += 1

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

            rebirths = data[str(userID)]["rebirths"]

            await ctx.channel.send(
                f"Oh lärkar, {ctx.message.author.mention}! Du rebirthar. Fine."
                + " Det är helt okej, så länge du inte blandar in mig. "
                + "Förstått? I vilket fall som helst så har du nu följande ..."
                + f" typ bonuses (eller nåt sånt):\n    "
                + f"+{rebirthBonus(rebirths)} XP per meddelande"
            )

            for lvl in range(lvl + 1):
                try:
                    await removeRole(userID, ("LvL " + str(lvl + 1)))
                except:
                    pass

            if rebirths == 1:
                grammarCase = " Rebirth"
            else:
                grammarCase = " Rebirths"

            try:
                await addRole(userID, (str(rebirths) + grammarCase))
            except:
                pass

        else:
            if neededLvlsForRebirth(rebirths) - lvl == 1:
                grammarCase = "level"
            else:
                grammarCase = "levlar"

            if userID == 410123402196811806:
                await channel.send(
                    f"Wow! {ctx.message.author.mention}, chilla! Jag vet att "
                    + "du äger stället, och att det är dina regler som gäller "
                    + f"här, men du är i level {lvl}. Du behöver komma upp i "
                    + f"minst {neededLvlsForRebirth(rebirths)} levlar. Du har"
                    + f" alltså {neededLvlsForRebirth(rebirths) - lvl} "
                    + f"{grammarCase} kvar."
                )

            else:
                await channel.send(
                    f"Wow! {ctx.message.author.mention}, chilla! Kom inte in "
                    + "som om du äger stället. Mina regler gäller här, och du "
                    + f"är i level {lvl}. Du behöver komma upp i, *minst*, "
                    + f"{neededLvlsForRebirth(rebirths)} levlar. Du har alltså"
                    + f" {neededLvlsForRebirth(rebirths) - lvl} {grammarCase} "
                    + "kvar. Kom igen, din lata ek!"
                )


@bot.event
async def on_message(message):
    global member

    if str(message.author) != "penid#7202" and randint(1, 1) == 1:
        member = message.author

        userID = str(message.author.id)

        with open("data.json", "r") as file:
            data = json.load(file)

        if userID not in data:
            print("Added: " + userID)
            data[str(userID)] = {"lvl": 1, "xp": 0, "rebirths": 0, "boosts": 1}
            file = open("data.json", "w")
            json.dump(data, file, indent=4)
            file.close()

        await addXP(userID)
        await levelUp(userID)

        await bot.process_commands(message)


async def addXP(userID):
    with open("data.json", "r") as file:
        data = json.load(file)

    lvl = data[userID]["lvl"]
    xp = data[userID]["xp"]
    rebirths = data[userID]["rebirths"]
    boosts = data[str(userID)]["boosts"]

    data[str(userID)]["xp"] += xpAdded(rebirths, boosts)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


async def levelUp(userID):
    with open("data.json", "r+") as file:
        data = json.load(file)
        lvl = data[str(userID)]["lvl"]
        xp = data[str(userID)]["xp"]
        rebirths = data[str(userID)]["rebirths"]

        if xp >= neededXpToLvlUp(lvl, rebirths):
            channel = bot.get_channel(727588975681863731)

            data[str(userID)]["lvl"] += 1
            data[str(userID)]["xp"] = 0
            lvl = data[str(userID)]["lvl"]

            with open("data.json", "w") as file2:
                json.dump(data, file2, indent=4)

            loggers_emoji = "<:loggers:860219204828528671>"

            await channel.send(
                f"Loggers! {loggers_emoji} <@{userID}> kom upp i **level "
                + f"{lvl}**! "
                + (f"{loggers_emoji} ") * 6
            )
            print(f"{userID} kom upp i level {lvl}")

            try:
                await addRole(userID, ("LvL " + str(lvl)))
            except:
                pass


async def addRole(userID, role):
    global guild

    for member in guild.members:
        if int(member.id) == int(userID):
            await member.add_roles(discord.utils.get(guild.roles, name=role))


async def removeRole(userID, role):
    global guild

    for member in guild.members:
        if int(member.id) == int(userID):
            await member.remove_roles(discord.utils.get(guild.roles, name=role))


def howManyMessagesUntil(rebirths=0, lvls=0, rebirthsAlready=0, LvlsAlready=0):
    messages = 0
    averageXP = 12.5

    for rbrt in range(rebirths - rebirthsAlready):
        for lvl in range(neededLvlsForRebirth(rbrt) - LvlsAlready):
            messages += neededXpToLvlUp((lvl + LvlsAlready), rbrt) / averageXP

        averageXP += round((rbrt + rebirthsAlready) ** 1.1)

    if rebirths == 0:
        rbrt = 0

    for lvl in range(lvls - LvlsAlready):
        messages += neededXpToLvlUp((lvl + LvlsAlready + 1), rbrt) / averageXP

    return round(messages)


bot.run(token)
