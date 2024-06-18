import streamlit as st
import pandas as pd
import datetime 
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu


st.set_page_config(layout='wide',page_title='EDA',page_icon='bar_chart')

with st.sidebar:
    
    st.header(' Input data')


    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is None:
    st.title('Watch Demo till the file is being uploaded')
    video_file = open('streamlit-webapplication-2024-06-08-23-06-27.mp4', 'rb')
    video_bytes = video_file.read()
    
    st.video(video_bytes)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=False)
    import json 
    import requests 
    from streamlit_lottie import st_lottie 
  
    url = requests.get( 
    "https://lottie.host/0b8efe05-edaf-4e86-b24c-b371363a9a31/w5jXb7Rp4k.json") 

    url_json = dict() 
  
    if url.status_code == 200:
        url_json = url.json() 
    else: 
        print("Error in the URL") 
  
  
    col20,col21=st.columns([1,9])
  
    with col20:
        st_lottie(url_json,height=100,width=100)

    with col21:
      
        st.title('Analyzing the Top 10 Seller Countries')
    selected=option_menu(menu_title=None,options=['Choropleth Chart','Bar Chart'],orientation='horizontal')
    
    if selected=='Choropleth Chart':
    
        col1,col2=st.columns(2)
    
        with col1:
             
            country_counts = df['seller_country'].value_counts().reset_index()
            country_counts.columns = ['Country', 'Count']
            fig24 = px.choropleth(country_counts, 
                                locations='Country', 
                                locationmode='country names', 
                                color='Count',
                                color_continuous_scale='viridis',
                                title='Seller Distribution by Country')
            fig24.update_layout(geo=dict(showframe=False, 
                                        projection_type='equirectangular'),
                            coloraxis_colorbar=dict(title='Count'))
            st.plotly_chart(fig24)
    
        with col2:
             product_category = df.groupby('seller_country')['product_category'].agg(lambda x: x.value_counts().idxmax()).reset_index()
             fig = px.choropleth(
             product_category,
             locations='seller_country',
             locationmode='country names',
             color='product_category',
             title='Most Common Product Category by Country',
             color_continuous_scale=px.colors.sequential.Plasma)
             st.plotly_chart(fig)
             
        col3,col4=st.columns(2)
             
        with col3:
            badge_mode = df.groupby('seller_country')['seller_badge'].agg(lambda x: x.value_counts().idxmax()).reset_index()
            fig = px.choropleth(
            badge_mode,
            locations='seller_country',
            locationmode='country names',
            color='seller_badge',
            title='Most Common Seller Badge by Country',
            color_continuous_scale=px.colors.sequential.Plasma,)
            fig.update_layout(width=650)
            st.plotly_chart(fig)
    
        with col4:
            product_season = df.groupby('seller_country')['product_season'].agg(lambda x: x.value_counts().idxmax()).reset_index()
            fig = px.choropleth(
            product_season,
            locations='seller_country',                
            locationmode='country names',
            color='product_season',
            title='Most Common Product Season by Country',
            color_continuous_scale=px.colors.sequential.Plasma)
            st.plotly_chart(fig)
    
    
    if selected=='Bar Chart':
        st.subheader('Product Condition')
        top_10_countries = df['seller_country'].value_counts().nlargest(10).index
        fig2 = make_subplots(rows=5, cols=2, subplot_titles=[f"Condition of products in {country}" for country in top_10_countries],vertical_spacing=0.12)
        for idx, specific_country in enumerate(top_10_countries):
    
            country_df = df[df['seller_country'] == specific_country]
            product_counts = country_df['product_condition'].value_counts()
            top_10_products = product_counts.nlargest(10)
            bar_chart = go.Bar(x=top_10_products.index, y=top_10_products.values, name=specific_country)
            fig2.add_trace(bar_chart, row=(idx // 2) + 1, col=(idx % 2) + 1)
    
        fig2.update_layout(height=650, width=1400, title_text="Condition of Product in Each Country")
        st.plotly_chart(fig2)
    
        st.subheader('Shipping Time Analysis')
        fig3 = make_subplots(rows=5, cols=2, subplot_titles=[f"Shipping Time Analysis in {country}" for country in top_10_countries])
        for idx, specific_country in enumerate(top_10_countries):
        
            country_df = df[df['seller_country'] == specific_country]
            product_counts = country_df['usually_ships_within'].value_counts()
            top_10_products = product_counts.nlargest(10)
            bar_chart = go.Bar(x=top_10_products.index, y=top_10_products.values, name=specific_country)
            fig3.add_trace(bar_chart, row=(idx // 2) + 1, col=(idx % 2) + 1)
        fig3.update_layout(height=650, width=1400, title_text="Top 10 Products Produced in Each Country")
        st.plotly_chart(fig3)
    
        st.subheader('Price Analysis')
        top_10_countries = df['seller_country'].value_counts().nlargest(10).index
        filtered_df = df[df['seller_country'].isin(top_10_countries)]
        average_prices = filtered_df.groupby('seller_country')[['price_usd', 'seller_price', 'seller_earning', 'buyers_fees']].mean().reset_index()
        average_prices_melted = average_prices.melt(id_vars='seller_country', var_name='price_type', value_name='average_price')
        fig = px.bar(
            average_prices_melted,
            x='seller_country',
            y='average_price',
            color='price_type',
            title='Average Prices in Top 10 Countries',
            labels={'seller_country': 'Country', 'average_price': 'Average Price', 'price_type': 'Price Type'},
            barmode='group'
        )
        fig.update_layout(xaxis_tickangle=-45,height=500,width=1400)
        st.plotly_chart(fig)
    
        st.subheader('Top 10 Products Analysis')
        top_10_countries = df['seller_country'].value_counts().nlargest(10).index
        fig = make_subplots(rows=5, cols=2, subplot_titles=[f"Top 10 Products Produced in {country}" for country in top_10_countries],vertical_spacing=0.15)
        for idx, specific_country in enumerate(top_10_countries):
    
                country_df = df[df['seller_country'] == specific_country]
                product_counts = country_df['product_type'].value_counts()
                top_10_products = product_counts.nlargest(10)
                bar_chart = go.Bar(x=top_10_products.index, y=top_10_products.values, name=specific_country)
                fig.add_trace(bar_chart, row=(idx // 2) + 1, col=(idx % 2) + 1)
        fig.update_layout(height=1000, width=1400, title_text="Top 10 Products Produced in Each Country")
        st.plotly_chart(fig)
