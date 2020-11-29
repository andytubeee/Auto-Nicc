import os
import uuid
import random
import pandas as pd
import readCSV

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def checkRole(roleName, roleCollection):
    for rc in roleCollection:
        if roleName == rc.name:
            return True
    return False


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} is connected to the following guild: \n'
          f'{guild.name} (id: {guild.id}) \n')


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
        softwareMem = set()
        desMem = set()
        generalMembers = set()

        teams = []

        totalMembers = 0
        geeks = 0
        creativeppl = 0
        generalppl = 0

        for guild in client.guilds:
            for member in guild.members:
                softwareBool = checkRole('Software', member.roles)
                designBool = checkRole('Designer', member.roles)
                memberBool = checkRole('Member', member.roles)
                teacherBool = checkRole('Teacher', member.roles)
                genBool = not (softwareBool or designBool)

                for role in member.roles:
                    if role.name == "Member":
                        if genBool:
                            generalMembers.add(member.display_name)
                        totalMembers += 1
                        members.append(member.display_name)
                    if role.name == "Software":
                        geeks += 1
                        softwareMem.add(member.display_name)
                    if role.name == "Designer":
                        creativeppl += 1
                        desMem.add(member.display_name)

                    generalppl = totalMembers - (creativeppl + geeks)

        print(f"Available members: {members}")
        print(f"Software members: {softwareMem}")
        print(f"Design members: {desMem}")
        print(f"General members: {generalMembers}")


        # Team assign prep

        await msg.channel.send(
            f"We currently have a total of {totalMembers} members. That is, {generalppl} "
            f"general participants, {geeks} geeks, and {creativeppl} creative people onboard.")

        for i in range(totalMembers // 4):
            team = random.sample(members, 4)
            for t in team:
                members.remove(t)
            teams.append(team)

        # print(len(members))

        if len(members) == 3:
            teams.append([members[0], members[1], members[2]])

        elif len(members) == 1:
            t1 = teams[0]
            m1 = t1.pop(random.randrange(len(t1)))
            t2 = teams[1]
            m2 = t2.pop(random.randrange(len(t1)))

            teams.append([members[0], m1, m2])
        elif len(members) == 2:
            t1 = teams[0]
            m1 = t1.pop(random.randrange(len(t1)))

            teams.append([members[0], members[1], m1])

        teamsDict = dict()
        for i, t in enumerate(teams):
            teamsDict[f"Team {i + 1}"] = t

        # print("\nTeams:\n")
        # print(teamsDict)

        # print(teamsDF.head())
        print("\n\nOld Teams: \n")
        print(readCSV.getOldTeams())
        print('\n')

        # Save teams to CSV

        try:
            teamsDF = pd.DataFrame.from_dict(teamsDict, orient='index')
            teamsDF.to_csv('Teams.csv', na_rep='-', index=False, header=False)
            print("Saved to Teams.csv")
        except:
            print("Error!")


# Activate bot
client.run(TOKEN)
