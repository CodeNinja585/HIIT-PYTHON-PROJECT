import streamlit as st
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


#load data
@st.cache_data
def load_data():
    
    df = pd.read_csv("africa_food_prices.csv") # original data frame    
    st.title("Africa Food Prices App")
    
    # data cleaning
    df['state'] = df['state'].fillna("null") #replacing the values null values in with "null"
    df = df.drop('currency_id', axis=1) #removing the currency_id    
    df = df.drop('Unnamed: 0', axis=1) #looking at the Unnamed column, I fail to see its significance so, I'll go ahead and drop it
    df = df.drop('mp_commoditysource', axis=1)    
    df['month'] = df['month'].astype(str) # changing the month from int to text
    month_map = {
    '1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'April',
    '5': 'May', '6': 'June', '7': 'July', '8': 'Aug',
    '9': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    df['month'] = df['month'].map(month_map)
    
    # Calculate price per unit
    price_per_unit = df['price'] / df['um_unit_id']  
    # add new column to the data frame
    df['price_per_unit'] = price_per_unit
    #return clean df
    return df


df = load_data()
st.write(df.head(3))

st.sidebar.title("Filters")
years = df['year'].unique().tolist()
selected_year = st.sidebar.selectbox('Select Year', years)

# Filter dataframe based on the selected year
filtered_year_df = df[df['year'] == selected_year]

# Display filtered data 
st.write(f'Data for the year {selected_year} ({len(filtered_year_df)} records)')
st.dataframe(filtered_year_df)

# Calculations

# Calculate total number of unique produce types
total_produce_count = df['produce'].nunique()

# Display the total number of produce types
st.write(f'Total Number of Produce Types: {total_produce_count}')


# Calculate average price per produce type for selected year
average_price_per_produce = df[df['year'] == selected_year].groupby('produce')['price'].mean().reset_index()

# Display average prices
st.subheader(f'Average Price per Produce Type for Year {selected_year}')
st.dataframe(average_price_per_produce)


# Count of records by year this data shows which year has the most distribution power
#.reset_index(): Resets the index of the resulting series to turn it into a DataFrame.
records_count_by_year = df['year'].value_counts().reset_index()

# Rename columns for clarity
records_count_by_year.columns = ['Year', 'Record Count']

# Display in a bar chart
st.subheader('Count of Records by Year')
st.bar_chart(records_count_by_year.set_index('Year'))

#Visualizations
st.set_option('deprecation.showPyplotGlobalUse', False)
st.subheader('Histogram of Price Distribution')
plt.hist(df['price'], bins=20, edgecolor='black')
plt.xlabel('Price')
plt.ylabel('Frequency')
st.pyplot()

# Disable the warning for pyplot global use
st.set_option('deprecation.showPyplotGlobalUse', False)
st.subheader('Mean Price Over Years')
mean_price_by_year = df.groupby('year')['price'].mean()
plt.plot(mean_price_by_year.index, mean_price_by_year.values, marker='o')
plt.xlabel('Year')
plt.ylabel('Mean Price')
plt.grid(True)
st.pyplot()


# Calculate average price by country
average_prices = df.groupby('country')['price'].mean().reset_index()
