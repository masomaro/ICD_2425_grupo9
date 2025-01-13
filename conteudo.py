# Código python e streamlit para a visualizaçao relativa a análise de conteúdo

#Livrarias necessárias
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import os
import webbrowser
import emoji
import csv
from PIL import Image

# FUNÇÕES

def showimage(img, legenda):
    st.image(img, caption=legenda, use_container_width=True)

def modelo_lda(html_file):
    # Carregar o HTML da visualização
    with open(html_file, 'r', encoding='utf-8') as f:
        html_string = f.read()
    
    # Salvar o HTML em um arquivo temporário
    temp_html_path = 'lda_temp.html'
    with open(temp_html_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(html_string)
    
    # Abrir o arquivo HTML em uma nova aba/janela no navegador ao clicar no botão
    if st.button('Abrir Visualização Interativa'):
        new_window_url = 'file:///' + os.path.abspath(temp_html_path)
        webbrowser.open_new_tab(new_window_url)
        st.success("A visualização foi aberta numa nova janela.")
    
def countDocs(df):
    # Agrupar por 'Cluster' e contar o número de 'Title'
    cluster_counts = df.groupby('Cluster')['Title'].count().reset_index()
    cluster_counts.columns = ['Cluster', 'Number of Titles']

    # Mostrar a tabela no Streamlit
    st.write("Contagem de documentos por cluster")
    st.write(cluster_counts)


def countDocsTopic(df, threshold: 0.8): #alterar essa percentagem quando necessario
    contagens = {col:0 for col in df.columns if 'topic' in col.lower()}
    
    for _, row in df.iterrows():
        for coluna in contagens:
            if row[coluna] > threshold:
                contagens[coluna] +=1
                
    return contagens

def ShowingTopics():
    topic_data = {
        'Tópico': ['0', '1', '2', '3', '4', '5'],
        'Palavras': [
            "technology, science, information, paper",  # Tópico 0
            "datum, model, paper, big",  # Tópico 1
            "study, chatgpt, technology, ethical",  # Tópico 2
            "technology, system, development, application",  # Tópico 3
            "technology, model, water, datum",  # Tópico 4
            "technology, study, development, analysis"  # Tópico 5
        ],
        'Descrição': [
            "Tecnologia e Ciência da Informação: relação entre tecnologia, ciência e gestão de informação em áreas como a medicina e a publicação científica.",
            "Big data e modelos: análise de grandes conjuntos de dados e de modelos.",
            "Inteligência Artificial e ética: estudos sobre questões éticas e o impacto de tecnologias e modelos de IA, como o ChatGPT.",
            "Sistemas tecnológicos: desenvolvimento e aplicação de sistemas inteligentes e de modelos de aprendizagem automática.",
            "Modelos tecnológicos: estudo e aplicação de tecnologias na gestão de recursos hídricos, com base em dados científicos.",
            "Estudos tecnológicos: análise de dados e tecnologias emergentes em áreas científicas ligadas com a educação e a informação."
        ]
    }

    df_topics = pd.DataFrame(topic_data)

    st.header("Tópicos")
    st.dataframe(df_topics)
    
    st.divider()
    
    st.header("As dimensões latentes sobre o impacto da IA na investigação científica")
    st.subheader("Tópico 0 - Tecnologia e Ciência da Informação")
    st.markdown("""
                <div style="font-size:20px;">
                Documentos sobre a relação entre a tecnologia, ciência 
                e gestão de informação em áreas como a medicina e a públicação cientifica.
                </div>
                """, unsafe_allow_html=True)
    st.text("\n")
    
    st.subheader("Tópico 1 - Big Data e modelos")
    st.markdown("""
                <div style="font-size:20px;">
                Documentos sobre análise de grandes conjuntos de dados e de modelos.
                </div>
                """, unsafe_allow_html=True)
    st.text("\n")
    
    st.subheader("Tópico 2 - Inteligência Artifical e ética")
    st.markdown("""
                <div style="font-size:20px;">
                Documentos sobre estudos sobre questões éticas e o impacto de 
                tecnologias e modelos de IA, como o ChatGPT.
                </div>
                """, unsafe_allow_html=True)
    st.text("\n")
    
    st.subheader("Tópico 3 - Sistemas tecnológicos")
    st.markdown("""
                <div style="font-size:20px;">
                Documentos sobre o desenvolvimento e aplicação de sistemas 
                inteligentes e de modelos de aprendizagem automática.
                </div>
                """, unsafe_allow_html=True)
    st.text("\n")
    
    st.subheader("Tópico 4 - Modelos tecnológicos")
    st.markdown("""
                <div style="font-size:20px;">
                Documentos sobre o estudo e aplicação de tecnologias na 
                gestão de recursos hídricos, com base em dados científicos.
                </div>
                """, unsafe_allow_html=True)
    st.text("\n")
    
    st.subheader("Tópico 5 - Estudos tecnológicos")
    st.markdown("""
                <div style="font-size:20px;">
                Documentos sobre a análise de dados e tecnologias emergentes em 
                áreas científicas ligadas com a educação e a informação.
                </div>
                """, unsafe_allow_html=True)
    st.text("\n")


def analise_conteudo(df):
    st.title("Análise de Conteúdo")
    st.header("Pré-processamento")
    st.markdown("""
                1. Uniformização do texto
                2. Tokenização básica
                3. Remoção de stopwords
                4. Lematização
                5. Frequência de palavras
                6. Remoção de palavras adicionais
                """)
    # Vetorização
    st.divider()
    st.header("Vetorização")
    
    st.subheader("Bigramas")
    graphic1='imgs\Bigrama.png'
    showimage(graphic1, "Bigramas mais frequentes")
    
    st.subheader("Term Frequency - Inverse Document Frequency (TF-IDF)")
    graphic2='imgs\TFIDF.png'
    showimage(graphic2, "Tabela de frequência de palavras")
    
    # Topicos
    st.divider()
    st.header("Dimensões latentes - Tópicos")
    
    # Modelo LDA: por motivos de tamanho da imagem, vai ser aberto numa nova janela
    st.subheader("Modelo LDA")
    graphic3='imgs\lda_vis.html'
    modelo_lda(graphic3)
    
    # TOPICOS
    # Inserir aqui a tabela sintese
    table1 = 'imgs/tabela_topicos.jpg'
    st.write("Tabela 1 - Tabela síntese dos topicos e descrição ")
    showimage(table1, "")
    
    # Tabelas
    df_topics= pd.read_csv(r'data\document_topic_distribution.csv', sep=';')
    st.write("Tabela 2 - Distribuição de coeficientes de cada documento por tópico ")
    st.dataframe(df_topics)
    
    df_docs=pd.read_csv(r'data\most_relevant_docs.csv', sep=";")
    st.write("Tabela 3 - Top 3 de documentos por tópico")
    st.dataframe(df_docs)
    
    st.divider()
    # CLUSTERS
    st.subheader("Clusterização")
    # Tabela com os clusters e documentos que lhe são associados
    df_clusters = pd.read_csv(r'data\clustered_documents.csv', sep=";")
    st.write("Tabela 3 - Distribuição de documentos por cluster")
    st.dataframe(df_clusters)
    
    #Mostrar topicos e clusters lado a lado
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.write("Contagem de documentos com coeficiente superior a 80% nos tópicos")
        st.dataframe(countDocsTopic(df_topics, threshold=0.8))
    with col2: 
        countDocs(df_clusters)

    heatmap ='imgs\heatmap_cluster_topics.png'
    showimage(heatmap, "Mapa de calor que relaciona os tópicos com os clusters")
    
