import cricpy.analytics as ca
import re, time
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path = os.path.join(BASE_DIR, 'scripts', 'player_data')
players = ['dhawan', 'rohit', 'kl_rahul', 'kohli', 'iyer', 'pandey', 'jadeja', 'shaw', 'gill', 'shami', 'chahal',
           'kuldeep', 'bumrah', 'saini', 'chahar', 'jadhav', 'dube', 'shardul', 'sundar', 'rahane']
player_names = {'dhawan': 'Shikhar Dhawan'}
# TODO: Fetch player names from Cricinfo <title>, store in a dictionary such that it's of the format {players[i]: fetched_name} and use it to show player's name in charts.
ids = {}
data = {}


def get_id(players):
    if len(players) == 1:
        query = "espn cricinfo " + i
        try:
            from googlesearch import search
        except ImportError:
            print("No module named google found.")
        for j in search(query, tld="com", num=1, stop=1, pause=2):
            ids[i] = int((re.findall(r'[0-9]+', j))[0])
            print(ids[i])
    else:
        for i in players:
            query = "espn cricinfo " + i
            try:
                from googlesearch import search
            except ImportError:
                print("No module named google found.")
            for j in search(query, tld="com", num=1, stop=1, pause=2):
                ids[i] = int((re.findall(r'[0-9]+', j))[0])
                print(ids[i])
        return ids




# get_id(players)
# fetch_data('Shikhar Dhawan', ids)


def batsmanRunsFreqPerf(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanRunsFreqPerf(path + k + ".csv", player)


def batsmanMeanStrikeRate(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanMeanStrikeRate(path + k + ".csv", player)


def batsmanRunsRanges(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanRunsRanges(path + k + ".csv", player)


# TEST
def batsman4s(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsman4s(path + k + ".csv", player)


def batsman6s(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsman6s(path + k + ".csv", player)


def batsmanDismissals(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanDismissals(path + k + ".csv", player)


def battingPerf3d(player):
    for k, v in player_names.items():
        if v == player:
            ca.battingPerf3d(path + k + ".csv", player)


def batsmanAvgRunsGround(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanAvgRunsGround(path + k + ".csv", player)


def batsmanAvgRunsOpposition(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanAvgRunsOpposition(path + k + ".csv", player)


def batsmanRunsLikelihood(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanRunsLikelihood(path + k + ".csv", player)


def batsmanPerfBoxHist(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanPerfBoxHist(path + k + ".csv", player)


def batsmanPerfHomeAway(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanPerfHomeAway(path + k + ".csv", player)


def batsmanMovingAverage(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanAvgRunsGround(path + k + ".csv", player)


def batsmanCumulativeAverageRuns(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanCumulativeAverageRuns(path + k + ".csv", player)


def batsmanCumulativeStrikeRate(player):
    for k, v in player_names.items():
        if v == player:
            ca.batsmanCumulativeStrikeRate(path + k + ".csv", player)


def batsmanPerfForecast(player):
    for k, v in player_names.items():

        input()
        if v == player:
            ca.batsmanPerfForecast(path + k + ".csv", player)



# WORKING
# batsmanRunsFreqPerf('Shikhar Dhawan')
# batsmanMeanStrikeRate('Shikhar Dhawan')
# batsmanRunsRanges('Shikhar Dhawan')
# batsman6s('Shikhar Dhawan')
# batsmanDismissals('Shikhar Dhawan')
# battingPerf3d('Shikhar Dhawan')
# batsmanAvgRunsGround('Shikhar Dhawan')
# batsmanAvgRunsOpposition('Shikhar Dhawan')
# batsmanRunsLikelihood('Shikhar Dhawan')
# batsmanPerfBoxHist('Shikhar Dhawan')
# batsmanMovingAverage('Shikhar Dhawan')
# batsmanCumulativeAverageRuns('Shikhar Dhawan')
# batsmanCumulativeStrikeRate('Shikhar Dhawan')
# batsmanPerfForecast('Shikhar Dhawan')