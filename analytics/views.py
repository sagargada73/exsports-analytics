from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image
from io import BytesIO
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as mlt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
from subprocess import check_output
from django.conf import settings
import os
mlt.style.use('fivethirtyeight')

def index(request):
    return render(request, 'dashboard.html', {})


def toss_graph(matches, delivery):
    df = matches.iloc[[matches['win_by_runs'].idxmax()]]
    mlt.subplots(figsize=(10,6))
    sns.countplot(x='season',hue='toss_decision',data=matches)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'toss_graph.png')
    plt.savefig(imageFile, format='png')
    plt.clf()

def toss_win_match_win(matches, delivery):
    df = matches[matches['toss_winner']==matches['winner']]
    slices = [len(df),(577-len(df))]
    labels = ['Yes','No']
    mlt.pie(slices,labels=labels,startangle=90,shadow=True,explode=(0,0.05),autopct='%1.1f%%',colors=['r','g'])
    fig = mlt.gcf()
    fig.set_size_inches(6,6)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats', 'ipl', 'toss_win_match_win.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def team1_vs_team2(team1,team2, matches):
    mt1 = matches[((matches['team1']==team1)|(matches['team2']==team1))&((matches['team1']==team2)|(matches['team2']==team2))]
    sns.countplot(x='season', hue='winner', data=mt1, palette='Set3')
    mlt.xticks(rotation='vertical')
    leg = mlt.legend( loc = 'upper center')
    fig=mlt.gcf()
    fig.set_size_inches(18,8)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'team1_team2.png')
    plt.savefig(imageFile, format='png')

def batting_bowling(delivery):
    high_scores=delivery.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index() 
    high_scores=high_scores[high_scores['total_runs']>=200]
    high_scores.nlargest(10,'total_runs')

    fig, ax = mlt.subplots(1,2)
    sns.countplot(high_scores['batting_team'],ax=ax[0])
    sns.countplot(high_scores['bowling_team'],ax=ax[1])
    mlt.xticks(rotation=90)
    fig=mlt.gcf()
    fig.set_size_inches(18,8)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'batting_bowling.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def team_chasing(delivery):
    high_scores=delivery.groupby(['match_id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()
    high_scores1=high_scores[high_scores['inning']==1]
    high_scores2=high_scores[high_scores['inning']==2]
    high_scores1=high_scores1.merge(high_scores2[['match_id','inning', 'total_runs']], on='match_id')
    high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_runs_x':'inning1_runs','total_runs_y':'inning2_runs'},inplace=True)
    high_scores1=high_scores1[high_scores1['inning1_runs']>=200]
    high_scores1['is_score_chased']=1
    high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs']<=high_scores1['inning2_runs'], 
                                            'yes', 'no')

    slices=high_scores1['is_score_chased'].value_counts().reset_index().is_score_chased
    labels=['target not chased','target chased']
    mlt.pie(slices,labels=labels,colors=['#1f2ff3', '#0fff00'],startangle=90,shadow=True,explode=(0,0.1),autopct='%1.1f%%')
    fig = mlt.gcf()
    fig.set_size_inches(6,6)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'team_chasing.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def top_batsmen(delivery):
    toppers=delivery.groupby(['batsman','batsman_runs'])['total_runs'].count().reset_index()
    toppers=toppers.pivot('batsman','batsman_runs','total_runs')
    fig,ax=mlt.subplots(2,2,figsize=(18,12))
    toppers[1].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[0,0],color='#45ff45',width=0.8)
    ax[0,0].set_title("Most 1's")
    ax[0,0].set_ylabel('')
    toppers[2].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[0,1],color='#df6dfd',width=0.8)
    ax[0,1].set_title("Most 2's")
    ax[0,1].set_ylabel('')
    toppers[4].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[1,0],color='#fbca5f',width=0.8)
    ax[1,0].set_title("Most 4's")
    ax[1,0].set_ylabel('')
    toppers[6].sort_values(ascending=False)[:5].plot(kind='barh',ax=ax[1,1],color='#ffff00',width=0.8)
    ax[1,1].set_title("Most 6's")
    ax[1,1].set_ylabel('')
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'top_batsmen.png')
    plt.savefig(imageFile, format='png')
    fig.clf()

def top_batsmen_score(matches, delivery):
    max_runs=delivery.groupby(['batsman'])['batsman_runs'].sum()
    batsmen = matches[['id','season']].merge(delivery, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
    a=batsmen.groupby(['batsman','batsman_runs'])['total_runs'].count().reset_index()
    b=max_runs.sort_values(ascending=False)[:10].reset_index()
    c=b.merge(a,left_on='batsman',right_on='batsman',how='left')
    c.drop('batsman_runs_x',axis=1,inplace=True)
    c.set_index('batsman',inplace=True)
    c.columns=['type','count']
    c=c[(c['type']==1)|(c['type']==2)|(c['type']==4)|(c['type']==6)]
    cols=['type','count']
    c.reset_index(inplace=True)
    c=c.pivot('batsman','type','count')

    trace1 = go.Bar(
        y=c.index, x=c[6],
        name="6's",
        orientation = 'h',
        marker = dict(color = 'rgba(178, 78, 139, 0.6)',
            line = dict(color = 'rgba(178, 78, 139, 1.0)',
                width = 3)
        )
    )
    trace2 = go.Bar(
        y=c.index, x=c[4],
        name="4's",
        orientation = 'h',
        marker = dict(color = 'rgba(58, 71, 80, 0.6)',
            line = dict(color = 'rgba(58, 71, 80, 1.0)',
                width = 3)
        )
    )

    trace3 = go.Bar(
        y=c.index, x=c[2],
        name="2's",
        orientation = 'h',
        marker = dict(color = 'rgba(101, 178, 139, 0.6)',
            line = dict(color = 'rgba(101, 178, 139, 1.0)',
                width = 3)
        )
    )
    trace4 = go.Bar(
        y=c.index, x=c[1],
        name="1's",
        orientation = 'h',
        marker = dict(color = 'rgba(208, 105, 80, 0.6)',
            line = dict(color = 'rgba(208, 105, 80, 1.0)',
                width = 3)
        )
    )

    data = [trace1, trace2,trace3,trace4]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    imageFile = os.path.join(settings.BASE_DIR, 'static', 'stats' , 'ipl', 'top_batsmen_score.png')
    fig.write_image(imageFile)
    

def ipl_index(request):
    matches_data = os.path.join(settings.BASE_DIR, 'data', 'matches.csv')
    deliveries_data = os.path.join(settings.BASE_DIR, 'data', 'deliveries.csv')

    matches = pd.read_csv(matches_data)   
    delivery = pd.read_csv(deliveries_data)

    matches.drop(['umpire3'], axis=1, inplace=True)
    delivery.fillna(0,inplace=True)

    matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)

    delivery.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)
    
    # toss_win_match_win(matches, delivery)
    toss_graph(matches, delivery)
    batting_bowling(delivery)
    team_chasing(delivery)
    top_batsmen(delivery)
    # top_batsmen_score(matches, delivery)

    teams =  ['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS']

    context_data = {
        'teams' : teams
    }

    return render(request, 'ipl/dashboard.html', context_data)


def setTeam(request):
    if request.method == 'POST':
        team = request.POST.get('team')
        context_data = {
            'team_name': team
        }
        return render(request, 'dashboard.html', context_data)

def get_teams_stats(request):

    team1 = request.POST.get('team1')
    team2 = request.POST.get('team2')

    matches_data = os.path.join(settings.BASE_DIR, 'data', 'matches.csv')
    deliveries_data = os.path.join(settings.BASE_DIR, 'data', 'deliveries.csv')

    matches = pd.read_csv(matches_data)   
    delivery = pd.read_csv(deliveries_data)

    matches.drop(['umpire3'], axis=1, inplace=True)
    delivery.fillna(0,inplace=True)

    matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)

    delivery.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)
    
    team1_vs_team2(team1,team2, matches)

    return HttpResponseRedirect('/ipl/')
    