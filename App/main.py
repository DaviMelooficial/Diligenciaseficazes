import streamlit as st

users = {"admin": "1234", "cliente1": "abcd"}
processos = []

# ----- Menu de opções em sidebar ----- #
def main():
    st.title("Diligências Eficazes")
    
    # Menu de Navegação
    menu = ["Login", "Cadastro de Processos", "Visualizar Processos"]
    escolha = st.sidebar.selectbox("Menu", menu)
    
    if escolha == "Login":
        login()
    elif escolha == "Cadastro de Processos":
        cadastrar_processos()
    elif escolha == "Visualizar Processos":
        visualizar_processos()

# ----- Tela de login ----- #
def login():
    st.subheader("Área de Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type='password')
    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Bem-vindo {username}")
            st.session_state["usuario"] = username
        else:
            st.error("Usuário ou senha incorretos")

# ----- Cadastrar processos ----- #
def cadastrar_processos():
    st.subheader("Cadastro de Processos")

    numero_processo = st.text_input("Número do Processo")
    cliente = st.text_input("Cliente")
    descricao = st.text_area("Descrição")
    arquivo = st.file_uploader("Anexar Documento", type=["pdf", "docx"])

    if st.button("Cadastrar"):
        if numero_processo and cliente:
            processo = {"numero": numero_processo, "cliente": cliente, "descricao": descricao}
            processos.append(processo)
            st.success(f"Processo {numero_processo} cadastrado com sucesso!")
        else:
            st.error("Preencha todos os campos!")

# ----- Visualizar processos ----- #
def visualizar_processos():
    st.subheader("Visualizar Processos")
    if processos:
        for processo in processos:
            st.write(f"Número do Processo: {processo['numero']}")
            st.write(f"Cliente: {processo['cliente']}")
            st.write(f"Descrição: {processo['descricao']}")
            st.write("---")
    else:
        st.write("Nenhum processo cadastrado.")

if __name__ == '__main__':
    main()
