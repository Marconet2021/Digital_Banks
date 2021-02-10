from tkinter import *
from tkinter import messagebox
import pymysql

Fonte_12 = "Arial, 12"
Fonte_12B = ("Arial", 12, "bold")
Fonte_14B = ("Arial", 14, "bold")
Preto = "black"
Branco = "white"
Gold = "#daa520"
Cinza51 = "gray51"
Verde = "#276955"

Windows = Tk()
Windows.geometry("400x300+500+250")
Windows.title("PROJETO ONG")
Windows.config(bg=Verde)

# Função para fechar Janela
def Sair(event=None):
    Windows.destroy()

def Autenticar(event=None):
    Lista_User = []
    Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
    Cursor_Usuario = Conexao.cursor()
    Cursor_Logado = Conexao.cursor()
    Cursor_Usuario.execute("SELECT NOME, LOGIN, SENHA FROM USUARIOS WHERE LOGIN = '%s' AND SENHA = '%s';"
                   % (Var_User.get(), Var_Pswds.get()))
    for nome in Cursor_Usuario.fetchall():
        Lista_User.append(nome[0])
    if Lista_User is not None:
        Windows.destroy()
        Usuario_Logado = ("INSERT INTO LOGADO(NOME)VALUES(%s);")
        Usuario_Paramentros = Lista_User[0]
        Cursor_Logado.execute(Usuario_Logado, Usuario_Paramentros)
        Conexao.commit()
        import Main
    else:
        messagebox.showinfo('ERROR', 'Dados Incorretos')
        Ent_User.delete(0, END)
        Ent_Pswds.delete(0, END)
        Ent_User.focus()

    Conexao.close()

# variavel declarada pra receber imagem
Imagem_Logo = PhotoImage(file="Imagens\\Label\\tk8.png")


# Criando Label pra Visualização da Imagem
Lbl_Logo = Label(Windows, image=Imagem_Logo, bg=Verde)
Lbl_Logo.image = Imagem_Logo
Lbl_Logo.place(x=20, y=30)

# Label de Saudação
Lbl_Sauda = Label(Windows, text="SEJA BEM VINDO!", bg=Verde, fg=Branco, font=Fonte_14B)
Lbl_Sauda.place(x=110, y=80)

# Label e Entry do Campo USUÁRIO
Var_User = StringVar() # Variavel pra receber dados digitados
Lbl_User = Label(Windows, text="USUÁRIO:", bg=Verde, fg=Branco, font=Fonte_12B)
Lbl_User.place(x=70, y=150)
Ent_User = Entry(Windows, bg=Branco, textvariable=Var_User, font=Fonte_12)
Ent_User.place(x=160, y=150)
Ent_User.bind("<Escape>", Sair) # Evento da Tecla ESC pra fechar janela
Ent_User.focus()

# Label e Entry do Campo SENHA
Var_Pswds = StringVar() # Variavel pra receber dados digitados
Lbl_Pswds = Label(Windows, text="SENHA:", bg=Verde, fg=Branco, font=Fonte_12B)
Lbl_Pswds.place(x=70, y=190)
Ent_Pswds = Entry(Windows, bg=Branco, textvariable=Var_Pswds, font=Fonte_12)
Ent_Pswds.place(x=160, y=190)
Ent_Pswds.bind("<Escape>", Sair) # Evento da Tecla ESC pra fechar janela
Ent_Pswds.bind("<Return>", Autenticar) # Evento da Tecla Enter pra chamar função Autenticar

# Criando Botão ENTRAR
BtnEntrar = Button(Windows, text="ENTRAR", bg=Verde, fg=Gold, font=Fonte_12B, command=Autenticar)
BtnEntrar.place(x=208, y=230)
# Criando Botão SAIR
BtnSair = Button(Windows, text="SAIR", bg=Verde, fg=Gold, font=Fonte_12B, command=Sair)
BtnSair.place(x=292, y=230)

Windows.mainloop()