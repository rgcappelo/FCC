import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Transformación Digital FCC",
    layout="wide"
)

# Función para cargar datos
@st.cache_data
def load_data():
    data = {
        'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        'Tiempo_Aprobacion': [45, 42, 40, 38, 35, 32, 30, 28, 25, 24, 23, 22],
        'Decisiones_Datos': [10, 12, 14, 16, 18, 20, 23, 25, 28, 30, 32, 35],
        'Adopcion_Digital': [20, 30, 40, 50, 60, 65, 70, 75, 80, 85, 88, 90],
        'Finalizacion_Formacion': [50, 55, 60, 65, 70, 72, 74, 76, 78, 80, 82, 85]
    }
    return pd.DataFrame(data)

# Cargar datos
df = load_data()

# Título principal
st.title('Dashboard de Transformación Digital FCC')
st.markdown('### Aprovechamiento de Oportunidades Digitales (Seizing)')

# Crear dos columnas para los KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Tiempo Actual Aprobación",
        f"{df['Tiempo_Aprobacion'].iloc[-1]} días",
        f"{df['Tiempo_Aprobacion'].iloc[0] - df['Tiempo_Aprobacion'].iloc[-1]} días"
    )

with col2:
    st.metric(
        "Decisiones Basadas en Datos",
        df['Decisiones_Datos'].iloc[-1],
        f"{((df['Decisiones_Datos'].iloc[-1] - df['Decisiones_Datos'].iloc[0])/df['Decisiones_Datos'].iloc[0]*100):.1f}%"
    )

with col3:
    st.metric(
        "Adopción Digital",
        f"{df['Adopcion_Digital'].iloc[-1]}%",
        f"{df['Adopcion_Digital'].iloc[-1] - df['Adopcion_Digital'].iloc[0]}%"
    )

with col4:
    st.metric(
        "Finalización Formación",
        f"{df['Finalizacion_Formacion'].iloc[-1]}%",
        f"{df['Finalizacion_Formacion'].iloc[-1] - df['Finalizacion_Formacion'].iloc[0]}%"
    )

# Crear dos filas para los gráficos
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    # Gráfico de línea para tiempo de aprobación
    fig_tiempo = px.line(
        df,
        x='Mes',
        y='Tiempo_Aprobacion',
        title='Reducción del Tiempo de Aprobación de Proyectos de TI',
        markers=True
    )
    fig_tiempo.add_hline(
        y=45*0.6,  # 40% de reducción del valor inicial
        line_dash="dash",
        line_color="red",
        annotation_text="Objetivo: -40%"
    )
    st.plotly_chart(fig_tiempo, use_container_width=True)

with row1_col2:
    # Gráfico de barras para decisiones basadas en datos
    fig_decisiones = px.bar(
        df,
        x='Mes',
        y='Decisiones_Datos',
        title='Cantidad de Decisiones Basadas en Datos',
        color='Decisiones_Datos'
    )
    fig_decisiones.add_hline(
        y=10*1.25,  # 25% de aumento del valor inicial
        line_dash="dash",
        line_color="green",
        annotation_text="Objetivo: +25%"
    )
    st.plotly_chart(fig_decisiones, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    # Gráfico de área para adopción digital
    fig_adopcion = px.area(
        df,
        x='Mes',
        y='Adopcion_Digital',
        title='Evolución de la Adopción de Herramientas Digitales',
        line_shape='spline'
    )
    fig_adopcion.add_hline(
        y=90,  # Objetivo de 90%
        line_dash="dash",
        line_color="green",
        annotation_text="Objetivo: 90%"
    )
    st.plotly_chart(fig_adopcion, use_container_width=True)

with row2_col2:
    # Gráfico de radar para tasa de finalización
    categories = ['Q1', 'Q2', 'Q3', 'Q4']
    q_values = [
        df['Finalizacion_Formacion'][2],  # Marzo
        df['Finalizacion_Formacion'][5],  # Junio
        df['Finalizacion_Formacion'][8],  # Septiembre
        df['Finalizacion_Formacion'][11]  # Diciembre
    ]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=q_values,
        theta=categories,
        fill='toself',
        name='Actual'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[80, 80, 80, 80],  # Objetivo de 80%
        theta=categories,
        name='Objetivo',
        line=dict(dash='dash')
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title='Tasa de Finalización del Programa de Formación en TI por Trimestre'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Agregar filtros en la barra lateral
st.sidebar.header('Filtros')
meses_seleccionados = st.sidebar.multiselect(
    'Seleccionar Meses',
    df['Mes'].unique(),
    default=df['Mes'].unique()
)