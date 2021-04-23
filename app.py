import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.title('Top Play Store Games EDA')

st.markdown("""
In this notebook, we will do some analysis by looking at the data of Top Play Store Games.
* What is the percentage of free video games?
* Which video game category has the most overall ratings?
* What category of video games are the most installed?
* Wat are the best video games according to google play?
""")

data = pd.read_csv('android-games.csv')

# Data Cleaning
data[['installs','mult']] = data['installs'].str.split(expand=True)
data[['mult']] = data[['mult']].replace(to_replace=['M','K','k'],
             value = [1, 0.1, 0.1])
data[['installs']] = data[['installs']].astype(float, errors='raise')
data['installs'] = data['installs'] * data['mult']
data['installs'] = data['installs'].apply(lambda x: str(x) + ' ' + 'M')
data['price'] = data['price'].apply(lambda x : '$' + ' ' + str(x))
data = data.drop(columns='mult')

# Display Data
if st.checkbox("Display Data"):
    st.write(data.head())

# Columns Name
if st.checkbox("Columns Name"):
    st.write(data.columns)

# Rows and Columns
dimensions = st.radio("What Dimension Do You Want to Show?", ("Rows", "Columns"))
if dimensions == "Rows":
    st.text("Showing Length of Rows")
    data.shape[0]

if dimensions == "Columns":
    st.text("Showing Length of Columns")
    data.shape[1]

# Missing Values
if st.checkbox("Looking for missing values"):
    st.write(data.isnull().sum())

# General Statistics 
if st.checkbox("Show Summary of Dataset"):
    st.write(data.describe())


#Sidebar
st.sidebar.title("Dataset")
st.sidebar.text_input("Link to data",("https://www.kaggle.com/dhruvildave/top-play-store-games"))

st.sidebar.title("Options")
option = st.sidebar.selectbox("which Dashboard?", ('Donut Chart', 'Bar Chart', 'Table'))

# st.header(option)


prices_games = data[['price']].value_counts().to_frame().reset_index().rename(columns={0:'counts'})
prices_games['price'] = prices_games['price'].apply(lambda x : str(x) + ' ' + "video games")
labels = list(prices_games['price'])

if option == 'Donut Chart':
    # Plot Video Game Prices
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=prices_games['counts'], name="PRICE"),
                row=1, col=1)
    fig.update_traces(hole=.5, hoverinfo="label+value+name")
    fig.update_layout(
        title="Video game prices",
        title_x=0.3,
        legend=dict(
            x=0.5,
            y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=12,
                color="black")
        ))
    st.plotly_chart(fig)


if option == 'Bar Chart':
    # Plot Games Category by total ratings
    category_tr = data.groupby(by='category')['total ratings'].sum().to_frame().sort_values('total ratings').reset_index()

    fig1 = px.bar(category_tr, x='total ratings', y='category',
                color='category')
    fig1.update_layout(showlegend=False,
                    title="Games Category by total ratings",
                    title_x=0.5,
                    xaxis_title='Total ratings',
                    yaxis_title='Category')
    st.plotly_chart(fig1)

    # Plot Games Category by install amount
    cat_installs = data[['category','installs']]
    cat_installs[['installs','mult']]=cat_installs['installs'].str.split(expand=True)
    cat_installs[['mult']]=cat_installs[['mult']].replace(to_replace=['M','K','k'],
                value=[1, 0.1, 0.1])
    cat_installs['installs']=cat_installs[['installs']].astype(float, errors='raise')
    cat_installs['installs']=cat_installs['installs']*cat_installs['mult']
    cat_installs = cat_installs.groupby(by = 'category')['installs'].sum().to_frame().sort_values('installs').reset_index()

    fig2 = px.bar(cat_installs, x='installs', y='category',
                color='category')
    fig2.update_layout(showlegend=False,
                    title="Games Category by install amount",
                    title_x=0.5,
                    xaxis_title='Installs (Millions)',
                    yaxis_title='Category')
    st.plotly_chart(fig2)


if option == 'Table':
    # Plot Top 20 Video Games (install, total ratings, average rating)
    data_table=data[['rank', 'title', 'category','total ratings', 'installs', 'average rating', 'price']]
    data_table[['installs','mult']]=data_table['installs'].str.split(expand=True)
    data_table['mult']=data_table['mult'].replace(to_replace=['M','K','k'],
                value=[1, 0.1, 0.1])
    data_table['installs']=data_table[['installs']].astype(float, errors='raise')
    data_table['installs']=data_table['installs']*data_table['mult']
    data_table=data_table[['title', 'category','total ratings', 'installs', 'average rating', 'price']]
    data_table=data_table.sort_values(['installs','total ratings', 'average rating'], ascending=False)[:20]
    data_table['installs'] = data_table['installs'].apply(lambda x: str(x) + ' ' + 'M')

    fig3 = go.Figure(data=[go.Table(
        header=dict(values=list(data_table.columns),
    #                 line_color='darkslategreen',
                    fill_color='lightskyblue',
                    align='center'),
        cells=dict(values=[list(data_table['title']),
                        list(data_table['category']),
                        list(data_table['total ratings']),
                        list(data_table['installs']),
                        list(data_table['average rating']),
                        list(data_table['price'])],
    #                line_color='darkslategray',
    #                fill_color='lightcyan',
                align=['left','center']))
        ])
    fig3.update_layout(title = "Top 20 Video Games (installs, total ratings, average rating)",
                    title_x = 0.5)
    st.plotly_chart(fig3)