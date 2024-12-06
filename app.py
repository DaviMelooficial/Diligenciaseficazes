import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import dotenv
import bcrypt
from datetime import datetime
from controle_diligencias import controle_diligencias

# Conexão ao banco
def connect_db():
    return sqlite3.connect("instance/diligencias.db")

# Autenticação de usuário
def authenticate_user(usuario, senha):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT senha, cargo, setor FROM usuarios WHERE usuario = ?", (usuario,))
        result = cursor.fetchone()

    if result:
        senha_hashed, cargo, setor = result
        if bcrypt.checkpw(senha.encode(), senha_hashed): 
            return cargo, setor
    return None

def login():
    st.title("Diligências Eficazes")
    st.subheader("Sistema de Login")
    usuario = st.text_input("usuario")
    senha = st.text_input("Senha", type="password")

    if st.button("Login"):
        user_info = authenticate_user(usuario, senha)
        if user_info:
            # Atualiza o estado do login
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.session_state.cargo, st.session_state.setor = user_info
            st.session_state.page = "Acompanhamento de Acordos"

            st.rerun()
        else:
            st.error("Credenciais inválidas.")

def rodar_aplicacao():

    funcionalidades = {
        "Controle de Diligências": controle_diligencias,
        "Cadastrar Diligências": "rodar_dashboard_hora",
        "Cadastro de Clientes": "carregar_acessos",
        "Financeiro": "estrategias"
    }
    
    st.sidebar.title("Menu de Navegação")
    st.sidebar.markdown(f"**Usuário:** {st.session_state.usuario}")
    st.sidebar.markdown(f"**Cargo:** {st.session_state.cargo}")
    st.sidebar.markdown(f"**Setor:** {st.session_state.setor}")

    # Menu baseado nas permissões
    permissoes = {
        "Gestor": ["Controle de Diligências", "Cadastrar Diligências", "Cadastro de Clientes", "Financeiro"],
        "Administrador": ["Controle de Diligências", "Cadastrar Diligências", "Cadastro de Clientes", "Financeiro"],
        "Colaborador": ["Controle de Diligências", "Cadastrar Diligências", "Cadastro de Clientes"],
    }

    st.sidebar.markdown("____________________")

    opcoes = permissoes.get(st.session_state.cargo, [])
    if opcoes:
        painel_selecionado = st.sidebar.radio("Selecione a visão:", opcoes, index=0)
        st.session_state.page = painel_selecionado

        # Executa o painel selecionado
        if st.session_state.page in funcionalidades:
            funcionalidades[st.session_state.page]()
        else:
            st.error("Visão não encontrada.")
    else:
        st.error("Você não tem permissão para acessar os dashboards.")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "Login"

# Função principal
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.page = "Login"

    if not st.session_state.logged_in:
        login()
    else:
        rodar_aplicacao()

# Executa a aplicação
if __name__ == "__main__":
    main()