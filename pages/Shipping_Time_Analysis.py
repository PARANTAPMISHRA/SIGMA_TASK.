import streamlit as st
import pandas as pd
import datetime 
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


st.set_page_config(layout='wide',page_title='EDA',page_icon='bar_chart')
st.title('Shipping Time Analysis')
with st.sidebar:
    
    st.header(' Input data')


    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col=False)
    value_count = df['usually_ships_within'].value_counts().reset_index()
    value_count.columns = ['shipping_time', 'Count']
    
    col1,col2=st.columns(2)
    
    with col1:
    
        fig20 = px.bar(value_count, 
                    x='shipping_time', 
                    y='Count', 
                    title='Distribution of Shipping Times',
                    labels={'shipping_time': 'Shipping Time', 'Count': 'Count'},
                    color='shipping_time',
                    color_continuous_scale='Viridis')
    
        
        fig20.update_layout(xaxis_tickangle=-90,width=670)
        st.plotly_chart(fig20)
    
    with col2:
        category_feature1 = 'usually_ships_within'  
        category_feature2 = 'product_category'  
    
        
        fig21 = px.histogram(df, 
                        x=category_feature2, 
                        color=category_feature1, 
                        barmode='group',
                        title='Count of Shipping Times by Product Category',
                        labels={category_feature2: 'Product Category', 'count': 'Count', category_feature1: 'Shipping Time'},
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    
        
        fig21.update_layout(xaxis_tickangle=-45, 
                        yaxis_title='Count', 
                        xaxis_title='Product Category')
        st.plotly_chart(fig21)
    
    
    category_feature1 = 'usually_ships_within'  
    category_feature2 = 'warehouse_name'  
    
    
    fig22 = px.histogram(df, 
                       x=category_feature2, 
                       color=category_feature1, 
                       barmode='group',
                       title='Count of Shipping Times by Warehouse Name',
                       labels={category_feature2: 'Warehouse Name', 'count': 'Count', category_feature1: 'Shipping Time'})
    
    
    fig22.update_layout(xaxis_tickangle=-45, 
                      yaxis_title='Count', 
                      xaxis_title='Warehouse Name',width=1200)
    st.plotly_chart(fig22)


