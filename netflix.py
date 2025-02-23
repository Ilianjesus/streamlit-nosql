import streamlit as st
import pandas as pd

st.title('Netflix data analysis')

#Read and show the data
@st.cache_data
def load_data(nrows = 500):
    netflix_link = 'movies_utf8.csv'
    try:
        data = pd.read_csv(netflix_link, encoding='utf-8')
        return data.head (nrows)
    except Exception as e:
        st.write(f"Error al cargar los datos: {e}")
        return None
#Create sidebar
sidebar = st.sidebar
sidebar.title('This is the sidebar')
    
#Load and display data if checkbox is selected  
num_filmes = st.number_input("Número de filmes a recuperar:", min_value=1, value=500, step=50)
netflix_data = load_data(num_filmes)

if netflix_data is not None:
    agree = sidebar.checkbox('Show dataset Overview')
    if agree:
        st.dataframe(netflix_data)

#Add text input and search button in sidebar for movie title search
search_term = sidebar.text_input('Search movie by title')
search_button = sidebar.button('Search')

if search_button and search_term:
    filtered_data = netflix_data[netflix_data['name'].str.contains(search_term, case=False, na=False)]
    if not filtered_data.empty:
        st.write(f'Found {len(filtered_data)} movies that match the search term')
        st.dataframe(filtered_data)
    else:
        st.write('No movies found with the search term')

#Selecterbox and command button for searching by director
director_list = netflix_data['director'].dropna().unique()
selected_director = sidebar.selectbox('Select director', director_list)

filter_button = sidebar.button('Filter by director')

if filter_button :
    if selected_director:
        #Filter movies by director
        director_films = netflix_data[netflix_data['director'] == selected_director]
        if not director_films.empty:
            st.write(f'Movies directed by {selected_director}:')
            st.dataframe(director_films)
        else:
            st.write(f'No movies found directed by {selected_director}')
    else:
        st.write('Please select a director to filter the movies')

