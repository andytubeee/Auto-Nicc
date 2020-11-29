import csv


def getOldTeams():
    with open('teams.csv', mode='r', encoding='utf-8') as f:
        readCSV = csv.reader(f, delimiter=',')
        teams = dict()
        for i, row in enumerate(readCSV):

            # Delete hyphen which represents empty team member
            if '-' in row:
                row.remove('-')

            teams[f"Team {i + 1}"] = row

        return teams
