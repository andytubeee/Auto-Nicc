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


def saveCSV(dictionay, file_name):
    try:
        teamsDF = pd.DataFrame.from_dict(dictionay, orient='index')
        teamsDF.to_csv(file_name, na_rep='-', index=False, header=False)
        print(f"Saved as {file_name}")
    except:
        print("Error!")

def checkExpertise(team, allSoftware, allDesign):
    numSoftware = 0
    numDesign = 0
    for t in team:
        if t in allSoftware:
            numSoftware += 1
        if t in allDesign:
            numDesign += 1

    return numSoftware, numDesign

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

        oldTeams = readCSV.getOldTeams()

        # print(teamsDF.head())
        print("\n\nOld Teams: \n")
        print(readCSV.getOldTeams())
        print('\n')

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
        print(f"Beginners: {generalMembers}")


        # Team assign prep

        await msg.channel.send(
            f"We currently have a total of {totalMembers} members. That is, {generalppl} "
            f"general participants, {geeks} geeks, and {creativeppl} creative people onboard.")

        for i in range(totalMembers // 4):
            originalTeam = random.sample(members, 4)
            for t in originalTeam:
                members.remove(t)
            teams.append(originalTeam)

        # Team balance out by number
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

        for originalTeam in teams:
            # print("\nBefore:")
            # print(team)
            sMember, dMember = checkExpertise(originalTeam, softwareMem, desMem)
            # print(sMember, dMember)
            if sMember == 0:
                # print('Got in sMember = 0 (Original team)')
                foundReplacement = False
                for team1 in teams:
                    if team1 != originalTeam:
                        # print('Got in team1 not the same team')
                        sMember1, dMember1 = checkExpertise(team1, softwareMem, desMem)
                        if sMember1 >= 2:
                            # print('Got in sMember >= 2')
                            for member in team1:
                                if member in softwareMem:
                                    # print('Got in member in softwareMem')
                                    if dMember1 >= 2 or member not in desMem:
                                        # print('Got in dMember1 >= 2')
                                        team1.remove(member)
                                        originalTeam.append(member)

                                        team1.append(originalTeam[0])
                                        originalTeam.remove(originalTeam[0])
                                        foundReplacement = True
                                        break

                    if foundReplacement:
                        break

            if dMember == 0:
                # print('Got in sMember = 0 (Original team)')
                foundReplacement = False
                for team1 in teams:
                    if team1 != originalTeam:
                        # print('Got in team1 not the same team')
                        sMember1, dMember1 = checkExpertise(team1, softwareMem, desMem)
                        if dMember1 >= 2:
                            # print('Got in sMember >= 2')
                            for member in team1:
                                if member in desMem:
                                    # print('Got in member in softwareMem')
                                    if sMember1 >= 2 or member not in softwareMem:
                                        for originalMember in originalTeam:
                                            if sMember >= 2 or originalMember not in softwareMem:
                                                # print('Got in dMember1 >= 2')
                                                team1.remove(member)
                                                originalTeam.append(member)

                                                team1.append(originalMember)
                                                originalTeam.remove(originalMember)
                                                foundReplacement = True
                                                break

                                if foundReplacement:
                                    break

                    if foundReplacement:
                        break

        tempMem = []
        for team in teams:
            for member in team:
                if member in tempMem:
                    print('Found duplicates')
                tempMem.append(member)

        print(len(tempMem), len(members))

        for t in teams:
            print(t)
            sMember, dMember = checkExpertise(t, softwareMem, desMem)
            print(sMember, dMember)

        # Prepare saving
        teamsDict = dict()
        for i, t in enumerate(teams):
            teamsDict[f"Team {i + 1}"] = t

        # Save teams to CSV
        saveCSV(teamsDict, 'teams.csv')

        for t in teams:
            await msg.channel.send(t)


# Activate bot
client.run(TOKEN)
