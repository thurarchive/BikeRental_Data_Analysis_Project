import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.cluster import KMeans
from datetime import datetime

sns.set(style='darkgrid')

# Load Data
@st.cache
def load_data():
    day = pd.read_csv('main_data.csv')
    day['dteday'] = pd.to_datetime(day['dteday'])
    day['year'] = day['yr'].map({0: 2011, 1: 2012})
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day['season_name'] = day['season'].map(season_map)
    weather_mapping = {
        1: 'Clear',
        2: 'Mist',
        3: 'Light Snow',
        4: 'Heavy Rain, Snow-Fog'
    }
    day['weathersit'] = day['weathersit'].replace(weather_mapping)
    return day

day = load_data()

# Helper Functions
def plot_rentals_by_season(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='season_name', y='cnt', hue='year', data=df, ax=ax)
    ax.set_title('Bike Rentals by Season and Year')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Rentals')
    ax.legend(title='Year')
    return fig

def plot_monthly_users(df):
    df['month'] = df['mnth'].map({
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
        6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
        11: "November", 12: "December"
    })
    monthly_users = df.groupby('month')[['casual', 'registered']].mean()
    monthly_users = monthly_users.reindex([
        "January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December"
    ])
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(monthly_users.index, monthly_users["casual"], marker='o', linewidth=2, color="#72BCD4", label="Casual")
    ax.plot(monthly_users.index, monthly_users["registered"], marker='o', linewidth=2, color="#FF6347", label="Registered")
    ax.set_title("Average Daily Rentals by User Type and Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Rentals")
    plt.xticks(rotation=45)
    ax.legend()
    return fig

def plot_user_types_by_holiday(df):
    if df.empty:
        return plt.figure()  # Return an empty figure if data is empty
    holiday_comparison = df.groupby('holiday')[['casual', 'registered']].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    holiday_comparison.plot(kind='bar', ax=ax)
    ax.set_title('Average Rentals by User Type: Holiday vs Non-Holiday')
    ax.set_xlabel('Comparison')
    ax.set_ylabel('Average Rentals')
    ax.set_xticklabels(['Non-Holiday', 'Holiday'], rotation=0)
    ax.legend(['Casual', 'Registered'])
    return fig

def plot_weather_analysis(df):
    if df.empty:
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.text(0.5, 0.5, "No data available for the selected filters", 
                ha='center', va='center', fontsize=20)
        ax.set_axis_off()
        return fig

    weather_analysis = df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(20, 10))
    bars = ax.bar(weather_analysis.index, weather_analysis.values, width=0.6)
    
    ax.set_title('Average Daily Rentals by Weather Situation', fontsize=20, pad=20)
    ax.set_xlabel('Weather Situation', labelpad=20, fontsize=15)
    ax.set_ylabel('Average Number of Rentals', fontsize=16)
    
    ax.set_xticks(range(len(weather_analysis)))
    ax.set_xticklabels(weather_analysis.index, rotation=0, ha='center', fontsize=12)
    plt.tight_layout()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    
    ax.set_facecolor('#f0f0f0')
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom', fontsize=14)

    return fig

def plot_temperature_vs_rentals(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    for year in df['year'].unique():
        year_data = df[df['year'] == year]
        sns.regplot(x='temp', y='cnt', data=year_data, scatter=False, label=str(year), ax=ax)
    ax.scatter(df['temp'], df['cnt'], alpha=0.3)
    ax.set_title('Temperature vs Total Rentals by Year')
    ax.set_xlabel('Normalized Temperature')
    ax.set_ylabel('Total Rentals')
    ax.legend()
    return fig

def plot_weekly_rentals(df):
    df['dayofweek'] = df['dteday'].dt.dayofweek
    weekly_pattern = df.groupby('dayofweek')[['casual', 'registered']].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    weekly_pattern.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Average Daily Rentals by Day of Week and User Type')
    ax.set_xlabel('Day of Week (0 = Monday, 6 = Sunday)')
    ax.set_ylabel('Average Rentals')
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    ax.legend(['Casual', 'Registered'])
    return fig

def plot_clusters(df):
    features = ['temp', 'hum', 'windspeed', 'cnt']
    X = df[features]
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=df, x='temp', y='cnt', hue='Cluster', palette='viridis', ax=ax)
    ax.set_title('Bike Rentals Clusters based on Temperature and Count')
    return fig

# Streamlit Layout
st.title('Bike Rentals Dashboard')
st.sidebar.header('Filters')
year_filter = st.sidebar.multiselect('Select Year', options=day['year'].unique(), default=day['year'].unique())
weather_filter = st.sidebar.multiselect('Select Weather', options=day['weathersit'].unique(), default=day['weathersit'].unique())
season_filter = st.sidebar.multiselect('Select Season', options=day['season_name'].unique(), default=day['season_name'].unique())

filtered_data = day[
    (day['year'].isin(year_filter)) &
    (day['weathersit'].isin(weather_filter)) &
    (day['season_name'].isin(season_filter))
]

if st.sidebar.checkbox('Show DataFrame'):
    st.subheader('Filtered Data')
    st.write(filtered_data)

st.subheader('Bike Rentals by Season and Year')
st.pyplot(plot_rentals_by_season(filtered_data))

st.subheader('Average Daily Rentals by User Type and Month')
st.pyplot(plot_monthly_users(filtered_data))

st.subheader('Comparison of User Types on Holidays vs Working Days')
st.pyplot(plot_user_types_by_holiday(filtered_data))

st.subheader('Average Daily Rentals by Weather Situation')
st.pyplot(plot_weather_analysis(filtered_data))

st.subheader('Temperature vs Total Rentals by Year')
st.pyplot(plot_temperature_vs_rentals(filtered_data))

st.subheader('Average Daily Rentals by Day of Week and User Type')
st.pyplot(plot_weekly_rentals(filtered_data))

st.subheader('Bike Rentals Clusters based on Temperature and Count')
st.pyplot(plot_clusters(filtered_data))

st.caption('Copyright © Fajri Fathur Rahman 2024')