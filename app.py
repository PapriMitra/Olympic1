
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import preprocess, helper
from helper import med_tally

# Define the path to your datasets
path = 'C:\\Users\\pmitr\\OneDrive\\Desktop\\New folder'

# Read the CSV files
df = pd.read_csv( 'events.csv')
df2 = pd.read_csv('regions.csv')

# Preprocess the data using the process function
df = preprocess.process(df, df2)

# Streamlit Sidebar
st.sidebar.title('Olympics - Summer')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# Display dataframe (for debugging purposes)
# st.dataframe(df)
#=========================================
# docker run -p 8501:8501 app
# docker build -t app .
#  ---------------------------- KEY FEATURES-------------------------
#-------------------------\
#   Medal Tally Option     |
#-------------------------/

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

#----------------------\
#   Overall Analysis    |
#----------------------/

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time,
                  x="Year", y="region",
                  title="Participating Nations Over the Years",
                  markers=True
                  )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Participating Nations",
        title_x=0.5,  # Center the title
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        hovermode="x unified"
    )

    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="Event")

    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Year", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

#----------------------------\
#   Country-wise Analysis     |
#----------------------------/

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

#   MEDAL TALLY
#-----------------
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

# HEAT MAP
# --------------
    st.title(selected_country + " excels in the following sports")

    # Generate the pivot table/heatmap data
    pt = helper.country_event_heatmap(df, selected_country)

    # Check if the pivot table is empty
    if pt.empty:
        st.write("No data available for the selected country.")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
    #
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

#----------------------------\
#   Athlete wise Analysis     |
#----------------------------/


if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    #
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')


#    Height Vs Weight Plot
#-------------------------------
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    # Get the filtered data for the selected sport
    temp_df = helper.weight_v_height(df, selected_sport)

    # Create the scatter plot using seaborn
    fig, ax = plt.subplots()

    # Correct scatterplot syntax (with x, y, hue, style properly passed)
    sns.scatterplot(
        x='Weight',
        y='Height',
        hue='Medal',
        style='Sex',
        s=60,
        data=temp_df,
        ax=ax
    )

    # Display the scatter plot
    st.pyplot(fig)

    # Men vs Women Participation Over the Years
    st.title("Men Vs Women Participation Over the Years")

    # Get data for men vs women participation
    final = helper.men_vs_women(df)

    # Create a line plot using Plotly
    fig = px.line(final, x="Year", y=["Male", "Female"],
                  labels={'value': 'Number of Athletes', 'variable': 'Gender'})

    # Update layout to match the specified width and height
    fig.update_layout(autosize=False, width=1000, height=600)

    # Display the line plot
    st.plotly_chart(fig)