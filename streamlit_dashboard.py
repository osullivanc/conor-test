
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

# Connect to the SQLite database
conn = sqlite3.connect('prototype_data_aggregator.sqlite')

# Title and Description
st.title('Climate and Energy Data Dashboard')
st.write('Explore data on economic losses from climate events and power generation capacity across the EU.')

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Economic Losses", "Power Capacity"])

# Economic Losses Page
if page == "Economic Losses":
    st.header("Economic Losses from Climate Events")
    
    # Query economic losses data
    query = "SELECT geo AS Country, SUM(obs_value) AS Total_Losses, MIN(time) AS Start_Year, MAX(time) AS End_Year FROM economic_losses GROUP BY geo;"
    losses_data = pd.read_sql_query(query, conn)
    
    # Display data
    st.subheader("Summary Table")
    st.dataframe(losses_data)
    
    # Visualization
    st.subheader("Total Economic Losses by Country (1980-2023)")
    plt.figure(figsize=(10, 6))
    plt.bar(losses_data['Country'], losses_data['Total_Losses'] / 1e3, color='red')
    plt.xlabel('Country')
    plt.ylabel('Total Losses (Billion EUR)')
    plt.title('Economic Losses from Climate Events (1980-2023)')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Power Capacity Page
if page == "Power Capacity":
    st.header("Power Generation Capacity")
    
    # Query power capacity data
    query = "SELECT country AS Country, technology AS Technology, SUM(capacity) AS Total_Capacity FROM power_capacity GROUP BY country, technology;"
    capacity_data = pd.read_sql_query(query, conn)
    
    # Display data
    st.subheader("Summary Table")
    st.dataframe(capacity_data)
    
    # Visualization
    st.subheader("Top 10 Technologies by Total Capacity")
    top_technologies = capacity_data.groupby("Technology").sum().sort_values(by="Total_Capacity", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.bar(top_technologies.index, top_technologies['Total_Capacity'] / 1e3, color='blue')
    plt.xlabel('Technology')
    plt.ylabel('Total Capacity (GW)')
    plt.title('Top 10 Technologies by Capacity')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Close database connection
conn.close()
