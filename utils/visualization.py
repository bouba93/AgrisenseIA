import streamlit as st
import pandas as pd
import plotly.express as px

def show_graphs():
    df = pd.read_csv('data/agriculture_data.csv')
    
    st.subheader("Évolution de la température")
    fig = px.line(df, x=df.index, y="Temperature (°C)", title="Température au fil du temps")
    st.plotly_chart(fig)
    
    st.subheader("Évolution de l'humidité")
    fig2 = px.line(df, x=df.index, y="Humidity (%)", title="Humidité au fil du temps")
    st.plotly_chart(fig2)
    
    st.subheader("Évolution des nutriments")
    fig3 = px.line(df, x=df.index, y="Nutrients (g/L)", title="Nutriments au fil du temps")
    st.plotly_chart(fig3)
    
    st.subheader("Évolution du pH")
    fig4 = px.line(df, x=df.index, y="pH", title="pH au fil du temps")
    st.plotly_chart(fig4)
