import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
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

#Dataset titanic
titanic_link = 'titanic.csv'
titanic_data = pd.read_csv(titanic_link)

#Sidebar
sidebar = st.sidebar
sidebar.title('This is the sidebar')

#U can add any elemnts to the sidebar
sidebar.image('ilian.jpeg')
sidebar.write('Ilian Jesus Orduña Herrera')
sidebar.write('zs22004363')

#Give user current date
today = datetime.date.today()
today_date = sidebar.date_input('Current date', today)
st.success('Current date: %s' % str(today_date))


#Checkbox 
#Display the dataset if the user select the checkbox
agree = sidebar.checkbox('Show dataset Overview')
if agree:
    st.dataframe(titanic_data)

#Radio
#Select the emabark townn of the passenger and display the data with this selection
selected_town = st.radio("Select the embark town",
                            titanic_data['embark_town'].unique())
st.write('Select embark town:', selected_town)

st.write(titanic_data.query(f"""embark_town ==@selected_town"""))
st.markdown('___')

# SLIDER 
# Select a range of the fare and then display the dataset 
optionals = st.expander("optionals Configurations", True)
fare_min = optionals.slider(
    "Minimum fare",
    min_value=float(titanic_data['fare'].min()),
    max_value=float(titanic_data['fare'].max()),
)

fare_max = optionals.slider(
    "Maximum fare",
    min_value=float(titanic_data['fare'].min()),
    max_value=float(titanic_data['fare'].max()),
)

subset_fare = titanic_data[(titanic_data['fare'] <= fare_max) & (fare_min <= titanic_data['fare'])]

#Display of the dataset
st.dataframe(subset_fare)


#GRAPHS
fig, ax = plt.subplots()
ax.hist(titanic_data.fare)
st.header("Histograma del titanic")
st.pyplot(fig)


#Second graph
fig2, ax2 = plt.subplots()
y_pos = titanic_data['class']
x_pos = titanic_data['fare']

ax2.barh(y_pos, x_pos)
ax2.set_ylabel('Class')
ax2.set_xlabel('Fare')
ax2.set_title('¿Cuanto pagaron las clases del Titanic?')

st.header ("Grafica de barras del titanic")
st.pyplot(fig2)


#Third graph
fig3, ax3 = plt.subplots()  

ax3.scatter(titanic_data.age, titanic_data.fare)
ax3.set_xlabel('Age')
ax3.set_ylabel('Fare')

st.header("Grafica de dispersion del titanic")
st.pyplot(fig3)

#Maps
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)

