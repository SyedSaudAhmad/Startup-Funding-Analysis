import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Startup Funding Analysis", layout="wide")

df = pd.read_csv("Startup_Cleaned.csv")
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

def load_overall_analysis():
    st.title("Overall Analysis")
    # total invested amount
    total = round(df['Amount'].sum())
    # max amount invested in a single startup
    maxfunding = df.groupby('Startup')['Amount'].max().sort_values(ascending=False).head(1).values[0]
    # averageticket size 
    avg = df.groupby('Startup')['Amount'].sum().mean()
    # total funded startups
    totalfunded = df['Startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max', str(round(maxfunding)) + 'Cr')
    with col3:
        st.metric('Average', str(round(avg)) + 'Cr')
    with col4:
        st.metric('Total Funded Startups', str(totalfunded))

    st.header("MoM Growth of Investment")
    selectedOption = st.selectbox('Select Type', ['Total', 'Count'])
    if selectedOption == 'Total':
        temp_df = df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()       
    else:
        temp_df = df.groupby(['Year', 'Month'])['Amount'].count().reset_index()
        
    temp_df['x_axis'] = temp_df['Month'].astype(str) + '-' + temp_df['Year'].astype(str)
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['Amount'])
    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(investor)

    # loading recent 5 investments made by the investor
    last5df = df[df["Investors"].str.contains(investor)].head()[['Date', 'Startup', 'City', 'Round', 'Vertical','Amount']]
    st.subheader("Most Recent Investments")
    st.dataframe(last5df)

    col1 , col2 = st.columns(2)
    # Biggest investments
    with col1:
        bigseries = df[df["Investors"].str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending=False).head(5)
        st.subheader("Biggest Investments")

        fig, ax = plt.subplots()
        ax.bar(bigseries.index, bigseries.values)
        st.pyplot(fig)

    with col2:
        # sectors of investment
        verticalseries = df[df["Investors"].str.contains(investor)].groupby(["Vertical"])['Amount'].sum()

        st.subheader("Sectoors of Investment")
        fig, ax = plt.subplots()
        ax.pie(verticalseries, labels=verticalseries.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig) 

    col1, col2 = st.columns(2)
    with col1:
    # Rounds of investment
        roundseries = df[df["Investors"].str.contains(investor)].groupby(["Round"])['Amount'].sum()
        st.subheader("Rounds of Investment")
        fig, ax = plt.subplots()
        ax.pie(roundseries, labels=roundseries.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig)

    with col2:
        # cities of investment 
        cityseries = df[df["Investors"].str.contains(investor)].groupby(["City"])['Amount'].sum()
        st.subheader("Cities of Investment")

        fig, ax = plt.subplots()
        ax.pie(cityseries, labels=cityseries.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig)

    yearseries = df[df["Investors"].str.contains(investor)].groupby(["Year"])["Amount"].sum()
    st.subheader("YoY Growth of Investment") 
    fig2, ax2 = plt.subplots()
    ax2.plot(yearseries.index, yearseries.values)
    st.pyplot(fig2)

    # Similar Investments

























st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup Analysis', 'Investor Analysis'])

if option == 'Overall Analysis':
    # st.title("Overall Analysis")
    st.write("This section provides an overall analysis of the startup funding data.")
    # btn0 = st.sidebar.button('Show Overall Analysis')
    # if btn0:
    load_overall_analysis()

elif option == 'Startup Analysis':
    st.title("Startup Analysis")
    st.write("This section provides an analysis of individual startups.")
    st.sidebar.selectbox('Select Startup', sorted(df['Startup'].unique().tolist()))
    btn1 =st.sidebar.button('Find Startup Details')

else:
    # st.title("Investor Analysis")
    # st.write("This section provides an analysis of different investors.")
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['Investors'].str.split(',').sum())))
    btn2 =st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
