import cricpy.analytics as ca
import re, time
import os

from django.conf import settings
path = os.path.join(settings.BASE_DIR, 'static', 'stats', 'individual')


def get_id(player):
    id = 0
    query = "espn cricinfo " + player
    try:
        from googlesearch import search
    except ImportError:
        print("No module named google found.")
    for j in search(query, tld="com", num=1, stop=1, pause=2):
        id = int((re.findall(r'[0-9]+', j))[0])
    return id

def fetch_data(player, id, type):
    player = ca.getPlayerData(id, dir=path, file=str(id) + ".csv", type=type, homeOrAway=[1, 2], result=[1, 2, 4])
    return player

def battingPerf3d(player, id):
    plt = ca.battingPerf3d(os.path.join(path, str(id) + ".csv"), player)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'individual', 'battingPerf3d.png')
    plt.savefig(imageFile, format='png')
    plt.close()

def batsmanAvgRunsGround(player, id):
    plt = ca.batsmanAvgRunsGround(os.path.join(path, str(id) + ".csv"), player)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'individual', 'batsmanAvgRunsGround.png')
    plt.savefig(imageFile, format='png')
    plt.close()

def batsmanRunsLikelihood(player, id):
    plt = ca.batsmanRunsLikelihood(os.path.join(path, str(id) + ".csv"), player)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'individual', 'batsmanRunsLikelihood.png')
    plt.savefig(imageFile, format='png')
    plt.close()

def batsmanAvgRunsOpposition(player, id):
    plt = ca.batsmanAvgRunsOpposition(os.path.join(path, str(id) + ".csv"), player)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'individual', 'batsmanAvgRunsOpposition.png')
    plt.savefig(imageFile, format='png')
    plt.close()