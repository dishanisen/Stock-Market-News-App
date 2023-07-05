
#!pip install streamlit
#!pip install plotly

import requests
import json
import streamlit as st
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Define Alpha Vantage API endpoint
endpoint = 'https://www.alphavantage.co/query'

# Define API parameters
params = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': '',
    'outputsize': 'compact',
    'apikey': '0SWBJ74SGZYNKVLQ'
}

# Define News API endpoint and parameters
news_endpoint = 'https://newsapi.org/v2/everything'
news_params = {
    'q': '',
    'apiKey': 'a12542d7be1f42aba0c3ca0d95c327fd',
    'pageSize': 10
}

# Define Streamlit app
def app():
    # Define app title
    st.title('Stock Price Projections')
    
    # Define user input fields
    stock_name = st.text_input('Enter stock name (e.g. AAPL)')
    days_back = st.slider('Select time period (days)', 1, 30, 7)
    
    # Retrieve stock data from API
    if stock_name:
        params['symbol'] = stock_name
        response = requests.get(endpoint, params=params)
        data = json.loads(response.text)
        
        # Create time series graph
        dates = list(data['Time Series (Daily)'].keys())[:days_back][::-1]
        prices = [float(data['Time Series (Daily)'][date]['4. close']) for date in dates]
        fig_dict = {
            'data': [{'x': dates, 'y': prices}],
            'layout': {'title': f'{stock_name} Stock Prices'}
        }
        st.plotly_chart(fig_dict)
        
        # Retrieve latest news articles about stock or company
        news_params['q'] = stock_name
        news_response = requests.get(news_endpoint, params=news_params)
        news_data = json.loads(news_response.text)
        
        # Display news feed in app
        st.subheader('Latest news articles about this stock/company:')
        for article in news_data['articles']:
            st.write(f"{article['title']} ({article['source']['name']})")
            st.write(article['description'])
            st.write(article['url'])
            st.write('\n')
# Call app function to start Streamlit app
app()

"""Made with love, by Dishani

"""