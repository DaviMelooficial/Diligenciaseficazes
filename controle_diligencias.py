import streamlit as st
import sqlite3
from datetime import datetime, date
import pandas as pd

# Conexão ao banco
def connect_db():
    return sqlite3.connect("instance/diligencias.db")

# Função para criar tabela de usuários
def criar_tabela_diligencias():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS diligencias (
            data_criacao TEXT PRIMARY KEY,
             BLOB NOT NULL,  -- Senhas armazenadas como BLOB (bytes)
            cargo TEXT NOT NULL,
            setor TEXT NOT NULL
        );
        """)
        conn.commit()

def exibir_filtros(visualizacao):
    col_esquerda, col_direita = st.columns([2, 1])

    with col_esquerda:

        # Seções para datas
        col_data_inicial, col_data_final = st.columns(2)
        with col_data_inicial:
            data_inicial = st.date_input("Data Inicial", date.today())
        with col_data_final:
            data_final = st.date_input("Data Final", date.today())

        # Filtros dinâmicos
        # 1. Clientes
        filtro_carteira = visualizacao['carteira'].unique().tolist()
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        with col_filtro1:
            carteiras = st.multiselect('Carteiras', filtro_carteira)

        # Filtrar dados com base na carteira
        visualizacao_filtrado = visualizacao
        if carteiras:
            visualizacao_filtrado = visualizacao_filtrado[visualizacao_filtrado['carteira'].isin(carteiras)]

        # 2. Supervisores (dependentes de Carteiras)
        filtro_supervisor = visualizacao_filtrado['supervisor'].unique().tolist()
        with col_filtro2:
            supervisores = st.multiselect('Supervisores', filtro_supervisor)

        # Filtrar dados com base nos supervisores
        if supervisores:
            visualizacao_filtrado = visualizacao_filtrado[visualizacao_filtrado['supervisor'].isin(supervisores)]

        # 3. Operadores (dependentes de Supervisores)
        filtro_operador = visualizacao_filtrado['nome_agente'].unique().tolist()
        with col_filtro3:
            operadores = st.multiselect('Operadores', filtro_operador)

    return data_inicial, data_final, carteiras, supervisores, operadores, col_direita

def controle_diligencias():
    st.title("Controle de Diligências")

    teste = {"A": 10, "B": 20}
    visualizacao = pd.DataFrame(teste, columns=["Teste"])

    exibir_filtros(visualizacao)

    st.dataframe()
    pass

# Executa a aplicação
if __name__ == "__main__":
    controle_diligencias()


