import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('artdepor.csv', sep=';', header=None, names=['Nombre', 'Precio', 'Deporte', 'Marca', 'Cantidad', 'Referencia'])

# Formatear precios
df['Precio'] = df['Precio'].apply(lambda x: f"${x:,.2f}")

# Título de la aplicación
st.title("Inventario de Artículos Deportivos")

# Barra lateral con filtros
st.sidebar.header("Filtros")

# Búsqueda
search_term = st.sidebar.text_input("Buscar artículo")
filtered_df = df[df['Nombre'].str.contains(search_term, case=False) | 
                  df['Deporte'].str.contains(search_term, case=False) |
                  df['Marca'].str.contains(search_term, case=False)]

# Seleccionar columnas
selected_columns = st.sidebar.multiselect('Seleccionar columnas', df.columns)

# Ordenar por
sort_column = st.sidebar.selectbox('Ordenar por', df.columns)
ascending = st.sidebar.checkbox('Ascendente', True)
sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

# Mostrar tabla
st.table(sorted_df[selected_columns])

# Gráfico de barras por deporte
fig = px.bar(sorted_df, x='Deporte', y='Cantidad', title='Cantidad de artículos por deporte')
st.plotly_chart(fig)

# Descargar datos
if st.button('Descargar datos'):
    csv = sorted_df[selected_columns].to_csv(index=False)
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name='inventario.csv',
        mime='text/csv',
    )