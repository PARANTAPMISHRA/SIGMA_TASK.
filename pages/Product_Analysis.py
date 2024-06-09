import streamlit as st
import pandas as pd
import datetime 
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


st.set_page_config(layout='wide',page_title='EDA',page_icon='bar_chart')
st.title('Analyzing the most common products')
with st.sidebar:
    
    st.header(' Input data')


    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=False)
    selected=option_menu(menu_title=None,options=['Product Popularity','Average Price and Category','Product Condition and Seasonality Analysis'],orientation='horizontal')
    
    value_count=df['product_type'].value_counts()
    product_type_to_analyze = value_count.index[0:10]
    
    if selected=='Product Popularity':
        fig15=px.bar(x=value_count.index[0:10], y=value_count.values[0:10], color=value_count.values[0:10],color_discrete_sequence='agsunset',title='Top 10 Products',labels={'x':'Product','y':'Count'})
        fig15.update_layout(xaxis_tickangle=-45,width=1000)
        st.plotly_chart(fig15)
        
    
        st.title("Product Like Count Analysis")
        
        selected_product_type = st.selectbox("Select a product type", product_type_to_analyze)
    
        
        filtered_df = df[df['product_type'] == selected_product_type]
    
        
        like_data = filtered_df['product_like_count']
    
        
        fig = px.scatter(filtered_df, x='price_usd',y='product_like_count',color='product_like_count',color_continuous_scale='blugrn',
                        title=f'{selected_product_type} Product Like Count Distribution',
                        labels={'price_usd': 'Price (USD)', 'product_like_count': 'Product Like Count'})
    
        
        fig.update_layout(xaxis_title='Price (USD)', yaxis_title='Product Like Count',
                        template='plotly_white',width=1000)
    
        
        st.plotly_chart(fig)
    
    
    if selected=='Average Price and Category':
    
        
        filtered_df = df[df['product_type'].isin(product_type_to_analyze)]
        
        average_prices = filtered_df.groupby('product_type')[['price_usd', 'seller_price', 'seller_earning', 'buyers_fees']].mean().reset_index()
    
        
        average_prices_melted = pd.melt(average_prices, id_vars='product_type', var_name='price_type', value_name='average_price')
    
        
        fig17 = px.bar(average_prices_melted, x='product_type', y='average_price', color='price_type', barmode='group',
                    title='Average Prices of Top 10 Brands', labels={'product_type': 'Product Category', 'average_price': 'Average Price'})
    
        
        fig17.update_layout(xaxis_tickangle=-45, legend_title_text='Price Type')
        st.plotly_chart(fig17)
    
        
        st.title("Product Category Distribution Analysis")
    
        
        selected_product_type = st.selectbox("Select a product type", product_type_to_analyze)
    
        
        filtered_df = df[df['product_type'] == selected_product_type]
    
        
        product_category_counts = filtered_df['product_category'].value_counts()
    
        
        fig_bar = px.bar(product_category_counts, x=product_category_counts.index, y=product_category_counts.values,
                        labels={'index': 'Product Category', 'y': 'Count'},
                        title=f'{selected_product_type} Product Category Distribution',color=product_category_counts.values,color_continuous_scale='emrld')
    
        
        fig_bar.update_layout(xaxis_title='Product Category', yaxis_title='Count',
                            template='plotly_white')
    
    
        fig_pie = px.pie(product_category_counts, values=product_category_counts.values, names=product_category_counts.index,
                        title=f'{selected_product_type} Product Category Distribution',
                        labels={'index': 'Product Category', 'values': 'Count'},hole=0.5,color_discrete_sequence=px.colors.sequential.Oryel)
    
        
        fig_pie.update_layout(template='plotly_white')
        col1,col2=st.columns(2)
        
        with col1:
    
            st.plotly_chart(fig_bar)
        with col2:
    
            st.plotly_chart(fig_pie)
    if  selected=='Product Condition and Seasonality Analysis':
        selected_product_type = st.selectbox("Select a product type", product_type_to_analyze)
        
        
        col1,col2=st.columns(2)
        
        
        with col1:
            st.subheader("Product Condition Distribution Analysis")
            
            filtered_df = df[df['product_type'] == selected_product_type]
    
            
            condition_data = filtered_df['product_condition']
    
            
            fig = px.histogram(filtered_df, x='product_condition', 
                            color_discrete_sequence=['skyblue'], 
                            title=f'{selected_product_type} Product Condition Distribution',
                            labels={'product_condition': 'Product Condition', 'count': 'Frequency'})
    
            
            fig.update_layout(xaxis_title='Product Condition', yaxis_title='Frequency')
    
            
            st.plotly_chart(fig)
    
    
        with col2:
            st.subheader("Product Season Distribution Analysis")
            
            product_season_counts = filtered_df['product_season'].value_counts()
    
            
            fig = px.pie(product_season_counts, values=product_season_counts.values, names=product_season_counts.index,
                        title=f'{selected_product_type} Product Season Distribution',
                        labels={'index': 'Product Season', 'values': 'Count'},hole=0.5)
    
            
            fig.update_layout(template='plotly_white')
    
            
            st.plotly_chart(fig)


