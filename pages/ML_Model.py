import streamlit as st
import pandas as pd
import datetime 
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
st.set_page_config(layout='wide',page_title='EDA',page_icon='bar_chart')
st.title('Machine Learning Model To Predict Price')
import joblib
seller_price,seller_earning,product_like_count,product_type,product_category,product_season,brand_name,product_material,product_color,product_condition,warehouse,seller_badge,shipping_time,seller_country=joblib.load('unique_values_data.joblib')
def user_input():
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _product_type=st.selectbox("Product Type",product_type)
    with col2:
        _product_category=st.selectbox("Product Category",product_category)
    with col3:
        _product_season=st.selectbox("Product Season",product_season)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _brand_name=st.selectbox("Brand Name",brand_name)
    with col5:
        _product_material=st.selectbox("Product Materia;",product_material)
    with col6:
        _product_color=st.selectbox("Product Color",product_color)
    col9,col10,col11,col12=st.columns(4)
    with col7:
        _product_condition=st.selectbox("Product Condition",product_condition)
    with col8:
        _warehouse=st.selectbox("Warehouse",warehouse)
    with col9:
        _seller_badge=st.selectbox("Seller Badge",seller_badge)
    st.balloons()
    with col10:
        _shipping_time=st.selectbox("Shipping Time",shipping_time)
    with col11:
        _seller_country=st.selectbox("Selller Contry",seller_country)
    with col12:
        _in_stock=st.selectbox("In Stock",['True','False'])
    col13,col14,col15,col16=st.columns(4)
    with col13:
        _seller_price=st.number_input('Seller Price')
    with col14:
        _seller_earning=st.number_input("Seller Earning")
    with col15:
        _buyers_fees=st.number_input("Buyers Fees")
    with col16:
        _product_like_count=st.number_input("Product Like Count")
    input_data={'product_type':_product_type,
                'product_category':_product_category,
                'product_season':_product_season,
                'product_condition':_product_condition,
                'product_like_count':_product_like_count,
                'in_stock':_in_stock,
                'brand_name':_brand_name,
                'product_material':_product_material,
                'product_color':_product_color,
                'seller_price':_seller_price,
                'seller_earning':_seller_earning,
                'seller_badge':_seller_badge,
                'buyers_fees':_buyers_fees,
                'warehouse_name':_warehouse,
                'usually_ships_within':_shipping_time,
                'seller_country':_seller_country
                }
    input_dataframe=pd.DataFrame(input_data,index=[0])
    st.table(input_dataframe)
    return input_data
X=user_input()
st.write('----')
import pickle
with open('saved_model_ (1).pkl', 'rb') as f:
    model=pickle.load(f)
with open('label_encoders_.pkl', 'rb') as f:
    loaded_label_encoders=pickle.load(f)
with open('scaler_.pkl', 'rb') as file:
    loaded_scalers = pickle.load(file)
def process_user_input(user_input, label_encoders, scalers):
    processed_input = {}
    for feature, value in user_input.items():
        if feature in label_encoders:
            processed_input[feature] = label_encoders[feature].transform([value])[0]
        elif feature in scalers:
            processed_input[feature] = scalers[feature].transform([[value]])[0][0]
        else:
            processed_input[feature] = value
    return processed_input
def predict_price(user_input, model, label_encoders, scalers):
    processed_input = process_user_input(user_input, label_encoders, scalers)
    input_df = pd.DataFrame([processed_input])
    prediction = model.predict(input_df)
    return prediction[0]

user_input = X
predicted_price = predict_price(user_input, model, loaded_label_encoders, loaded_scalers)
col1,col2= st.columns(2)
with col1:
    st.metric(label='Price in USD',value=predicted_price)
with col2:
  with st.expander('About this app'):
    st.markdown('**Model Used for Prediction**')
    st.info('Linear Regression')

    st.markdown('**Model Performance on Test Dataset**')
    st.image('Model_performace.png')

    st.markdown('**Feature Dependencies**')
    st.image('Feature_dependencies.png')
    
    st.markdown('Libraries used:')
    st.code('''- Pandas for data wrangling
    - Scikit-learn for building a machine learning model
    - Altair for chart creation
    - Streamlit for user interface
    ''', language='markdown')
