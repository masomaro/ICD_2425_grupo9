import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import geopy as gp
import emoji
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderServiceError



# importaçao ficheiros py
import bibliometrica as bib
import conteudo as cont


#Funções a serem utilizadas dentro de funções do menu

def apresentacao():
    st.subheader("Recolha de informação")
    st.markdown("""
                    A fonte selecionada para a pesquisa bibliográfica foi a base de dados multidisciplinar Scopus.
                    Para a pesquisa bibliográfica foram usados os termos "artificial intelligence", "scientific research" e “impact*”, resultando na seguinte expressão de pesquisa:
            (TITLE-ABS-KEY("artificial intelligence") AND TITLE-ABS-KEY("scientific research") AND TITLE-ABS-KEY("impact*")).
            """)

def dados_gerais(df1, df2, df3):
    """
    Mostra o número de documentos, o número de países afiliados e o número de áreas temáticas.
    
    Parâmetros:
    df1 - DataFrame contendo os documentos
    df2 - DataFrame contendo os países afiliados
    df3 - DataFrame contendo as áreas temáticas
    """
    
    # Número de documentos
    num_documentos = df1.shape[0]
    
    # Número de países afiliados
    num_paises = df2[df2['COUNTRY']!= 'Undefined']['COUNTRY'].nunique()
    
    # Número de áreas temáticas
    num_areas = df3[df3['SUBJECT AREA'] != 'Undefined']['SUBJECT AREA'].nunique()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>📄</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 40px'>{num_documentos}</div>", unsafe_allow_html=True) 
        st.markdown("<div style='text-align: center;'>documentos</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>🌍</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 40px'>{num_paises}</div>", unsafe_allow_html=True) 
        st.markdown("<div style='text-align: center;'>países de afiliação</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>📚</h1>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 40px'>{num_areas}</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>áreas temáticas</div>", unsafe_allow_html=True)


# 1 Configurações da página
st.set_page_config(
    page_title="O impacto da IA e Investigação Científica",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Dataframes necessárias

df = pd.read_csv(r'data\scopus.csv')
df_country = pd.read_csv(r'data\Scopus-Country.csv')
df_subject = pd.read_csv(r'data\Scopus-Subject.csv')


# Funções para cada seção do menu
def visao_geral(df):
    st.title("O impacto da inteligência artificial na investigação científica")
    apresentacao()
    st.subheader("Dados gerais") 
    dados_gerais(df, df_country, df_subject)
    
    st.divider()
    st.text("CSV da Scopus em bruto")
    st.dataframe(df)
    
    
# Menu na barra lateral
with st.sidebar:
    selected = option_menu(
        "Índice",
        ["Introdução",
        "Análise Bibliométrica",
        "Análise de Conteúdo",
        "Conclusão"],
        default_index=0,
    )

# Conteúdo baseado na seleção do menu
if selected == "Introdução":
    visao_geral(df)
    
elif selected == "Análise Bibliométrica":
    bib.analise_bibliometrica(df)
    bib.geoMapdocuments(df_country)
    bib.subjectCloud(df_subject)

elif selected == "Análise de Conteúdo":
    cont.analise_conteudo(df)
elif selected == "Conclusão":
    cont.ShowingTopics()
    

