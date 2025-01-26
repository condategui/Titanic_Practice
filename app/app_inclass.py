# IMPORTANTE TENERE STREAMLIT INSTALADO PARA QUE FUNCIONE
## Hemos creado un servidor, para abrirlo hemos hecho: streamlit run [relative path de la app]
## web para pillar los graficos y hacer las funciones: https://plotly.com/python/bar-charts/
## ctl c paramos el servidor de streamlit en la terminal

# Importando librerias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Funciones utiles y graficos (e invoco cuando necesito)
## grafico de barras
def bar_chart(data, x, y):
    fig = px.bar(data, x=x, y=y)
    return fig


# pr conf
##layout tienes: wide & centered
st.set_page_config(page_title='TITANIC DASHBOARD', layout='wide')

# textos
st.title('TITANIC DASHBOARD')
st.text('Esto es un test interactivo')
st.markdown('---')

# menu
## comento para que no se vea y no moleste
#st.sidebar.title('MENU')

#datos
## En memoria
df=pd.read_csv(r'streamlitenv/data/Titanic_check.csv')
### r' para leerlo
## Lo mostramos 
    #st.dataframe(df) - comentamos para seguir la clase


#tabs
tab1, tab2, tab3 = st.tabs(['Datos', 'Otros', 'libre'])

with tab1: 
    st.dataframe(df)
with tab2:
    st.subheader('Gráfico de Barras')
    graph1 = bar_chart(df, 'Pclass', 'Sex')
    st.plotly_chart(graph1)
    st.text('Este gráfico explica las cosas que ya ves ;)')

#columnas
with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text('Columna 1')
    with col2: 
        st.subheader('Gráfico de Barras')
        graph2 = bar_chart(df, 'Pclass', 'Embarked')
        st.plotly_chart(graph2)
        st.text('Este gráfico explica las cosas que ya ves x2 haha ;)')
    with col3:
        st.text('Columna 3')


# Para hacer nuestras presentaciones

#menu - panel de control personalizado
st.sidebar.title('Menu')
st.sidebar.button('Inicio')
st.sidebar.button('Analisis de Datos')