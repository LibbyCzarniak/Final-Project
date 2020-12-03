import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Throughout this part of the project we are going to develop the primary parts of our dashboard. We want to create input controls that allow users to provide
# a round pick, position, combine test, and test statistic for a player they're considering. This input will be used to provide summary statistics from past NFL
# Combines for the test the user gives. It'll also be utilized in creating boxplots depicting the distribution of data points for that test in each round of past
# NFL Combines. If the user provides a statistic for a player he's considering, he'll be able to get an idea of how that player compares to past performances.
# Lastly, we want to recommend statistics the user may want to look for (based on the input he gives) when trying to decide on a player to draft.

# Based on our prior data preparation, we have code to create five datasets that we'll need to accomplish our vision for the dashboard.
# We'll keep explanations short here since this is all duplicated from the Cleaning for Dashboard notebook.

# Let's load in our data file with combine statistics for 2000-2017 and save it to a dataframe.

all_data = pd.read_csv('combine_data_since_2000.csv') # read in the csv file with the dataset

# We'll make a dataframe with only rows for players who have been drafted and change the Round column to integer datatype

nfl_data = all_data[all_data['Team'].notna()]               # keep only players who have a team in the Team column rather than nan
nfl_data['Round'] =nfl_data['Round'].astype(int)            # change round column datatype

# We'll make five new dataframes that contain data for players for each of the five positions so we can analyze them separately and make recommendations for them.

qb_df = nfl_data.loc[nfl_data['Pos']== 'QB'] # get only rows for quarter backs
dt_df = nfl_data.loc[nfl_data['Pos']== 'DT'] # get only rows for defensive tackles
rb_df = nfl_data.loc[nfl_data['Pos']== 'RB'] # get only rows for running backs
wr_df = nfl_data.loc[nfl_data['Pos']== 'WR'] # get only rows for wide receivers
olb_df = nfl_data.loc[nfl_data['Pos']== 'OLB'] # get rows for only outside linebackers

# Let's change those dataframes to have columns for statistics we care about and make a copy for manipulation later on

qb_df = qb_df[['Player', 'Ht', 'Wt', 'Forty', 'Shuttle', 'BenchReps', 'Year', 'Round', 'Pick']] # keep columns for forty, shuttle run, bench reps
qb_df2 = qb_df.copy()

wr_df = wr_df[['Player', 'Ht', 'Wt', 'Forty', 'Shuttle', 'Vertical', 'Year', 'Round', 'Pick']] # keep columns for forty, shuttle run, and vertical jump
wr_df2 = wr_df.copy()

rb_df = rb_df[['Player', 'Ht', 'Wt', 'Forty', 'Shuttle', 'Cone', 'Year', 'Round', 'Pick']] # keep columns for forty, cone, and shuttle run
rb_df2 = rb_df.copy()

dt_df = dt_df[['Player', 'Ht', 'Wt', 'Forty', 'Cone', 'BenchReps', 'Year', 'Round', 'Pick']] # keep columns for forty, cone, and bench reps
dt_df2 = dt_df.copy()

olb_df = olb_df[['Player', 'Ht', 'Wt', 'Vertical', 'Shuttle', 'Cone', 'Year', 'Round', 'Pick']] # keep columns for vertical jump, shuttle run, and cone
olb_df2 = olb_df.copy()

# Now we have 5 dataframes (one for each position) containing statistic columns that we care about and a copy of them.

# We'll transition to creating the objects we want to include on the dashboard. Let's give the dashboard a title and explain to the user what he
# can do with it.

# set title for dashboard
st.title("NFL Combine Analysis")
# describe purpose to user
st.markdown("Provide a position, a combine test, and the round you have a draft pick in. You'll be able to see "
            "statistics for that test and position from combines spanning across 2000-2017. "
            "You can also input a statistic you have for a player and see how they rank against past players. "
            "We'll use the position and round to give recommendations for what statistics you may want to look for "
            "at that position.")

# We have a title and the purpose of the dashboard clearly laid out for users.

# We're going to make four functions that will calculate the min, max, median, and average for the summary statistics displayed at the top of the dashboard.
# We'll include data from every year to ensure that enough statistics are included in the calculations.

def get_mean_stat(df, stat):                # take the dataframe and combine test
    return df[stat].mean()                  # calculate and return the mean for the column with the combine test statistic

def get_max_stat(df, stat):                 # take the dataframe and combine test
    return df[stat].max()                   # calculate and return the maximum for the column with the combine test statistic

def get_min_stat(df, stat):                 # take the dataframe and combine test
    return df[stat].min()                   # calculate and return the minimum for the column with the combine test statistic

def get_median_stat(df, stat):              # take the dataframe and combine test
    return df[stat].median()                # calculate and return the median for the column with the combine test statistic

# Now we have four functions that we can use to calculate the summary statistics we want at the top of the dashboard.
# We'll use these later on after we have defined the user input since we need that to calculate the summary stats.

# We need to make sliders and drop down boxes that allow users to choose a round, position, combine test, and statistic
# for a particular player they're considering.

# make the slider for the user to choose the round
round_pick = st.sidebar.slider("Pick a round(1-7):",1,7,1,1)

# make a drop down box that allows the user to choose a position
position = st.sidebar.selectbox("Pick a position:",('Quarterback', 'Defensive Tackle', 'Running Back', 'Wide Receiver', 'Outside Line Backer'))

# Make a drop down box that allows the user to choose which combine test he wants data for. We'll use if/else
# statements to determine which combine tests the user can pick from based on the position he's analyzing.
# we'll also create an input box that allows the use to give a statistic for a player he's considering

if position == 'Quarterback':
    stat = st.sidebar.selectbox("Pick a Statistic to graph:",('Forty', 'Shuttle', 'BenchReps'))
    if stat == "Forty":
        input_stat = st.sidebar.number_input("Input Forty Stat:")
    elif stat == "Shuttle":
        input_stat = st.sidebar.number_input("Input Shuttle Stat:")
    elif stat == "BenchReps":
        input_stat = st.sidebar.number_input("Input BenchReps Stat:")
elif position == 'Defensive Tackle':
    stat = st.sidebar.selectbox("Pick a Statistic to graph:",('Forty', 'Cone', 'BenchReps'))
    if stat == "Forty":
        input_stat = st.sidebar.number_input("Input Forty Stat:")
    elif stat == "Cone":
        input_stat = st.sidebar.number_input("Input Cone Stat:")
    elif stat == "BenchReps":
        input_stat = st.sidebar.number_input("Input BenchReps Stat:")
elif position == 'Running Back':
    stat = st.sidebar.selectbox("Pick a Statistic to graph:", ('Forty', 'Cone', 'Shuttle'))
    if stat == "Forty":
        input_stat = st.sidebar.number_input("Input Forty Stat:")
    elif stat == "Cone":
        input_stat = st.sidebar.number_input("Input Cone Stat:")
    elif stat == "Shuttle":
        input_stat = st.sidebar.number_input("Input Shuttle Stat:")
elif position == 'Wide Receiver':
    stat = st.sidebar.selectbox("Pick a Statistic to graph:", ('Forty', 'Shuttle', 'Vertical'))
    if stat == "Forty":
        input_stat = st.sidebar.number_input("Input Forty Stat:")
    elif stat == "Shuttle":
        input_stat = st.sidebar.number_input("Input Shuttle Stat:")
    elif stat == "Vertical":
        input_stat = st.sidebar.number_input("Input Vertical Stat:")
else:
    stat = st.sidebar.selectbox("Pick a Statistic to graph:", ('Cone', 'Shuttle', 'Vertical'))
    if stat == "Cone":
        input_stat = st.sidebar.number_input("Input Cone Stat:")
    elif stat == "Shuttle":
        input_stat = st.sidebar.number_input("Input Shuttle Stat:")
    elif stat == "Vertical":
        input_stat = st.sidebar.number_input("Input Vertical Stat:")

# Now we have all of our sliders, drop down boxes, and input boxes that we need to get the appropriate user input.

# Let's make a dictionary that has the position and its corresponding dataframe.

position_dict = {'Quarterback':qb_df2,
                 'Defensive Tackle': dt_df2,
                 'Running Back': rb_df2,
                 'Wide Receiver': wr_df2,
                 'Outside Line Backer': olb_df2}

# now we have a dictionary with the position name as the key and the name of the dataframe for that positon as the value.
# We can use this to get the appropriate dataframe based on the position that the user is interested in throughout the rest of the code.

# Let's use that dictionary and the user input to display the summary stats for the combine test of the user's position

st.header(f"Summary statistics for {stat} test for {position}s from 2000-2017 NFL Combines: ")  # create a header
st.write(f"Minimum: {get_min_stat(position_dict.get(position), stat):.2f} ")                    # call get_min_stat function for minimum
st.write(f"Maximum: {get_max_stat(position_dict.get(position), stat):.2f} ")                    # call get_max_stat function for maximum
st.write(f"Average: {get_mean_stat(position_dict.get(position), stat):.2f} ")                   # call get_mean_stat function for average
st.write(f"Median: {get_median_stat(position_dict.get(position), stat):.2f} ")                  # call get_median_stat function for median

# now we have the summary statistics displayed at the top of the dashboard for the position and given combine test

# Let's make boxplots for the combine test that the user is interested in. The statistic will be on the y-axis
# and the round will be on the x-axis. We're going to use data from every year between 2000 and 2017 since some years may
# not have data for every round. If the user provides a statistic for a player, we want to plot that point on the boxplot
# for the given round to show the user where the player falls compared to past players.

df = position_dict.get(position)                        # get the dataframe from position_dict based on the position the user gives
df2 = df[df[stat].notna()]                              # drop nans to avoid errors
sns.boxplot(x= df2['Round'], y=stat, data= df2)         # make a boxplot with Round on the x-axis and stat on the y-axis
if input_stat != 0:                                     # if user provides a statistic for a player, plot that dot on the graph
    plt.scatter(round_pick-1, input_stat, marker="o",
                s=100, color='blue')
plt.title( f'{position} {stat} Statistics for each Round')      # set the title
st.pyplot(plt.gcf())                                            # show the graph

# we've made our boxplots and will plot the given player statistic on them. The user will be able to visualize past Combine statistics
# and investigate how players statistics compare based on the draft round.

# We want to provide the percentile for the statistic that the user provides. We need to get the dataframe for the user-entered position
# and sort it to put the picks in order for each round. We can then add the user-provided statistic to the dataframe and calculate
# its percentile

pos_df = position_dict.get(position)                    # get the dataframe from the position dictionary
pos_df2 = pos_df.sort_values(['Round', 'Pick'])         # sort on Round then Pick columns
pos_df2_copy = pos_df2.copy()

# make a dataframe with only the round and stat the user wants
all_old_stats = pos_df2_copy[pos_df2_copy.Round == round_pick][stat]
# append the user-provided stat to the dataframe
with_new_player = all_old_stats.append( pd.Series( [ input_stat ] ) )
# calculate percentiles and multiply by 100
percentiles = with_new_player.rank(pct=True) * 100
# get the percentile for the statistic that we added since it will be the last row
my_percentile = percentiles.iloc[-1]

# now we have the percentile for the statistic that the user provides for his player of interest. This will give the user
# a quantitative analysis of how his player of interest compares to past players as opposed to a visual analysis with the boxplot.

# let's write the percentile to the dashboard

st.write(f"This player falls in the {my_percentile:.2f}th percentile of {position}s.")

# now we have the percentile on the dashboard just below the boxplots

# Let's now turn to making a recommendation. When the user gives a position and round, he'll be able
# to see the statistics for the three combine tests for that position based on the top five draft
# picks from that round in the past. This will give the user an idea of what combine statistics he may
# want to look for when deciding who he wants to draft.

# Let's make the function that will give average combine test statistics for the top 5 picks
# in each round from past NFL drafts.

def get_top_five_picks(round_pick):                         # make a function that takes the round as parameter
    df = pos_df2.loc[pos_df2['Round']==round_pick]          # filter the position dataframe to include only stats for that round
    df_t5_round = df.dropna().iloc[0:5]                              # get just the first 5 rows from that dataframe (top 5 picks)
    return df_t5_round.iloc[:,3:6].mean()                   # return the mean combine test statistics for the top 5 picks from that round

# we have a function that'll give us the average statistics for the top 5 picks in the user-given round. We can display these statistics on the dashboard

# make a header telling the user he's going to see recommended stats
st.header("Recommended Statistics")

st.write(f"These are the average statistics for {position}s who were one of the top 5 picks in the round you're looking at:")

#call the get_top_five_picks function to calculate the recommended statistics and display them
df_t5_round = get_top_five_picks(round_pick)
df_t5_round

# now the recommended statistics are displayed at the bottom of the dashboard

# we've successfully created all of the object we need to provide users with a comprehensive analysis of NFL Combine data
# and help them make informed decisions at the NFL draft.
