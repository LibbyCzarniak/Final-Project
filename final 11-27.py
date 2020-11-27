#!/usr/bin/env python
# coding: utf-8

# Throughout this notebook, we are going to analyze NFL combine data from 2000-2017 to help NFL owners and coaches make informed decisions during the draft. 
# 
# We'll first perform exploratory data analysis using scatterplots and summary statistics for relevant tests for the top 5 positions at the combines. This should give owners and coaches a general idea of how certain positions performed at the combine.
# 
# We'll then build a recommender system that allows coaches and owners to input a position, round, and pick number and spits back statistics for players of the same position who have been drafted at the beginning of that round in the past. Hopefully, NFL teams can use these statistics to identify players at the combine who may be candidates for the draft pick. 

# We first import all the necessary packages used throughout the project. 

# In[1]:


get_ipython().system('pip install seaborn==0.11.0')


# In[2]:


get_ipython().system('pip install streamlit==0.71.0')


# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# We have all of the packages that we'll need throughout the notebook imported.
# 
# Now let's load in our data file with combine statistics for 2000-2017, save it to a dataframe, and inspect the beginning rows to get an idea of the data in each column.

# In[4]:


all_data = pd.read_csv('combine_data_since_2000.csv')
all_data.head()


# All the data is in the dataframe. The columns show that we have player name, position, height, and weight as well as the statistics for the combine tests. There are also columns for the year they were drafted in, the team that drafted them, and their round and pick numbers. 
# 
# All of the columns appear to be of the appropriate datatype, and some players have nan values for some of the tests. There are also some players with nan values for team, round, and pick. These players were not drafted that year.
# 
# We only want to look at players who have been drafted, so we'll make a dataframe with only rows that do not have an nan value in the Team column.

# In[5]:


nfl_data = all_data[all_data['Team'].notna()] # keep only players who have a team in the Team column
nfl_data # print out the dataframe


# So now our dataframe has data only for the players who were drafted. There are still nan values for some tests for some players, but we'll deal with those later on. 
# 
# We want to explore data and make recommendations for only five of the more well-known positions in the draft: quarterback (QB), defensive tackle (DT), running back (RB), wide receiver (WR), and outside linebacker (OLB).
# 
# We'll make five new dataframes that contain data for players for each of these five positions so we can analyze them separately and make recommendations for them.

# In[6]:


nfl_data['Round'] =nfl_data['Round'].astype(int)


# We try to find the number of each person drafted for each position.

# In[7]:


# nfl_data['extra'] = 1
# nfl_data.groupby('Pos')['extra'].sum()


# In[8]:


qb_df = nfl_data.loc[nfl_data['Pos']== 'QB'] # get only rows for quarter backs
dt_df = nfl_data.loc[nfl_data['Pos']== 'DT'] # get only rows for defensive tackles
rb_df = nfl_data.loc[nfl_data['Pos']== 'RB'] # get only rows for running backs
wr_df = nfl_data.loc[nfl_data['Pos']== 'WR'] # get only rows for wide receivers
olb_df = nfl_data.loc[nfl_data['Pos']== 'OLB'] # get rows for only outside linebackers
qb_df.info()


# There's now 5 dataframes: one for quarterbacks, one for defensive tackles, one for running backs, one for wide receivers, and one for outside linebackers.
# 
# We want to look at only the 3 most important combine tests for these positions, so we'll keep columns in these dataframes with only those statistics. We'll also keep player names, heights and weights; we also want to make sure we keep the year they were drafted and their round and pick.

# What stats were looking at for each position
# 
# RB= forty, cone, shuttle
# 
# QB= forty, shuttle, benchreps
# 
# DT = benchreps, cone, forty 
# 
# WR= forty, vertical, shuttle
# 
# OLB= shuttle, cone, vertical
# 
# keep player, position, the three stats, year, round, and pick, ht, wt 

# In[9]:


qb_df = qb_df[['Player', 'Ht', 'Wt', 'Forty', 'Shuttle', 'BenchReps', 'Year', 'Round', 'Pick']] # keep columns for forty, shuttle run, bench reps
qb_df


# In[10]:


wr_df = wr_df[['Player', 'Ht', 'Wt', 'Forty', 'Shuttle', 'Vertical', 'Year', 'Round', 'Pick']] # keep columns for forty, shuttle run, and vertical jump
wr_df


# In[11]:


rb_df = rb_df[['Player', 'Ht', 'Wt', 'Forty', 'Shuttle', 'Cone', 'Year', 'Round', 'Pick']] # keep columns for forty, cone, and shuttle run
rb_df


# In[12]:


dt_df = dt_df[['Player', 'Ht', 'Wt', 'Forty', 'Cone', 'BenchReps', 'Year', 'Round', 'Pick']] # keep columns for forty, cone, and bench reps
dt_df


# In[13]:


olb_df = olb_df[['Player', 'Ht', 'Wt', 'Vertical', 'Shuttle', 'Cone', 'Year', 'Round', 'Pick']] # keep columns for vertical jump, shuttle run, and cone
olb_df


# The five individual dataframes have only the more important combine test statistics that NFL coaches and owners would be interested in analyzing for each position.
# 
# Our goal is to provide summary statistics (minimum, maximum, median, and average) for the three main combine tests for each of these positions. We'll include data from every year to ensure that enough statistics are included in the calculations.
# 
# We're going to make four functions that will calculate the min, max, median, and average. We'll show these at the top of the dashboard when an owner or coach specifies which position they want to analyze and get a rcommendation for.

# We want to use a dictonary to take the users input on the slider and match the dataframe used in the function, and do the same with statistic. We'll use them for the next 4 functions 

# In[15]:


def get_mean_stat(df, stat): # take the dataframe and combine test 
    return df[stat].mean() # calculate the mean for the column with the combine test statistic

get_mean_stat(dt_df, 'Forty')


# In[16]:


def get_max_stat(df, stat): # take the dataframe and combine test 
    return df[stat].max() # calculate the maximum for the column with the combine test statistic


# In[17]:


def get_min_stat(df, stat): # take the dataframe and combine test 
    return df[stat].min() # calculate the minimum for the column with the combine test statistic


# In[18]:


def get_median_stat(df, stat): # take the dataframe and combine test 
    return df[stat].median() # calculate the median for the column with the combine test statistic


# There's four functions that give us the summary statistics we need to display at the top of the dashboard.
# 
# Graphs are also an important part of exploratory data analysis. We'll make boxplots for the combine test statistics for the five positions. The statistic will be on the y-axis and the round will be on the x-axis. We're going to use data from every year between 2000 and 2017 since some years may not have data for every round.
# 
# We'll make a function that takes as parameters the position and combine test the NFL coaches and owners choose. 

# Going to make a scatterplot where the round will be shown on the x-axis, and on the y-axis the user can choose what stat they want to see, and what year. 

# In[41]:


sns.boxplot( x='Round', y='Shuttle', data=qb_df )
#plt.plot( qb_df['Round'], qb_df['Shuttle'], 'bo' ) # blue circles
#plt.ylim( 0, 5 )
plt.title( 'QB Shuttle Statistics for each Round', fontdict={ "fontsize": 25 } )
plt.xlabel( 'Round' )
plt.ylabel( 'Shuttle Statistics' )
plt.show()


# Now we have a function to make a graph as well. These graphs will help NFL coaches and players visualize how players performed at the combine across each round.

# We tried to sort it by year too, but there wasn't enough data for each specific year, makes more sense to look at them all at once. 

# st.slider("Prompt",min,max,default,step)
# 

# st.selectbox("Prompt",("List","of","options"))

# In[20]:


round_pick = st.slider("Pick a round(1-7):",1,7,1,1)


# In[ ]:


position = st.selectbox("Pick a position",('Quarterback', 'Defensive Tackle', 'Running Back', 'Wide Reciever', 'Outside Line Backer'))


# Can't pick quarterback, benchreps, and a specific round because there isnt enough data 

# In[37]:


if position == 'Quarterback':
    stat = st.selectbox("Pick a Statistic to graph:",('Forty', 'Shuttle', 'Benchreps'))
elif position == 'Defensive Tackle':
    stat = st.selectbox("Pick a Statistic to graph:",('Forty', 'Cone', 'Benchreps'))
elif position == 'Running Back':
    stat = st.selectbox("Pick a Statistic to graph:", ('Forty', 'Cone', 'Shuttle'))
elif position == 'Wide Reciever':
    stat = st.selectbox("Pick a Statistic to graph:", ('Forty', 'Shuttle', 'Vertical'))
else:
    stat = st.selectbox("Pick a Statistic to graph:", ('Cone', 'Shuttle', 'Vertical'))


# In[38]:


position_dict = {'Quarterback':qb_df,
                 'Defensive Tackle': dt_df,
                 'Running Back': rb_df,
                 'Wide Receiver': wr_df,
                 'Outside Line Backer': olb_df}


# In[40]:


def make_boxplot(stat, position):
    df = position_dict.get(position)
    sns.boxplot( x=df['Round'], y=stat, data= df  )
    plt.title( f'{position} {stat} Statistics for each Round' )
    plt.xticks( rotation=90 )
    plt.show()

make_boxplot('Forty', 'Quarterback')


# Person inputs the round, and the position. 
# 
# when they pick the position they get the mean, max, min, median for the three important stats 
# 
# And we look at the players with the same position who have been drafted in that round (for every year)
# 
# rank the players by pick, and take the statistics for the top 10-20 in each round, and give back those statistics 

# In[ ]:


sns.boxplot( x='Round', y='Vertical', data=olb_df )
# plt.plot( qb_df['Round'], qb_df['Shuttle'], 'bo' ) # blue circles
#plt.ylim( 0, 5 )
plt.title( 'QB Shuttle Statistics for each Round', fontdict={ "fontsize": 25 } )
plt.xlabel( 'Round' )
plt.ylabel( 'Shuttle Statistics' )
plt.show()


# Dropped the rows with nan values 

# In[ ]:


# qb_r1 = qb_df[qb_df.Round == 1]
# qb_r1.head(5)


# In[ ]:


# def get_avg_stats():
#     rb_df2 = rb_df.sort_values(['Round', 'Pick'])
#     rb_df2.dropna()
#     for i in range (1, 8):
#         new_df = rb_df2['Round'] == i 


# In[ ]:


def sort_by_round(pos_df):
    pos_df2 = pos_df.sort_values(['Round', 'Pick'])
    pos_df2 = pos_df2.dropna()
    return pos_df2

sort_by_round(wr_df)


# Needed to put pos_df= sort_by_round(wr_df) there or else it wouldn't run, soo everything right now is on the wide reciever data frame

# In[ ]:


pos_df2 = sort_by_round(wr_df)

def get_top_five_picks(round_pick):     
    df = pos_df2.loc[pos_df2['Round']==round_pick]
    df_t5_round = df.iloc[0:5]   
    return df_t5_round   

df_t5_round = get_top_five_picks(1)
#df['first_year'] = df['years'].apply( get_first_year )


# In[ ]:


df_t5_round = get_top_five_picks(1)

def get_avg_stats(rb_t5_r1):
    return df_t5_round.iloc[:,3:6].mean()

get_avg_stats(df_t5_round)

