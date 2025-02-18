import streamlit as st
import pandas as pd

#names_link = 'dataset.csv'

#names_data = pd.read_csv(names_link)

st.title('My streamlit app')
#st.dataframe(names_data)


sidebar = st.sidebar
sidebar.title('Esta es la barra lateral')
sidebar.write('Aquí van los elementos de entrada')

st.header('Informacion sobre el conjunto de datos')
st.header('Descripción de los datos')

st.write("""
         
         Este es un simple ejemplo de una app para predecir.
         ¡Esta app predice mis datos!

         """)


