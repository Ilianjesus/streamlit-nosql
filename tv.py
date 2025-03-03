import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title('Data Analysis of TV Shows')
# Logo
st.image('Max_Education.png', width=200)

# Función con caché para cargar los datos
@st.cache_data
def load_data(n=500):
    tv_link = 'TMDB_tv_dataset_v3.csv'
    df = pd.read_csv(tv_link)
    return df.head(n)

# Sidebar 
sidebar = st.sidebar
sidebar.title('Sidebar')
sidebar.image('ilian.jpeg')
sidebar.write('Ilian Jesus Orduña Herrera')
sidebar.write('zs22004363')
# Text input para el número de filas a mostrar
num_rows = sidebar.number_input('Enter the number of rows to display', min_value=1, max_value=168000, value=500)
# Checkbox para mostrar los datos
show_data = sidebar.checkbox('Show DataFrame', value=True)
# Cargar los datos y mostrarlos si se selecciona la opción
tv_data = load_data(num_rows)
if show_data:
    st.dataframe(tv_data)


# BUSQUEDA POR NOMBRE
st.subheader('Buscar por TV Show')
search_query = st.text_input('Introduce el nombre del TV Show')
search_button = st.button('Buscar')

if search_button and search_query:
    filtered_data = tv_data[tv_data['name'].str.contains(search_query, case=False, na=False)]
    
    if not filtered_data.empty:
        st.write(f"Resultados para '{search_query}':")
        st.dataframe(filtered_data)
    else:
        st.write(f"No se encontraron resultados para '{search_query}'.")

# FILTRO POR GÉNERO
st.subheader('Filtro por género')
genres = tv_data['genres'].dropna().unique()
selected_genre = st.selectbox('Elige un genero', ['All'] + list(genres))

if selected_genre != 'All':
    filtered_by_genre = tv_data[tv_data['genres'].str.contains(selected_genre, case=False, na=False)]
    st.write(f"Resultados para el genero: {selected_genre}")
    st.dataframe(filtered_by_genre)
else:
    st.write("Mostrando todos los datos.")
    st.dataframe(tv_data)


# HISTOGRAMA DE PROMEDIO DE VOTOS 
st.subheader('Histograma de promedio de votos')
# Filtrar los valores no nulos de la columna 'vote_average'
filtered_vote_average = tv_data['vote_average'].dropna()
# Crear el histograma
plt.figure(figsize=(8, 6))
plt.hist(filtered_vote_average, bins=20, color='skyblue', edgecolor='black')
plt.title('Distribucion de promedio de votos')
plt.xlabel('Voto promedio')
plt.ylabel('Frequencia')
plt.grid(True)
st.pyplot(plt)


# GRAFICO DE BARRAS PARA PROMEDIO DE VOTOS VS GENERO (3 géneros más comunes)
st.subheader('Promedio de votos por género')
# Filtrar los 3 géneros más comunes
top_genres = tv_data['genres'].dropna().value_counts().head(3).index
# Filtrar los datos solo para los 3 géneros más comunes
filtered_by_top_genres = tv_data[tv_data['genres'].isin(top_genres)]
# Promedio de la calificación por género
average_vote_by_genre = filtered_by_top_genres.groupby('genres')['vote_average'].mean().sort_values(ascending=False)
# Crear gráfico de barras
plt.figure(figsize=(8, 6))
average_vote_by_genre.plot(kind='bar', color='lightgreen', edgecolor='black')
plt.title('Promedio de votos por género')
plt.xlabel('Genero')
plt.ylabel('Promedio de votos')
plt.xticks(rotation=45)
plt.ylim(1, 10)
plt.grid(True)
st.pyplot(plt)


# DIAGRAMA DE DISPERSIÓN
st.subheader('Diagrama de dispersión de la cantidad de episodios contra a la duración del episodio')
# Filtrar los valores no nulos de las columnas 'number_of_episodes' y 'episode_run_time'
filtered_episodes = tv_data[['number_of_episodes', 'episode_run_time']].dropna()
# Crear gráfico de dispersión
plt.figure(figsize=(8, 6))
plt.scatter(filtered_episodes['number_of_episodes'], filtered_episodes['episode_run_time'], alpha=0.6, color='orange')
plt.title('Numero de episodios vs Duración del episodio')
plt.xlabel('Numero de episodios')
plt.ylabel('Duracion del episodio (minutos)')
plt.grid(True)
st.pyplot(plt)

