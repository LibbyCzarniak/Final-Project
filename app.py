import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Now let's load in our data file with combine statistics for 2000-2017, save it to a dataframe, and inspect the first 5 rows to get an idea of the data in each column.

all_data = pd.read_csv('combine_data_since_2000.csv') # read in the csv file with the dataset
#all_data.head() # print out the first 5 rows

# We only want to look at players who have been drafted, so we'll make a dataframe with only rows that do not have an nan value in the Team column.

nfl_data = all_data[all_data['Team'].notna()] # keep only players who have a team in the Team column
#nfl_data # print out the dataframe

# We'll make five new dataframes that contain data for players for each of these five positions so we can analyze them separately and make recommendations for them.

nfl_data['Round'] =nfl_data['Round'].astype(int)

qb_df = nfl_data.loc[nfl_data['Pos']== 'QB'] # get only rows for quarter backs
dt_df = nfl_data.loc[nfl_data['Pos']== 'DT'] # get only rows for defensive tackles
rb_df = nfl_data.loc[nfl_data['Pos']== 'RB'] # get only rows for running backs
wr_df = nfl_data.loc[nfl_data['Pos']== 'WR'] # get only rows for wide receivers
olb_df = nfl_data.loc[nfl_data['Pos']== 'OLB'] # get rows for only outside linebackers
#qb_df.info()

# Let's change our quarterback dataframe to have only those columns for statistics we care about

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

# We're going to make four functions that will calculate the min, max, median, and average.
# We'll include data from every year to ensure that enough statistics are included in the calculations.
# We want to use a dictionary to take the users input on the slider and match the dataframe used in the
# function, and do the same with statistic. We'll use them for the next 4 functions

def get_mean_stat(df, stat): # take the dataframe and combine test
    return df[stat].mean() # calculate and return the mean for the column with the combine test statistic

#get_mean_stat(dt_df, 'Forty')

def get_max_stat(df, stat): # take the dataframe and combine test
    return df[stat].max() # calculate and return the maximum for the column with the combine test statistic

def get_min_stat(df, stat): # take the dataframe and combine test
    return df[stat].min() # calculate and return the minimum for the column with the combine test statistic

def get_median_stat(df, stat): # take the dataframe and combine test
    return df[stat].median() # calculate and return the median for the column with the combine test statistic

# Let's now make boxplots for the combine test statistics for the five positions. The statistic will be on the y-axis
# and the round will be on the x-axis. We're going to use data from every year between 2000 and 2017 since some years may
# not have data for every round.
#
# We'll make a function that takes as parameters the position and combine test the NFL coaches and owners choose.
# Before making that function, however, we need to make sliders and drop down boxes that allow coaches and owners to choose
# a round, position, and combine test.

# set title for dashboard

st.title("NFL Combine Analysis")
st.markdown("Provide a position, a combine test, and the round you have a draft pick in. You'll be able to see "
            "statistics for that test and position from combines spanning across 2000-2017. "
            "You can also input a statistic you have for a player and see how they rank against past players. "
            "We'll use the position and round to give recommendations for what statistics you may want to look for "
            "at that position.")

# We'll make a drop down box that allows the user to choose which position he wants to analyze statistics for.

position = st.sidebar.selectbox("Pick a position:",('Quarterback', 'Defensive Tackle', 'Running Back', 'Wide Receiver', 'Outside Line Backer'))

# We now need a drop down box that allows the user to choose which combine test he wants data for. We'll use if/else
# statements to determine which combine tests the user can pick from based on the position he's analyzing.

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

# Let's make a dictionary that has the position and its corresponding dataframe that we can use in the function. This will make it easier to get the dataframe we need once the user gives a position.

position_dict = {'Quarterback':qb_df2,
                 'Defensive Tackle': dt_df2,
                 'Running Back': rb_df2,
                 'Wide Receiver': wr_df2,
                 'Outside Line Backer': olb_df2}

# display the summary stats after the user chooses the position and statistic/test

st.header(f"Summary statistics for {stat} test for {position}s from 2000-2017 NFL Combines: ")
st.write(f"Minimum: {get_min_stat(position_dict.get(position), stat):.2f} ")
st.write(f"Maximum: {get_max_stat(position_dict.get(position), stat):.2f} ")
st.write(f"Average: {get_mean_stat(position_dict.get(position), stat):.2f} ")
st.write(f"Median: {get_median_stat(position_dict.get(position), stat):.2f} ")

# make the slider for the user to choose the round

round_pick = st.sidebar.slider("Pick a round(1-7):",1,7,1,1)

# def three_input_stats(pos_df2, stat_type):
#     if position == 'Quarterback':
#         first_stat = st.number_input("Input Forty Stat:")
#         input_stat = st.number_input("Input Shuttle Stat:")
#         input_stat = st.number_input("Input BenchReps Stat:")
#         df_input_stats = pos_df2.append([{'Forty': first_stat,'Shuttle': second_stat,'Benchreps': third_stat}], ignore_index=True)
#     elif position == 'Defensive Tackle':
#         first_stat = st.number_input("Input Forty Stat:")
#         second_stat = st.number_input("Input Cone Stat:")
#         third_stat = st.number_input("Input BenchReps Stat:")
#         df_input_stats = pos_df2.append([{'Forty': first_stat},{'Cone':second_stat},{'Benchreps': third_stat}], ignore_index=True)
#     elif position == 'Running Back':
#         first_stat = st.number_input("Input Forty Stat:")
#         second_stat = st.number_input("Input Cone Stat:")
#         third_stat = st.number_input("Input Shuttle Stat:")
#         df_input_stats = pos_df2.append([{'Forty': first_stat},{'Cone':second_stat},{'Shuttle': third_stat}], ignore_index=True)
#     elif position == 'Wide Reciever':
#         first_stat = st.number_input("Input Forty Stat:")
#         second_stat = st.number_input("Input Shuttle Stat:")
#         third_stat = st.number_input("Input Vertical Stat:")
#         df_input_stats = pos_df2.append([{'Forty': first_stat},{'Shuttle':second_stat},{'Vertical': third_stat}], ignore_index=True)
#     else:
#         first_stat = st.number_input("Input Cone Stat:")
#         second_stat = st.number_input("Input Shuttle Stat:")
#         third_stat = st.number_input("Input Vertical Stat:")
#         df_input_stats = pos_df2.append([{'Cone': first_stat},{'Shuttle':second_stat},{'Vertical': third_stat}], ignore_index=True)
#     return df_input_stats, first_stat, second_stat, third_stat
#
# three_input_stats(qb_df2, 'Forty')


# if first_stat != 0 and second_stat != 0

#player_stat = st.selectbox("Pick")

# if position == 'Quarterback':
#     player_stat = st.selectbox("Pick a Statistic to see on Graph:",('Forty', 'Shuttle', 'Benchreps'))
# elif position == 'Defensive Tackle':
#     player_stat = st.selectbox("Pick a Statistic to see on Graph:",('Forty', 'Cone', 'Benchreps'))
# elif position == 'Running Back':
#     player_stat = st.selectbox("Pick a Statistic to see on Graph:", ('Forty', 'Cone', 'Shuttle'))
# elif position == 'Wide Reciever':
#     player_stat = st.selectbox("Pick a Statistic to see on Graph:", ('Forty', 'Shuttle', 'Vertical'))
# else:
#     player_stat = st.selectbox("Pick a Statistic to see on Graph:", ('Cone', 'Shuttle', 'Vertical'))
# df = position_dict.get(position)

# round = round_pick
# stat = stat
# position = position
# player_stat = player_stat


# We're ready to make the boxplots

df = position_dict.get(position)                            # get the dataframe from position_dict based on the position the user gives
df2 = df[df[stat].notna()]
sns.boxplot(x= df2['Round'], y=stat, data= df2)          # make a boxplot with Round on the x-axis and stat on the y-axis
if input_stat != 0:
    plt.scatter(round_pick-1, input_stat, marker="o",
                s=100, color='blue')
plt.title( f'{position} {stat} Statistics for each Round') # set the title
st.pyplot(plt.gcf())                                         # show the graph

pos_df = position_dict.get(position)
pos_df2 = pos_df.sort_values(['Round', 'Pick']) # sort on Round then Pick columns
pos_df2 = pos_df2.dropna() # drop nans
pos_df2_copy = pos_df2.copy()

# Let's now turn to making a recommender system. When the user gives a position and round, he'll be able
# to see the statistics for the top three combine tests for that position based on the top five draft
# picks from that round in the past. This will give the user an idea of what combine statistics he may
# want to look for when deciding who he wants to draft.

# We need to first make a function that will sort our position dataframes by round and then by pick.
# We'll also drop all nans now to make sure that we can calculate statistics without getting an error.

#df_for_percentiles

all_old_stats = pos_df2_copy[pos_df2_copy.Round == round_pick][stat]
with_new_player = all_old_stats.append( pd.Series( [ input_stat ] ) )
percentiles = with_new_player.rank(pct=True) * 100
my_percentile = percentiles.iloc[-1]


st.write(f"This player falls in the {my_percentile:.2f}th percentile of {position}s.")


# Let's make the function that will give average combine test statistics for the top 5 picks
# in each round from past NFL drafts.

# pos_df2 = sort_by_round(wr_df) # use the sort_by_round function to sort the dataframe for the
# position the user wants

def get_top_five_picks(round_pick):    # make a function that takes the round as parameter
    df = pos_df2.loc[pos_df2['Round']==round_pick] # filter the position dataframe to include only stats for that round
    df_t5_round = df.iloc[0:5]   # get just the first 5 rows from that dataframe (top 5 picks)
    return df_t5_round.iloc[:,3:6].mean()   # return the mean combine test statistics for the top 5 picks from that round

st.header("Recommended Statistics")
st.write(f"These are the average statistics for {position}s who were one of the top 5 picked in the round you're looking at:")

df_t5_round = get_top_five_picks(round_pick)
df_t5_round



