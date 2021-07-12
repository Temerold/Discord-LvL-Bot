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


loggers_emoji = "<:loggers:860219204828528671>"


def neededXpToLvlUp(lvl, rebirths):
    return round((0.5 * (lvl ** 2) + lvl * 2) * 25 + (rebirths ** 1.1))


def neededLvlsForRebirth(rebirths):
    return round(rebirths ** 0.8) + 5


def rebirthBonus(rebirths):
    return round(rebirths ** 1.2)


def xpEarnings(rebirths):
    return round((randint(5, 20) + rebirthBonus(rebirths)))


@bot.command()
async def level(ctx):
    userID = str(ctx.message.author.id)

    with open("data.json", "r") as file:
        data = json.load(file)

    lvl = data[userID]["lvl"]
    xp = data[userID]["xp"]
    rebirths = data[userID]["rebirths"]

    await ctx.send(
        f"""{ctx.message.author.mention}, dina stats lyder som följande:
    LvL: {lvl}
    XP: {xp}/{neededXpToLvlUp(lvl, rebirths)}
    Rebirths: {rebirths}
    
    Rebirth-bonus: +{rebirthBonus(rebirths)} XP/msg"""
    )


@bot.command()
async def rebirth(ctx):
    userID = str(ctx.message.author.id)

    with open("data.json", "r+") as file:
        data = json.load(file)
        lvl = data[str(userID)]["lvl"]
        rebirths = data[str(userID)]["rebirths"]

        if lvl >= neededLvlsForRebirth(rebirths):
            data[userID]["lvl"] = 1
            data[userID]["xp"] = 0
            data[userID]["rebirths"] += 1
            # Resets level and XP but adds one rebirth

            rebirths = data[userID]["rebirths"]
            # Defines the amount of rebirths as a varible, to send and
            # print it later.

            file.seek(0)
            # Sometimes, `json.dump` dumps at the end of the file.
            # `file.seek(0)` assures that `json.dump()` overwrites the
            # file, starting at the beginning.

            json.dump(data, file, indent=4)

            file.truncate()
            # Removes the rest of the file, even if there isn't any.
            # This is needed if `json.dump` doesn't overwrite the file,
            # and instead jsut writes new content before it. If so, the
            # old content gets removed.

            rebirths = data[userID]["rebirths"]

            await ctx.channel.send(
                f"Oh lärkar, {ctx.message.author.mention}! Du rebirthar. Fine."
                + " Det är helt okej, så länge du inte blandar in mig... "
                + "Förstått? I vilket fall som helst så har du nu följande ..."
                + f" typ bonuses (eller nåt sånt):\n    "
                + f"+{rebirthBonus(rebirths)} XP per meddelande"
            )

            for lvl in range(lvl + 1):
                try:
                    await removeRole(userID, ("LvL " + str(lvl + 1)))
                except:
                    pass
            # Removes the level-earned roles from the user, testing
            # all possible roles they could have (1->lvl + 1).

            if rebirths == 1:

                grammarCase = "Rebirth"
            # In the case that this' the user's first rebirth, for the
            # string to be grammatically correct, `grammarCase` gets
            # defined as a singular "Rebirth".

            else:
                grammarCase = "Rebirths"
                # `GrammarCase` gets defines as a plural

            try:
                await addRole(userID, f"{rebirths} {grammarCase}")
            except:
                pass

        else:
            if neededLvlsForRebirth(rebirths) - lvl == 1:
                # In the case that there's only level left, for the
                # string to be grammatically correct, `grammarCase` gets
                # defined as a singular "level".

                grammarCase = "level"  # "Level" in Swedish

            else:
                grammarCase = "levlar"  # "Levels" in Swedish
                # `GrammarCase` gets defines as a plural

            if userID == 410123402196811806:
                # Me, the creator - Temerold. Instead of giving me an
                # attitude, it treats me with respect. Since I'm its creator.

                await ctx.channel.send(
                    f"Wow! {ctx.message.author.mention}, chilla! Jag vet att "
                    + "du äger stället, och att det är dina regler som gäller "
                    + f"här, men du är i level {lvl}. Du behöver komma upp i "
                    + f"minst {neededLvlsForRebirth(rebirths)} levlar. Du har"
                    + f" alltså {neededLvlsForRebirth(rebirths) - lvl} "
                    + f"{grammarCase} kvar."
                )

            else:
                await ctx.channel.send(
                    f"Wow! {ctx.message.author.mention}, chilla! Kom inte in "
                    + "som om du äger stället. Mina regler gäller här, och du "
                    + f"är i level {lvl}. Du behöver komma upp i, *minst*, "
                    + f"{neededLvlsForRebirth(rebirths)} levlar. Du har alltså"
                    + f" {neededLvlsForRebirth(rebirths) - lvl} {grammarCase} "
                    + "kvar. Kom igen, din lata ek!"
                )
                # **An attitide**


@bot.event
async def on_message(message):
    if str(message.author) != "penid#6678" and randint(1, 1) == 1:
        userID = str(message.author.id)

        with open("data.json", "r") as file:
            data = json.load(file)

        if userID not in data:
            print("Added: " + userID)

            data[userID] = {"lvl": 1, "xp": 0, "rebirths": 0}
            # Creates new user with one level, zero XP, and zero rebirths

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

        await addXP(userID)
        await levelUp(userID)

        await bot.process_commands(message)


async def addXP(userID):
    with open("data.json", "r") as file:
        data = json.load(file)

    data[userID]["xp"] += xpEarnings(data[userID]["rebirths"])
    # Adds xpEarnings XP to the user

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


async def levelUp(userID):
    global loggers_emoji

    with open("data.json", "r+") as file:
        data = json.load(file)

    lvl = data[userID]["lvl"]
    xp = data[userID]["xp"]
    rebirths = data[userID]["rebirths"]

    if xp >= neededXpToLvlUp(lvl, rebirths):
        data[userID]["lvl"] += 1
        data[userID]["xp"] = 0

        with open("data.json", "w") as file2:
            json.dump(data, file2, indent=4)

        await bot.get_channel(727588975681863731).send(
            f"Loggers! {loggers_emoji} <@{userID}> kom upp i **level "
            + f"{lvl + 1}**! "
            + (f"{loggers_emoji} ") * 6
        )
        print(f"{userID} kom upp i level {lvl + 1}")

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


bot.run(token)
