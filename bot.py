import os
import uuid
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} is connected to the following guild: \n'
          f'{guild.name} (id: {guild.id})')


@client.event
async def on_message(msg):
    message = msg.content

    if message == "*changenickall":
        for guild in client.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.name == "Member":
                        await member.edit(nick=str(uuid.uuid1()).split("-")[0])
        await msg.channel.send("Successfully generated random nicknames for everyone.")



    elif message == "*deletenick":
        for guild in client.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.name == "Member":
                        await member.edit(nick=None)
        await msg.channel.send("Successfully removed everyone's nickname.")



    elif message == "*assignteams":
        members = []
        softwareMem = []
        desMem = []

        totalMembers = 0
        geeks = 0
        creativeppl = 0
        generalppl = 0

        for guild in client.guilds:
            for member in guild.members:
                for role in member.roles:
                    if role.name == "Member":
                        totalMembers += 1
                        members.append(member.display_name)
                    if role.name == "Software":
                        geeks += 1
                        softwareMem.append(member.display_name)
                    if role.name == "Designer":
                        creativeppl += 1
                        desMem.append(member.display_name)

                    generalppl = totalMembers - (creativeppl + geeks)

        print(f"Available members: {members}")
        print(f"Software members: {softwareMem}")
        print(f"Design members: {desMem}")

        print("\nTeams:\n")

        # Team assign prep

        await msg.channel.send(
            f"We currently have a total of {totalMembers} members. That is, {generalppl} "
            f"general participants, {geeks} geeks, and {creativeppl} creative people onboard.")

        if int(totalMembers % 4) == 0:

            # Teams of 4

            await msg.channel.send(f"We can try {int(totalMembers / 4)} teams of 4 (Full team).")

            teams = [random.sample(members, 4) for _ in range(int(totalMembers / 4))]
            await msg.channel.send("The teams are:")
            for t in teams:
                await msg.channel.send("; ".join(t))

        if int(totalMembers % 4) == 3:
            await msg.channel.send(
                f"We can try {int(totalMembers / 4)} teams of 4 (Full team), and a team of "
                f"{int(totalMembers % 4)} people.")

            teams = [random.sample(members, 4) for _ in range(int(totalMembers // 4))] + \
                    [random.sample(members, 3)]

            print(teams)

        elif 1 <= int(totalMembers % 4) <= 2 and int(totalMembers % 4) != 0:
            # Two people shouldn't be on team
            await msg.channel.send(
                f"We can try {int(totalMembers / 3)} teams of 3 (Full team), and a team of "
                f"{int(totalMembers % 3)} people.")

        teams = [random.sample(members, 3) for _ in range(int(totalMembers // 3))] + \
                [random.sample(members, int(totalMembers % 3))]

        print(teams)


# Activate bot
client.run(TOKEN)
