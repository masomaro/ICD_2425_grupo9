import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import wordcloud
import nltk
import streamlit as st
import plotly.express as px
from matplotlib.colors import ListedColormap, BoundaryNorm
from wordcloud import WordCloud

#Funções a serem utilizadas dentro de funções do menu

def top_documents_and_distribution(df):
    """
    Mostra o top 10 de documentos mais citados, a distribuição de documentos por ano,
    e o top de keywords de autor e de indexação.
    
    Parâmetros:
    df - DataFrame contendo os documentos
    """
    # Seleção do ano
    year = st.slider("Selecionar o ano:", min_value=1990, max_value=2024)
    df_year = df[df['Year'] == year]
    
    # Gráfico de linhas que destaca o ano selecionado
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df.groupby('Year').size(), ax=ax)
    ax.axvline(year, color='red', linestyle='--')
    ax.set_title("Distribuição de documentos por ano")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Número de documentos")
    st.pyplot(fig)
    
    # Top 10 de documentos mais citados
    st.subheader("Número de citações")
    top_cited_articles = df_year[['Title', 'Cited by']].sort_values(by='Cited by', ascending=False).head(10)
    st.write(f"Citações a documentos do ano {year}:")
    st.dataframe(top_cited_articles)
    
    # Distribuição de documentos por ano
    st.subheader("Distribuição de documentos por ano")
    st.write(f"Número de documentos publicados em {year}: {len(df_year)}")
    
    st.subheader("Palavras-chave")
    
    # Top de keywords de autor e de indexação em colunas
    col1, col2 = st.columns(2)
    with col1:
        
        top_author_keywords = df_year['Author Keywords'].value_counts().head(10)
        st.write(f"Keywords de autor nos documentos de {year}:")
        st.dataframe(top_author_keywords)
    
    with col2:
        
        top_index_keywords = df_year['Index Keywords'].value_counts().head(10)
        st.write(f"Keywords de indexação nos documentos de {year}:")
        st.dataframe(top_index_keywords)
        
    st.write("""As palavras-chaves de indexação atribuídas aos documentos que se revelaram mais frequentes são:
            “artificial intelligence”, 
            “scientific researches”, 
            “human”, 
            “machine learning”
            “deep learning”.""")

def geoMapdocuments(df_country, color_scale=px.colors.sequential.Plasma):
    st.header("Distribuição de número de documentos por país")
    
    # Slider para selecionar o número mínimo de documentos
    min_docs = st.slider("Selecionar o número mínimo de documentos:", min_value=int(df_country['NR_PUB'].min()), max_value=int(df_country['NR_PUB'].max()), value=int(df_country['NR_PUB'].min()))
    
    # Filtrar o DataFrame com base no número mínimo de documentos selecionado
    df_filtered = df_country[df_country['NR_PUB'] >= min_docs]
    
    fig = px.scatter_geo(
        df_filtered,
        locations='COUNTRY',
        locationmode='country names',
        hover_name='COUNTRY',
        size='NR_PUB',
        projection="natural earth",
        hover_data={'NR_PUB': True},
        color='NR_PUB',
        color_continuous_scale=color_scale
    )
    
    # Configurações adicionais de layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    return st.plotly_chart(fig)


def subjectCloud(df):
    min_value = 0
    max_value = df['NR'].max()
    # Gerar a Treemap usando Plotly
    fig = px.treemap(df, path=['SUBJECT AREA'], values='NR',
                    color='NR', hover_data={'NR': True},
                    color_continuous_scale='portland', 
                    range_color = ([min_value, max_value])
    )
    # Mostrar o número dentro de cada quadrado
    fig.data[0].textinfo = 'label+text+value'
    
    # Ajustar layout
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25),
                    hoverlabel=dict(bgcolor="black", font_size=11, font_family="Helvetica"))
    
    # Mostrar o gráfico no Streamlit
    st.header('Distribuição de documentos por áreas temáticas')
    st.plotly_chart(fig)
    
'''FUNÇÃO PRINCIPAL ONDE APARECE NA PÁGINA'''

def analise_bibliometrica(df):
    st.title("Análise Bibliométrica")
    
    top_documents_and_distribution(df)
    

