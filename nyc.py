import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("NYC Bike Data")

# Read and show the data with the selected number of rows
@st.cache_data
def load_data(n_rows=None):
    nyc_link = 'citibike-tripdata.csv'
    df = pd.read_csv(nyc_link, nrows=n_rows, parse_dates=['started_at']) 
    df['hour'] = df['started_at'].dt.hour 
    
    # Renombrar columnas
    df = df.rename(columns={'start_lat': 'lat', 'start_lng': 'lon'})
    return df

# Parameter to select the number of rows to display
num_rows = st.number_input("Number of rows to display", min_value=100, max_value=97289, value=100, step=50)
nyc_data = load_data(num_rows)

# Sidebar
sidebar = st.sidebar
sidebar.title('Filters')
sidebar.image('ilian.jpeg')
sidebar.write('Ilian Jesus Orduña Herrera')
sidebar.write('zs22004363')

# Checkbox to show dataset
agree = sidebar.checkbox('Show dataset')
if agree:
    st.dataframe(nyc_data)

# Slider para seleccionar la hora del día en rango de 0 a 23, default en 12
selected_hour = sidebar.slider('Select hour of the day', 0, 23, 12) 

# Filtrar los datos por la hora seleccionada
filtered_data = nyc_data[nyc_data['hour'] == selected_hour]

# Graficar el número de recorridos por hora
st.subheader(f'Number of Rides at {selected_hour}:00 Hours')

fig, ax = plt.subplots()
hour_counts = nyc_data['hour'].value_counts().sort_index()
ax.bar(hour_counts.index, hour_counts.values, color='skyblue')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Number of Rides')
ax.set_title('Bike Rides per Hour')
st.pyplot(fig)

# Mostrar mapa con los puntos GPS de inicio de recorridos
st.subheader(f'Map of Bike Start Locations at {selected_hour}:00 Hours')
if not filtered_data.empty:
    st.map(filtered_data[['lat', 'lon']])
else:
    st.write("No data available for the selected hour.")
