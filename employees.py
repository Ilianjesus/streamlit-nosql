import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title('Employee Data')

# Función con caché para cargar los datos
@st.cache_data
def load_data(n=500):
    employees_link = 'Employees.csv'
    df = pd.read_csv(employees_link)
    return df.head(n)

# Sidebar input for number of rows to display
num_rows = st.sidebar.number_input('Enter the number of rows to display', min_value=1, max_value=1000, value=500)

# Sidebar checkbox to control whether to display the dataframe
show_data = st.sidebar.checkbox('Show DataFrame', value=True)

# Cargar datos
employees_data = load_data(num_rows)

# Mostrar el dataframe solo si el checkbox está marcado
if show_data:
    st.dataframe(employees_data)
else:
    st.write("DataFrame is hidden. Check the box to display.")

# Función de búsqueda con caché
@st.cache_data
def search_employees(df, employee_id=None, hometown=None, unit=None):
    # Filtro de búsqueda
    filtered_df = df
    if employee_id:
        filtered_df = filtered_df[filtered_df['Employee_ID'].astype(str).str.contains(employee_id)]
    if hometown:
        filtered_df = filtered_df[filtered_df['Hometown'].str.contains(hometown, case=False, na=False)]
    if unit:
        filtered_df = filtered_df[filtered_df['Unit'].str.contains(unit, case=False, na=False)]
    return filtered_df

# Buscador en la interfaz
st.sidebar.header("Employee Search")

# Entradas de búsqueda
employee_id = st.sidebar.text_input('Search by Employee ID')
hometown = st.sidebar.text_input('Search by Hometown')
unit = st.sidebar.text_input('Search by Unit')

# Botón de búsqueda
if st.sidebar.button('Search'):
    # Filtrar datos basados en las entradas
    search_results = search_employees(employees_data, employee_id, hometown, unit)
    
    # Mostrar resultados
    if not search_results.empty:
        st.write(f"Found {len(search_results)} employee(s).")
        st.dataframe(search_results)
    else:
        st.write("No results found.")

# Función de filtrado por nivel educativo con caché
@st.cache_data
def filter_by_education(df, education_level):
    if education_level:
        return df[df['Education_Level'] == education_level]
    return df

# Sidebar control de filtrado por nivel educativo
education_levels = employees_data['Education_Level'].unique()
education_level = st.sidebar.selectbox('Select Education Level', ['All'] + list(education_levels))

# Filtrar por nivel educativo
filtered_by_education = filter_by_education(employees_data, education_level if education_level != 'All' else None)

# Mostrar los datos filtrados por nivel educativo
if not filtered_by_education.empty:
    st.write(f"Found {len(filtered_by_education)} employee(s) with {education_level} education level.")
    st.dataframe(filtered_by_education)
else:
    st.write("No results found for the selected education level.")

# Función de filtrado por ciudad con caché
@st.cache_data
def filter_by_hometown(df, hometown):
    if hometown:
        return df[df['Hometown'] == hometown]
    return df

# Sidebar control de filtrado por ciudad
cities = employees_data['Hometown'].unique()
city = st.sidebar.selectbox('Select City', ['All'] + list(cities))

# Filtrar por ciudad
filtered_by_city = filter_by_hometown(employees_data, city if city != 'All' else None)

# Mostrar los datos filtrados por ciudad
if not filtered_by_city.empty:
    st.write(f"Found {len(filtered_by_city)} employee(s) from {city}.")
    st.dataframe(filtered_by_city)
else:
    st.write(f"No results found for the selected city.")

# Función de filtrado por unidad funcional (Unit) con caché
@st.cache_data
def filter_by_unit(df, unit):
    if unit:
        return df[df['Unit'] == unit]
    return df

# Sidebar control de filtrado por unidad funcional
units = employees_data['Unit'].unique()
unit = st.sidebar.selectbox('Select Unit', ['All'] + list(units))

# Filtrar por unidad funcional
filtered_by_unit = filter_by_unit(employees_data, unit if unit != 'All' else None)

# Mostrar los datos filtrados por unidad funcional
if not filtered_by_unit.empty:
    st.write(f"Found {len(filtered_by_unit)} employee(s) in the {unit} unit.")
    st.dataframe(filtered_by_unit)
else:
    st.write(f"No results found for the selected unit.")

# Histograma de empleados agrupados por edad
st.header("Age Distribution of Employees")

# Función para crear el histograma de edad
def plot_age_histogram(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df['Age'], bins=range(int(df['Age'].min()), int(df['Age'].max()) + 1, 1), alpha=0.7, color='skyblue')
    plt.title('Distribution of Employee Ages')
    plt.xlabel('Age')
    plt.ylabel('Number of Employees')
    plt.grid(True)
    st.pyplot(plt)

# Mostrar el histograma de edades
plot_age_histogram(employees_data)

# Gráfico de frecuencias para las unidades funcionales
st.header("Employee Frequency by Unit")

# Función para crear el gráfico de barras de frecuencias por unidad
def plot_unit_frequency(df):
    unit_counts = df['Unit'].value_counts()
    plt.figure(figsize=(10, 6))
    unit_counts.plot(kind='bar', color='skyblue', alpha=0.7)
    plt.title('Employee Count by Unit')
    plt.xlabel('Unit')
    plt.ylabel('Number of Employees')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Mostrar el gráfico de frecuencias por unidad
plot_unit_frequency(employees_data)

# Gráfico de deserción por ciudad (Hometown)
st.header("Attrition Rate by City (Hometown)")

# Función para crear el gráfico de barras de deserción por ciudad
def plot_attrition_by_city(df):
    # Agrupar por ciudad y calcular el índice de deserción promedio
    attrition_by_city = df.groupby('Hometown')['Attrition_rate'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    attrition_by_city.plot(kind='bar', color='lightcoral', alpha=0.7)
    plt.title('Attrition Rate by City (Hometown)')
    plt.xlabel('City')
    plt.ylabel('Average Attrition Rate')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Mostrar el gráfico de deserción por ciudad
plot_attrition_by_city(employees_data)

# Gráfico de edad vs tasa de deserción (Attrition Rate)
st.header("Age vs Attrition Rate")

# Función para crear el gráfico de dispersión de edad vs tasa de deserción
def plot_age_vs_attrition(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Age'], df['Attrition_rate'], alpha=0.5, color='teal')
    plt.title('Age vs Attrition Rate')
    plt.xlabel('Age')
    plt.ylabel('Attrition Rate')
    plt.grid(True)
    st.pyplot(plt)

# Mostrar el gráfico de dispersión de edad vs tasa de deserción
plot_age_vs_attrition(employees_data)

# Gráfico de tiempo de servicio vs tasa de deserción (Attrition Rate)
st.header("Time of Service vs Attrition Rate")

# Función para crear el gráfico de dispersión de tiempo de servicio vs tasa de deserción
def plot_service_vs_attrition(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Time_of_service'], df['Attrition_rate'], alpha=0.5, color='orange')
    plt.title('Time of Service vs Attrition Rate')
    plt.xlabel('Time of Service (Years)')
    plt.ylabel('Attrition Rate')
    plt.grid(True)
    st.pyplot(plt)

# Mostrar el gráfico de dispersión de tiempo de servicio vs tasa de deserción
plot_service_vs_attrition(employees_data)
