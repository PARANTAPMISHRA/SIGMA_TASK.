import streamlit as st
import pandas as pd
import datetime 
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
st.set_page_config(layout='wide',page_title='EDA',page_icon='bar_chart')




with st.sidebar:
    
    st.header(' Input data')


    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=False)
    st.header('Analyzing top 10 Brands')
    
    selected=option_menu(menu_title=None,options=['Brand Popularity','Average Price and Sales','Top Product'],orientation='horizontal')
    
    
    top_n_brands = 10
    
            
    brand_counts = df['brand_name'].value_counts().head(top_n_brands)
    
            
    top_brands_df = df[df['brand_name'].isin(brand_counts.index)]
    top_brands_stats = pd.DataFrame({'Name': brand_counts.index,'Count': brand_counts.values})
    top_brands_stats.sort_values(by='Name',ascending=True,inplace=True)
    
    brand_count=top_brands_stats[['Name','Count']]
    
            
    top_brands = brand_count['Name']  
    
            
    filtered_df = df[df['brand_name'].isin(top_brands)]
    if selected == 'Brand Popularity':
        
    
        col1,col2=st.columns(2)
    
    
        with col1:
            brand_popularity = df['brand_name'].value_counts().head(10)
            
            fig7 = px.bar(x=brand_popularity.index, y=brand_popularity.values, 
                        labels={'x': 'Brand Name', 'y': 'Number of Products'}, 
                        title='Brand Popularity',color=brand_popularity.values,color_continuous_scale='viridis')
            fig7.update_xaxes(tickangle=90)
            st.plotly_chart(fig7)
    
    
        with col2:
            
            average_ratings = filtered_df.groupby('brand_name')['product_like_count'].mean()
    
            
            average_ratings = average_ratings.reindex(top_brands)
    
            fig12=px.bar(x=average_ratings.index,y=average_ratings.values,color=average_ratings.values,color_continuous_scale='viridis',title='Average Product Ratings')
            fig12.update_layout(xaxis_tickangle=-90)
            fig12.add_trace(go.Scatter(x=average_ratings.index,y=average_ratings.values,name='Trend Line',line=dict(color='royalblue')))
            st.plotly_chart(fig12)
    
    
    if selected=='Average Price and Sales':
        top_brands = brand_count['Name']
        filtered_df = df[df['brand_name'].isin(top_brands)]
    
        col1,col2=st.columns(2)
            
        with col1:
            average_prices = filtered_df.groupby('brand_name')[['price_usd', 'seller_price', 'seller_earning', 'buyers_fees']].mean()
    
            fig14 = px.bar(average_prices,title='Average Prices based on Product Type', labels={'brand_name': 'Brand', 'y': 'Average Price','variable':'Price Type'},color_discrete_sequence='aggrnyl')
            fig14.update_layout(xaxis_tickangle=-45, legend_title_text='Price Type',width=680)
    
            st.plotly_chart(fig14)
    
        with col2:
            
            brand_performance = filtered_df.groupby('brand_name')[['sold', 'reserved', 'available', 'in_stock', 'should_be_gone']].sum()
            fig13 = px.bar(brand_performance,title='Performance of Top 10 Brands', labels={'brand_name': 'Brand', 'y': 'Count','variable':'Performance'},color_discrete_sequence='aggrnyl')
            st.plotly_chart(fig13)
    
    
    if selected=='Top Product':
        
    
        col1,col2=st.columns(2)
    
    
        st.title("Brand Product Distribution")
        name_of_brands = brand_count['Name']
        selected_brand = st.selectbox("Select a brand", name_of_brands)
        filtered_df = df[df['brand_name'] == selected_brand]
        product_data = filtered_df['product_type'].value_counts().head(10)
    
        fig = px.bar(x=product_data.index, y=product_data.values,
                    labels={'x': 'Product', 'y': 'Frequency'},
                    title=f'Top 10 Product Distribution for {selected_brand}',color_discrete_sequence='purpor')
        fig.update_xaxes(tickangle=90)
    
        with col1:
            st.plotly_chart(fig)
    
    
        product_data = filtered_df['product_category'].value_counts().head(10)
    
        
        fig = px.funnel_area(names=product_data.index, values=product_data.values,
                    labels={'names': 'Gender', 'values': 'Frequency'},
                    title=f'Category Target of {selected_brand}',color_discrete_sequence='purpor')
        fig.update_xaxes(tickangle=90)
    
        with col2:
            st.plotly_chart(fig)
    
        col3,col4=st.columns(2)
        product_data = filtered_df['product_season'].value_counts().head(10)
    
        
        fig = px.pie(names=product_data.index, values=product_data.values,
                    labels={'names': 'Season', 'values': 'Frequency'},
                    title=f'{selected_brand} Season Distribution',hole=0.5)
    
        
        with col3:
            st.plotly_chart(fig)
    
    
        product_data = filtered_df['product_condition'].value_counts().head(20)
    
        
        fig = px.line(x=product_data.index, y=product_data.values,
                    labels={'x': 'Condition', 'y': 'Frequency'},
                    title=f'Top 10 Product Condition Analysis of {selected_brand}',markers=True)
        fig.update_xaxes(tickangle=90)
        
        
        with col4:
            st.plotly_chart(fig)
