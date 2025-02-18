import pandas as pd
import streamlit as st
import numpy as np

#Create title to the web app
st.title('My first streamlit app')


#Dataset names
names_link = 'dataset.csv'
names_data = pd.read_csv(names_link)

st.dataframe(names_data)

#Cache
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(names_link, nrows=nrows)
    return data    

# Welcome message
def bienvenida (nombre):
    mymensaje = "Bienvenido/a : " + nombre
    return mymensaje

myname = st.text_input('Enter your name')
if (myname):
    mensaje = bienvenida(myname)
    st.write(f" {mensaje} ")

#Control Button
if st.button('Search'):
    st.write('Has presionado el boton de busqueda')

#Selectedbox
selected_sex = st.selectbox("Select sex", names_data["sex"].unique())
st.write(f'selected option: {selected_sex!r}')
filtered_data_sex = names_data[names_data['sex'] == selected_sex ]

#Sidebar
sidebar = st.sidebar
sidebar.title('This is the sidebar')

#U can add any elemnts to the sidebar
sidebar.image('ilian.jpeg')
sidebar.write('Ilian Jesus Orduña Herrera')
sidebar.write('zs22004363')