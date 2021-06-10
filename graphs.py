# This script is intended to make several figures, each containing mutiple graphs
# to show relationships and trends that support the idea that the addition of the 
# three pointer changed the nba and made games less exciting to watch.


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import scipy.stats as stats

# read in data from csv files
players = pd.read_csv('data/Players.csv')
season_stats = pd.read_csv('data/Seasons_Stats.csv')
player_data = pd.read_csv('data/player_data.csv')

# create a dictionary of matching column names and explanations
names = ['ID','Year','Player','Position', 'Age','Team','Games', 'Games Started',
         'Minutes Played','Player Efficiency Rating','True Shooting Percentage',
        '3 Point Attempts','Free Throws','Offensive Rebound Percentage','Defensive Rebound Percentage',
        'Total Rebounds Percentage','Assists','Steal Percentage','Block Percentage',
         'Turnover Percentage', 'Usage Percentage','blanl','Offensive Win Shares','Defensive Win Shares',
        'Win Shares','Win Share per 48 Minutes','blank2','Offensive Box Plus/Minus','Defensive Box Plus/Minus',
        'Box Plus/Minus','Value Over Replacement Player','Field Goals','Field Goal Attempts','Field Goal Percentage',
        'Three Pointers','Three Point Attempts','Three Point Percentage','Two Pointers','Two Pointer Attempts',
        'Two Pointer Percentage','Effective Field Goal Percentage','Free Throws','Free Throw Attempts',
        'Free Throw Percentage','Offensive Rebounds','Defensive Rebounds','Total Rebounds','Assists',
        'Steals','Blocks','Turnovers','Personal Fouls','Points']
codes = {}
for key, val in zip(season_stats.columns, names):
    codes[key] = val



# plots mean statistics from the selection of columns over the years in the dataset
selection = ['Year', '2PA','3PA',
         'FGA', 'FG%', 'FTA', 'PF','AST','TS%']
selected_season_stats_by_year= season_stats[selection].groupby('Year').mean()
fig, axs = plt.subplots(4,2, figsize=(15, 12))
for stat, ax in zip(selection[1:], axs.flatten()):
    # basic plot
    ax.plot(range(68), selected_season_stats_by_year[stat])
    
    # titles and labels
    ax.set_title(f'{codes[stat]} By Year 1950-2017')
    ax.set_xlabel('Year')
    ax.set_ylabel(f'{codes[stat]}')
    ax.set_xticks(range(0,70, 10))
    ax.set_xticklabels(range(1950,2018, 10), rotation=45)
    
    # vertical lines at key points in time
    ax.axvline(30, linestyle='--',alpha=.6, color='k', label='Three Point Rule Introduced')
    ax.axvline(49, linestyle='--',alpha=.6, color='green', label='Player\'s Association\nStrike')
    
    # makes the top and right spines grey
    ax.spines['right'].set_color((.8,.8,.8))
    ax.spines['top'].set_color((.8,.8,.8))
    
    # stylizes labels and title
    ax.xaxis.get_label().set_style('italic')
    ax.xaxis.get_label().set_size(10)
    ax.yaxis.get_label().set_style('italic')
    ax.yaxis.get_label().set_size(10)
    ax.title.set_weight('bold')
    
    # sets appropriate x and y axis limits
    ax.set_xlim(0,67)
    ax.set_ylim(selected_season_stats_by_year[stat].max() *.1,selected_season_stats_by_year[stat].max()*1.2)
    
    ax.legend()
fig.suptitle('Average Player Statistics Over the Years', fontsize=20,weight='bold')
fig.tight_layout()
plt.savefig('mean_stats_by_year.png')


# plots selected the distrubitoin of selected statistics from Steph Curry against Brian Taylor
# it's meant to show how much the definition of a 'good shooter' has changed
new_key_stats = ['Player', '3PA', '3P%','2PA', '2P%', 'FTA','FT%']

steph = season_stats[(season_stats['Player'] == 'Stephen Curry') & (season_stats.Year == 2017)][new_key_stats]
brian = season_stats[(season_stats['Player'] == 'Brian Taylor')&(season_stats['Year'] == 1981)][new_key_stats]

fig, axs = plt.subplots(1, 3, figsize=(10, 4))
percents = ['3P%','2P%','FT%']
attempts = ['3PA','2PA','FTA']
for attempt, percentage, ax in zip(attempts, percents, axs.flatten()):
        
    sa, sb = float(steph[percentage]*steph[attempt] +1), float(steph[attempt]-(steph[percentage]*steph[attempt])+1)
    ba, bb = float(brian[percentage]*brian[attempt]+ 1), float(brian[attempt]-(brian[percentage]*brian[attempt])+1)
    sbeta = stats.beta(sa, sb)
    bbeta = stats.beta(ba,bb)
    x = np.linspace(0.0, 1.0, 301)
    ax.plot(x, sbeta.pdf(x), label='Steph Curry')
    ax.plot(x, bbeta.pdf(x), label='Brian Taylor')
    ax.set_title(f'{codes[attempt][:-9]}')
    ax.axvline(sbeta.ppf(.5), alpha=.6,linestyle='--', color='k', label='mean')
    ax.axvline(bbeta.ppf(.5),alpha=.6, linestyle='--', color='k')
    
    ax.set_xlabel('Success Rate')
    ax.set_ylabel('Probability')
    
    # set the x limit more appropriately
    ax.set_xlim(min(sbeta.ppf(.001),bbeta.ppf(.001)), max(sbeta.ppf(.999), bbeta.ppf(.999)))
    
    # makes the top and right spines grey
    ax.spines['right'].set_color((.8,.8,.8))
    ax.spines['top'].set_color((.8,.8,.8))
    
    # stylizes labels and title
    ax.xaxis.get_label().set_style('italic')
    ax.xaxis.get_label().set_size(10)
    ax.yaxis.get_label().set_style('italic')
    ax.yaxis.get_label().set_size(10)
    ax.title.set_weight('bold')
    
    # adds transparent grid
    ax.grid('on', alpha=.5)
    
    ax.legend()

fig.suptitle('Steph Curry\nVs\nBrian Taylor(3 Point Shooting Leader 1981)', fontsize=14, weight='bold')
plt.tight_layout()
plt.savefig('Steph_versus_Brian.png')

# hypothesis testing
# h0 = the three point rule in 1979 didn't impact the  is played
# hA = the three point rule changed how the game is played and which statistics 
# athletes focus on during practice

top_ten_stats = ['Player','Year','3PA','3P%','2PA','2P%','AST','BLK','STL','TRB','TOV','FTA','PTS', 'PER']
pvalues = []

# separate years to compare
newest = season_stats[season_stats.Year == 2017.0]
oldest = season_stats[season_stats.Year == 1980]

fig, axs = plt.subplots(3,4, figsize=(20,15))

for stat, ax in zip(top_ten_stats[2:], axs.flatten()):
    # create distributions and a range
    x = np.linspace(min(newest[stat].min(),oldest[stat].min()),
                    max(newest[stat].max(), oldest[stat].max()),
                    300)
    new_dist = stats.norm(loc=newest[stat].mean(), scale=newest[stat].std())
    old_dist = stats.norm(loc=oldest[stat].mean(), scale=oldest[stat].std())
    
    # Mann Whitney U tests to test whether the distribution has changed in our comparison 
    pval = stats.mannwhitneyu(oldest[stat], newest[stat])[1]
    
    # make plots
    ax.plot(x, new_dist.pdf(x), label='2017')
    ax.plot(x, old_dist.pdf(x), label='1980')
    
    # add title and labels
    ax.set_title(f'{codes[stat]}')
    ax.set_xlabel(f'P Value: {pval:.5f}')
    ax.set_ylabel('Probability')
    
    # show means for each distribution
    ax.axvline(newest[stat].mean(), linestyle='--', color='k', alpha=.6)
    ax.axvline(oldest[stat].mean(), linestyle='--', color='k', alpha=.6)
    
    # makes the top and right spines grey
    ax.spines['right'].set_color((.8,.8,.8))
    ax.spines['top'].set_color((.8,.8,.8))
    
    # stylizes labels and title
    ax.xaxis.get_label().set_weight('bold')
    ax.xaxis.get_label().set_size(10)
    ax.yaxis.get_label().set_style('italic')
    ax.yaxis.get_label().set_size(10)
    ax.title.set_weight('bold')
    ax.grid('on', alpha=.3)
    ax.legend()
    
fig.suptitle('Average League Statistics\n2017 vs 1980\n(Mann Whitney U Test)', fontsize=20, weight='bold')

fig.tight_layout()
plt.savefig('stats_2017_v_1980.png')



# separates the data by decade
eighties = players_and_stats[(players_and_stats.Year < 1990) & (players_and_stats.Year > 1979)]
nineties = players_and_stats[(players_and_stats.Year < 2000) & (players_and_stats.Year > 1989)]
twooughts = players_and_stats[(players_and_stats.Year < 2010) & (players_and_stats.Year > 1999)]
twotens = players_and_stats[(players_and_stats.Year < 2018) & (players_and_stats.Year > 2009)]

# extracts the top ten scorers from each decade
top_ten_eighties = eighties[eighties['PTS'] >= np.percentile(eighties['PTS'].values, 90)][['Player','PTS']].groupby('Player').mean('PTS').sort_values(by=['PTS'], inplace=False, ascending=False).head(10)
top_ten_nineties = nineties[nineties['PTS'] >= np.percentile(nineties['PTS'].values, 90)][['Player','PTS']].groupby('Player').mean('PTS').sort_values(by=['PTS'], inplace=False, ascending=False).head(10)
top_ten_two_oughts = twooughts[twooughts['PTS'] >= np.percentile(twooughts['PTS'].values, 90)][['Player','PTS']].groupby('Player').mean('PTS').sort_values(by=['PTS'], inplace=False, ascending=False).head(10)
top_ten_two_tens = twotens[twotens['PTS'] >= np.percentile(twotens['PTS'].values, 90)][['Player','PTS']].groupby('Player').mean('PTS').sort_values(by=['PTS'], inplace=False, ascending=False).head(10)

# gets the season statistics for each player, separating by decade
top_ten_stats = ['Player','Year', 'PER','3PA','3P%','2PA','2P%','AST','BLK','FTA','STL','TOV%','PTS']
top_ten_eighties_stats = [season_stats[(season_stats['Player']==name) &(season_stats.Year < 1990) & (season_stats.Year > 1979)][top_ten_stats] for name in top_ten_eighties.index]
top_ten_nineties_stats = [season_stats[(season_stats['Player']==name) &(season_stats.Year < 2000) & (season_stats.Year > 1989)][top_ten_stats] for name in top_ten_nineties.index]
top_ten_two_oughts_stats = [season_stats[(season_stats['Player']==name) &(season_stats.Year < 2010) & (season_stats.Year > 1999)][top_ten_stats] for name in top_ten_two_oughts.index]
top_ten_two_tens_stats = [season_stats[(season_stats['Player']==name) &(season_stats.Year < 2018) & (season_stats.Year > 2009)][top_ten_stats] for name in top_ten_two_tens.index]

# calculates the means for each of those players in the respective decade
eighties_means = [df.groupby('Player').mean() for df in top_ten_eighties_stats]   
nineties_means = [df.groupby('Player').mean() for df in top_ten_nineties_stats]
two_oughts_means = [df.groupby('Player').mean() for df in top_ten_two_oughts_stats]
two_tens_means = [df.groupby('Player').mean() for df in top_ten_two_tens_stats]

#  concats the lists of means into pandas dataframes 
eighties_total = pd.concat(eighties_means)
nineties_total = pd.concat(nineties_means)
twooughts_total = pd.concat(two_oughts_means)
twotens_total = pd.concat(two_tens_means)


fig, axs = plt.subplots(2,5, figsize=(20, 12))
for stat, ax in zip(top_ten_stats[3:], axs.flatten()):
    # get the means of each statistic by decade
    means = [eighties_total[stat].mean(), nineties_total[stat].mean(),twooughts_total[stat].mean(), twotens_total[stat].mean()]
    
    # makes basic plot
    ax.plot(range(4), means, linewidth=2, marker='o')
    
    # change the bounds of the y axis to more accurately show the change in relation
    # to the league maximum and minimum
    ax.set_ylim(season_stats[stat].min(), season_stats[stat].max()*.85)
    
    # adds title and labels
    ax.set_title(f'{codes[stat]}')
    ax.set_xlabel('Decade')
    ax.set_ylabel(f'{codes[stat]}')
    ax.set_xticks(range(4))
    ax.set_xticklabels([(str(year) + '\'s') for year in range(1980, 2020, 10)])
    
    # stylizes labels and title
    ax.xaxis.get_label().set_style('italic')
    ax.xaxis.get_label().set_size(10)
    ax.yaxis.get_label().set_style('italic')
    ax.yaxis.get_label().set_size(10)
    ax.title.set_weight('bold')
    
    # adds transparent grid
    ax.grid('on', alpha=.3)
fig.suptitle('Average Statistics for the Top Ten\nPlayers by decade', fontsize=24, weight='bold')
fig.tight_layout()
plt.savefig('top_ten_stats_by_decade.png')
