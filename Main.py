from tkinter import *
from tkinter import messagebox
from tkinter import Canvas as CV
from tkinter.ttk import Combobox
from pycep_correios import get_address_from_cep
import pymysql
import time
import datetime
import requests
import json
from tkcalendar import DateEntry

# Variaveis de Cor e Fontes
Black = "black"
Verde = "#276955"
Branco = "white"
Cinza60 = "gray60"
Gold = "gold"
Cinza51 = "gray51"
Fonte8 = ("Arial, 8")
Fonte8B = ("Arial", 8, "bold")
Fonte10B = ("Arial", 10, "bold")
Fonte11B = ("Arial", 11, "bold")
Fonte12B = ("Arial", 12, "bold")
Fonte14_H = ("Helvetica", 14)
Fonte14B = ("Arial", 14, "bold")
Fonte15B = ("Arial", 15, "bold")
Fonte18B = ("Arial", 18, "bold")
Fonte20B = ("Arial", 20, "bold")
Fonte10 = "Arial, 10"
Fonte11 = "Arial, 11"
Fonte12 = "Arial, 12"
Cinza_Romano = "#5f626a"
Preto = "black"
tempo = datetime.date.today()

Janela = Tk()
Janela.geometry("1500x750+5+5")
Janela.title("PROJETO ONGS")
Janela.config(bg=Branco)
Janela.resizable(False, False)

# IMAGEM DO FUNDO LOGO
image = PhotoImage(file="Imagens//Label//Logo_tela.png")
image = image.subsample(1, 1)
labelimage = Label(image=image, bg=Branco)
labelimage.place(x=1230, y=530)


def Desativar():
    pass
# ------------------------ FIM ----------------------------------------------------------------------------------------
# ---------------- TELA SAIR ------------------------------------------------------------------------------------------
def Sair(event=None):
    Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
    Cursor_User_Excluir = Conexao.cursor()
    Cursor_User_Excluir.execute("TRUNCATE LOGADO")
    Conexao.commit()
    Conexao.close()
    Janela.destroy()
# ------------------------ FIM ----------------------------------------------------------------------------------------
# ------------------------ CADASTRO DE USUARIO ------------------------------------------------------------------------
def Cadastro_usuario(event=None):

    List_Ano_Nasc = []
    Primeiro_Ano = int(tempo.year) - 70
    Contador = 0
    for i in range(71):
        List_Ano_Nasc.append(int(Primeiro_Ano) + Contador)
        Contador = Contador + 1

    def Calcula_Idade(event=None):

        try:
            mes_idade = int(Mes_Nasc.get()) + 1
            n = datetime.date.today() - datetime.date(int(Ano_Nasc.get()), mes_idade, int(Dia_Nasc.get()))
            idade.set(str(n.days / 365)[:2])
        except:
            idade.set('0')

    def limitar_Size_Login(login):
        if len(login) > 8:
            return False
        return True

    def limitar_Size_Senha(Senha):
        if len(Senha) > 6:
            return False
        return True

    def Limpar_Dados():
        Var_Nome.set("")
        Var_Cpf.set("")
        EntEmail.delete(0, END)
        EntSenha.delete(0, END)
        EntSenha2.delete(0, END)
        EntLogin.delete(0, END)
        CMBDia_Nasc.set("DIA")
        CMBMes_Nasc.set("MÊS")
        CMBAno_Nasc.set("ANO")
        EntNome.focus()

    def Nome_Maisc(event=None):
        Var_Nome.set(EntNome.get().upper())

    def Em_cima_Salvar(event=None):
        Lbl_txt_Salvar.config(fg=Branco)

    def Saiu_de_cima_Salvar(event=None):
        Lbl_txt_Salvar.config(fg=Verde)

    def Em_cima_Exit(event=None):
        Lbl_txt_Exit.config(fg=Branco)

    def Saiu_de_cima_Exit(event=None):
        Lbl_txt_Exit.config(fg=Verde)

    def Show_Senha(event=None):

        if Var_Show_Senha.get() == "0":
            EntSenha.config(show="")
            EntSenha2.config(show="")
            Var_Senha.set(EntSenha.get())
            Var_Senha_2.set(EntSenha2.get())
        else:
            EntSenha.config(show="*")
            EntSenha2.config(show="*")

    def Quit():
        Tela_User.destroy()

    def validate(action, index, value_if_allowed,
                 prior_value, text, validation_type, widget_name, possible_new_value, login):

        if text in '0123456789':
            try:
                float(value_if_allowed)
                if len(login) > 11:
                    return False
                return True
            except ValueError:
                return False
        else:
            return False

    def Salvar_Usuario(event=None):

        Conexao = ""
        Cursor_Ja_Cadastrado = ""
        btSalvar.config(state=DISABLED)
        # Tratando o erro de Entry vazio
        # Condição da Variavel da Entry USUÁRIO vazia
        if Var_Nome.get() == "" or Var_Cpf.get() == "" or EntEmail.get() == "" or EntLogin.get() == "" or \
                Var_Senha.get() == "" or Var_Senha_2.get() == "":
            messagebox.showinfo('ERROR', 'HÁ CAMPO(S) SEM DADOS!')
            EntNome.focus()
        else:
            CPF = Var_Cpf.get()
            try:
                Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
                Cursor_Ja_Cadastrado = Conexao.cursor()

            except:
                messagebox.showinfo("ERROR", "PROBLEMA COM CONEXÃO COM O BANCO DE DADOS")

            Resultado_Pesq = Cursor_Ja_Cadastrado.execute("SELECT NOME FROM USUARIOS WHERE CPF = '%s';" % CPF)
            if Resultado_Pesq != 0:
                messagebox.showinfo("DUPLICADO", "USUÁRIO JA CADASTRADO COM ESSE CPF!", parent=Tela_User)
                Limpar_Dados()
                btSalvar.config(state=NORMAL)

            else:

                if Var_Senha.get() == Var_Senha_2.get():

                    resultado = messagebox.askyesno("CONFIRMAÇÃO", f"VOCê CONFIRMA O CADASTRO DO USUÁRIO\n"
                                f"{Var_Nome.get().upper()} ?", parent=Tela_User)
                    Dt_Nascimento = (f"{Ano_Nasc.get()}-{Mes_Nasc.get()}-{Dia_Nasc.get()}")

                    if resultado == True:
                        inserirUsuario = "INSERT INTO USUARIOS(NOME, CPF, DATA_NASC, EMAIL, LOGIN, SENHA)" + \
                                         "VALUES(%s, %s, %s, %s, %s, %s);"

                        ParamentrosUsuario = (Var_Nome.get().upper(), Var_Cpf.get(), Dt_Nascimento, EntEmail.get(),
                                              EntLogin.get(), Var_Senha.get())

                        cursor_bd = Conexao.cursor()
                        cursor_bd.execute(inserirUsuario, ParamentrosUsuario)
                        Conexao.commit()
                        Conexao.close()
                        Limpar_Dados()
                        messagebox.showinfo("CONFIRMAÇÃO", f"USUÁRIO {Var_Nome.get().upper()} CADASTRADO COM SUCESSO!",
                                            parent=Tela_User)
                        Tela_User.destroy()

                    else:
                        Var_Nome.set(""), Var_Cpf.set(""), EntEmail.delete(0, END), EntLogin.delete(0, END),
                        Var_Senha.set(""), Var_Senha_2.set("")
                        EntNome.focus()
                        btSalvar.config(state=NORMAL)

                else:
                    messagebox.showerror('ERROR', 'Senha não Compactível com a Anterior')
                    Var_Senha.set("")
                    Var_Senha_2.set("")
                    EntSenha.focus()
                    btSalvar.config(state=NORMAL)

    Tela_User = Toplevel()
    Tela_User.config(bg=Verde)
    Tela_User.geometry("620x412+300+100")

    # Caminho com Variavel com a foto
    Foto_User = PhotoImage(file="Imagens\\Label\\usuario.png")
    Foto_Salvar = PhotoImage(file="Imagens\\Botoes\\Save.png")
    Foto_Sair = PhotoImage(file="Imagens\\Botoes\\Cancel.png")
    Vcmd = (Tela_User.register(validate), '%d', '%i', '%i', '%s', '%S', '%v', '%V', '%W', '%P')

    Tela_Geral = LabelFrame(Tela_User, text="CADASTRO DE USUÁRIO", bg=Verde, fg=Gold, font=Fonte11B)
    Tela_Geral.place(x=5, y=1, width=603, height=400)
    Tela_Pessoal = LabelFrame(Tela_Geral, text="DADOS PESSOAIS", font=Fonte10B, bg=Verde, fg=Gold)
    Tela_Pessoal.place(x=90, y=75, width=500, height=175)
    Tela_Password = LabelFrame(Tela_Geral, text="LOGIN", font=Fonte10B, bg=Verde, fg=Gold)
    Tela_Password.place(x=90, y=255, width=500, height=115)

    # Label para criar aviso do botão Salvar
    Lbl_txt_Salvar = Label(Tela_Geral, text="Salvar", bg=Verde, fg=Verde, font=Fonte10)
    Lbl_txt_Salvar.place(x=490, y=52)
    # Label para criar aviso do botão Exit
    Lbl_txt_Exit = Label(Tela_Geral, text="Sair", bg=Verde, fg=Verde, font=Fonte10)
    Lbl_txt_Exit.place(x=550, y=52)

    # Imagem do Usuario
    Label_Imagem_User = Label(Tela_Geral, image=Foto_User, border=0, bg=Verde)
    Label_Imagem_User.image = Foto_User
    Label_Imagem_User.place(x=5, y=10)

    # Label e Entry do NOME
    Var_Nome = StringVar()
    LblNome = Label(Tela_Pessoal, text="NOME:", font=Fonte11B, bg=Verde, fg=Branco)
    LblNome.place(x=10, y=5)
    EntNome = Entry(Tela_Pessoal, font=Fonte12, width=30, textvariable=Var_Nome)
    EntNome.place(x=80, y=5)
    EntNome.bind("<KeyRelease>", Nome_Maisc)
    EntNome.focus()

    # Label e Entry do CPF
    Var_Cpf = StringVar()
    LblCpf = Label(Tela_Pessoal, text="CPF:", font=Fonte11B, bg=Verde, fg=Branco)
    LblCpf.place(x=10, y=45)
    EntCpf = Entry(Tela_Pessoal, font=Fonte12, width=20, textvariable=Var_Cpf, validate='key', validatecommand=Vcmd)
    EntCpf.place(x=80, y=45)

    # Label e Entry Data de Nascimento
    # Dia
    Dia_Nasc = StringVar()
    Dia_Nasc.set("")
    LblDT_Nasc = Label(Tela_Pessoal, text='DATA NASC:', font=Fonte12B, bg=Verde, fg=Branco)
    LblDT_Nasc.place(x=10, y=85)
    CMBDia_Nasc = Combobox(Tela_Pessoal, font=Fonte12, textvariable=Dia_Nasc)
    CMBDia_Nasc['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                             '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
    CMBDia_Nasc.set("DIA")
    CMBDia_Nasc['state'] = 'readonly'
    CMBDia_Nasc.place(x=125, y=85, width=50)

    # Mês
    Mes_Nasc = StringVar()
    Mes_Nasc.set("")
    CMBMes_Nasc = Combobox(Tela_Pessoal, font=Fonte12, textvariable=Mes_Nasc)
    CMBMes_Nasc['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
    CMBMes_Nasc.set("MÊS")
    CMBMes_Nasc['state'] = 'readonly'
    CMBMes_Nasc.place(x=185, y=85, width=60)

    # Ano
    Ano_Nasc = StringVar()
    Ano_Nasc.set("")
    CMBAno_Nasc = Combobox(Tela_Pessoal, font=Fonte12, textvariable=Ano_Nasc, values=List_Ano_Nasc)
    CMBAno_Nasc.set("ANO")
    CMBAno_Nasc['state'] = 'readonly'
    CMBAno_Nasc.place(x=255, y=85, width=60)

    idade = StringVar()
    LblAnos = Label(Tela_Pessoal, text='IDADE: ', font=Fonte12B, bg=Verde, fg=Branco)
    LblAnos.place(x=320, y=85)
    LblAnos2 = Label(Tela_Pessoal, textvariable=idade, font=Fonte12B, bg=Verde, fg=Gold)
    LblAnos2.place(x=400, y=85)
    LblAnos3 = Label(Tela_Pessoal, text='Anos.', font=Fonte12B, bg=Verde, fg=Branco)
    LblAnos3.place(x=430, y=85)
    CMBMes_Nasc.bind('<<ComboboxSelected>>', Calcula_Idade)
    CMBDia_Nasc.bind('<<ComboboxSelected>>', Calcula_Idade)
    CMBAno_Nasc.bind('<<ComboboxSelected>>', Calcula_Idade)
    Calcula_Idade()

    # Label e Entry Email
    LblEmail = Label(Tela_Pessoal, text="EMAIL:", font=Fonte12B, bg=Verde, fg=Branco)
    LblEmail.place(x=10, y=125)
    EntEmail = Entry(Tela_Pessoal, width=33, font=Fonte12)
    EntEmail.place(x=80, y=125)

    # Label e Entry Login
    lblLogin = Label(Tela_Password, text='LOGIN:*', font=Fonte12B, bg=Verde, fg=Branco)
    lblLogin.place(x=5, y=5)
    Valided = Tela_Password.register(func=limitar_Size_Login)
    EntLogin = Entry(Tela_Password, validate='key', validatecommand=(Valided, '%P'), font=Fonte11, width=15)
    EntLogin.place(x=100, y=5)

    # Label e Entry 1° Senha
    Var_Senha = StringVar()
    lbSenha = Label(Tela_Password, text='SENHA:*', font=Fonte12B, bg=Verde, fg=Branco)
    lbSenha.place(x=5, y=35)
    Valided_Senha1 = Tela_Password.register(func=limitar_Size_Senha)
    EntSenha = Entry(Tela_Password, validate='key', validatecommand=(Valided_Senha1, '%P'), font=Fonte11, width=10,
                     show="*", textvariable=Var_Senha)
    EntSenha.place(x=100, y=35)

    # Label e Entry 2° Senha
    Var_Senha_2 = StringVar()
    lbSenha2 = Label(Tela_Password, text='CONFIRMAR SENHA:*', font=Fonte12B, bg=Verde, fg=Branco)
    lbSenha2.place(x=200, y=35)
    Valided_Senha2 = Tela_Password.register(func=limitar_Size_Senha)
    EntSenha2 = Entry(Tela_Password, validate='key', validatecommand=(Valided_Senha2, '%P'), font=Fonte11, width=10,
                      textvariable=Var_Senha_2, show="*")
    EntSenha2.place(x=380, y=35)
    EntSenha2.bind("<Return>", Salvar_Usuario)

    # CheckButton pra mostrar a senha ou não
    Var_Show_Senha = StringVar()
    Var_Show_Senha.set("0")
    Chkbt_Show_Senha = Checkbutton(Tela_Password, text="MOSTRAR SENHA", bg=Verde, fg=Branco, font=Fonte8,
                                   variable=Var_Show_Senha, selectcolor=Cinza60, onvalue=1, activebackground=Cinza60,
                                   activeforeground=Verde)
    Chkbt_Show_Senha.place(x=5, y=65)
    Chkbt_Show_Senha.bind("<Button>", Show_Senha)

    # Label e Avisos de Login e Senha
    lbRecado = Label(Tela_Password, text='Login com Máximo 8 Caracteres', font=Fonte8, bg=Verde, fg=Branco)
    lbRecado.place(x=280, y=5)
    lbRecado2 = Label(Tela_Password, text='Senha com Máximo 6 Caracteres', font=Fonte8, bg=Verde, fg=Branco)
    lbRecado2.place(x=280, y=65)

    # BOTÕES.....
    # Botão SALVAR
    btSalvar = Button(Tela_Geral, bg=Verde, image=Foto_Salvar, activebackground=Verde, command=Salvar_Usuario)
    btSalvar.image = Foto_Salvar
    btSalvar.place(x=482, y=2)
    btSalvar.bind("<Enter>", Em_cima_Salvar)
    btSalvar.bind("<Leave>", Saiu_de_cima_Salvar)
    # Botão SAIR
    btSair = Button(Tela_Geral, image=Foto_Sair, bg=Verde, command=Quit, activebackground=Verde)
    btSair.image = Foto_Sair
    btSair.place(x=537, y=2)
    btSair.bind("<Enter>", Em_cima_Exit)
    btSair.bind("<Leave>", Saiu_de_cima_Exit)

    Tela_User.mainloop()
# ------------------------ FIM ----------------------------------------------------------------------------------------
# ---------------- CADASTRO DE CLIENTES -------------------------------------------------------------------------------
def Cadastro_Clientes(event=None):
    global Contador
    Contador = 1

    def Sair_Clientes(event=None):
        Tela_Clientes.destroy()

    def Consulta_Existente(event=None):
        try:
            Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
            Cursor_Existente_Cliente = Conexao.cursor()
            Cursor_Existente_Cliente.execute("SELECT IDCLIENTE FROM CLIENTES WHERE IDCLIENTE = '%s'"
                                             % Var_Cod_Clientes.get().strip())
            Cod_Valido = Cursor_Existente_Cliente.fetchall()
            if Cod_Valido == ():
                pass
            else:
                messagebox.showinfo("ERROR", "CLIENTE JÁ CADASTRADO")
                Var_Cod_Clientes.set("")
                EntCod_Clientes.focus()
        except:
            messagebox.showinfo("ERROR", "ALGO DEU ERRADO")

    def Codigo_num(action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def Title2(event=None):
        Var_Nome_Clientes.set(EntNome_Clientes.get().upper())

    def Capitalise(event=None):
        Var_Rua_Clientes.set(EntRua.get().title())

    def Capitalise2(event=None):
        Var_Bairro_Clientes.set(EntBairro.get().title())

    def Cursor_1(event=None):
        ECep.focus()

    def Cursor_2(event=None):
        if Var_Bairro_Clientes.get() == "":
            EntBairro.focus()
        else:
            if Var_Cidade_Clientes.get() == "":
                EntCidade.focus()
            else:
                EntEmail.focus()

    def Cursor_3(event=None):
        EntEmail.focus()

    def Hifem(event=None):
        Contar = len(ECep.get())
        if Contar == 5:
            ECep2.focus()

    def Passando_Cliente(event=None):
        LblCliente_ori.config(fg=Branco)

    def Saindo_Cliente(event=None):
        LblCliente_ori.config(fg=Cinza_Romano)

    def Botao_Salvar_emcima(event=None):
        LblBtn_Salvar.config(fg=Branco)

    def Botap_Salvar_saindo(event=None):
        LblBtn_Salvar.config(fg=Verde)

    def Botao_Sair_emcima(event=None):
        LblBtn_Sair.config(fg=Branco)

    def Botap_Sair_saindo(event=None):
        LblBtn_Sair.config(fg=Verde)

    def Salvar_Cliente(event=None):

        if Var_Cod_Clientes.get() == "" or Var_Nome_Clientes.get() == "" or ECep.get() == "" or Var_Email.get() == "":
            messagebox.showinfo("VAZIO", "HÁ DADOS FALTANDO!")

        else:
            Confir = messagebox.askyesno("CONFIRMAÇÃO",
                                         f"VOCÊ CONFIRMA O CADASTRO DO CLIENTE\n{Var_Nome_Clientes.get().upper()}")
            if Confir == True:
                try:
                    Dt_Objeto = datetime.datetime.strptime(Var_Data.get(), '%d/%m/%Y')
                    Dt_formatado = datetime.datetime.strftime(Dt_Objeto, '%Y/%m/%d')
                    Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
                    Cursor_Bd_Clientes = Conexao.cursor()
                    Clientes = ("INSERT INTO CLIENTES(IDCLIENTE, RAZAO, RUA, NUMERO, BAIRRO, CIDADE, EMAIL, ULT_COMPRA)"
                                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s);")
                    Parametros_Clientes = (Var_Cod_Clientes.get(), Var_Nome_Clientes.get(),
                                           Var_Rua_Clientes.get(), Var_Num_Clientes.get(),
                                           Var_Bairro_Clientes.get(), Var_Cidade_Clientes.get(),
                                           Var_Email.get(), Dt_formatado)
                    Cursor_Bd_Clientes.execute(Clientes, Parametros_Clientes)
                    Conexao.commit()
                    Conexao.close()
                    messagebox.showinfo("SUCESSO", f"CLIENTE {Var_Nome_Clientes.get()}\nCADASTRADO COM SUCESSO!")
                    Tela_Clientes.destroy()
                except:
                    messagebox.showinfo("CONEXÃO", "CLIENTE JÁ CADASTRADO")
                    Var_Cod_Clientes.set("")
                    Var_Nome_Clientes.set("")
                    ECep.delete(0, END)
                    Var_Rua_Clientes.set("")
                    Var_Cidade_Clientes.set("")
                    Var_Num_Clientes.set("")
                    Var_Bairro_Clientes.set("")
                    EntCod_Clientes.focus()
            else:
                Var_Cod_Clientes.set("")
                Var_Nome_Clientes.set("")
                ECep.delete(0, END)
                Var_Rua_Clientes.set("")
                Var_Cidade_Clientes.set("")
                Var_Num_Clientes.set("")
                Var_Bairro_Clientes.set("")
                EntCod_Clientes.focus()

    def Upper_City(event=None):
        Var_Cidade_Clientes.set(EntCidade.get().upper())

    def Upper_Uf(event=None):
        Var_Uf_Cliente.set(EntUf.get().upper())

    def MudarStatus(habilitar):
        if habilitar == True:
            novoestado = NORMAL
        else:
            novoestado = DISABLED

        EntRua.config(state=novoestado)
        EntBairro.config(state=novoestado)
        EntCidade.config(state=novoestado)
        EntUf.config(state=novoestado)

    def ConsultarCep(event=None):
        try:
            resultado = dict()
            resultado = get_address_from_cep(ECep.get() + ECep2.get())
            try:
                # Carregar Campos retornados na Tela
                MudarStatus(True)
                if resultado['cidade'] == '' and resultado['uf'] == '':
                    EntRua.config(state=NORMAL)
                    EntBairro.config(state=NORMAL)
                    EntCidade.config(state=NORMAL)
                    EntCidade.bind("<KeyRelease>", Upper_City)
                    EntUf.bind("<KeyRelease>", Upper_Uf)
                    EntUf.config(state=NORMAL)
                    EntRua.focus()

                elif resultado['logradouro'] == '' and resultado['bairro'] == '':
                    EntRua.config(state=NORMAL)
                    EntBairro.config(state=NORMAL)
                    EntRua.focus()
                    EntCidade.delete(0, END)
                    EntCidade.insert(0, resultado['cidade'].upper())
                    EntUf.delete(0, END)
                    EntUf.insert(0, resultado['uf'])
                    EntCidade.config(state=DISABLED)
                    EntUf.config(state=DISABLED)

                else:
                    EntRua.delete(0, END)
                    EntRua.insert(0, resultado['logradouro'])
                    EntBairro.delete(0, END)
                    EntBairro.insert(0, resultado['bairro'])
                    EntCidade.delete(0, END)
                    EntCidade.insert(0, resultado['cidade'].upper())
                    EntUf.delete(0, END)
                    EntUf.insert(0, resultado['uf'])
                    MudarStatus(False)
                    EntNum.focus()
            except:
                messagebox.showerror("Erro Consulta CEP", "O CEP informado não é válido")
                ECep.focus()

            return resultado
        except:
            Cep_Consulta = messagebox.askyesno("SEM CONEXÃO", "SEM CONEXÃO COM INTERNET! DESEJA CONTINUAR")
            if Cep_Consulta == True:
                EntRua.config(state=NORMAL)
                EntBairro.config(state=NORMAL)
                EntCidade.config(state=NORMAL)
                EntUf.config(state=NORMAL)
                EntRua.focus()
                EntCidade.bind("<KeyRelease>", Upper_City)
                EntUf.bind("<KeyRelease>", Upper_Uf)
            else:
                Sair_Clientes()

    Tela_Clientes = CV(Janela, highlightbackground=Verde, highlightcolor=Verde, bg=Verde)
    Tela_Clientes.place(x=400, y=20, width=455, height=385)

    # Caminho com Variavel com a foto
    Foto_Salvar_Clientes = PhotoImage(file="Imagens//Botoes//Save.png")
    Foto_Sair_Clientes = PhotoImage(file="Imagens//Botoes//Cancel.png")
    Imagem_Cliente = PhotoImage(file='Imagens//Label//Clientes.png')
    Imagem_Validate = PhotoImage(file='Imagens//Botoes//Validate.png')
    cod_unt = (Tela_Clientes.register(Codigo_num), '%d', '%i', '%i', '%s', '%S', '%v', '%V', '%W')

    FrClientes = LabelFrame(Tela_Clientes, text="CADASTRO DE CLIENTES", bg=Cinza_Romano, fg=Branco, font=Fonte11B)
    FrClientes.place(x=5, y=80, width=440, height=295)

    FrEnd_Cli = LabelFrame(FrClientes, text="ENDEREÇO", bg=Cinza_Romano, fg=Branco, font=Fonte10)
    FrEnd_Cli.place(x=3, y=70, width=430, height=160)

    # Label para criar aviso do botão Consultar Cep
    LblCliente_ori = Label(FrEnd_Cli, text="Consultar Cep", bg=Cinza_Romano, fg=Cinza_Romano, font=Fonte10)
    LblCliente_ori.place(x=180, y=5)

    # Label para criar aviso do botão Salvar
    LblBtn_Salvar = Label(Tela_Clientes, text="Salvar", bg=Verde, fg=Verde, font=Fonte10)
    LblBtn_Salvar.place(x=329, y=57)
    # Label para criar aviso do botão Sair
    LblBtn_Sair = Label(Tela_Clientes, text="Sair", bg=Verde, fg=Verde, font=Fonte10)
    LblBtn_Sair.place(x=393, y=57)
    # Label para mostrar a tecla de Atalho F2 pra Salvar
    LblAtalho = Label(Tela_Clientes, text="F2  -  Salvar", bg=Verde, fg=Cinza60, font=Fonte10)
    LblAtalho.place(x=220, y=15)

    # Imagem do Usuario
    Lbl_Img_Cliente = Label(Tela_Clientes, image=Imagem_Cliente, border=0, bg=Verde)
    Lbl_Img_Cliente.image = Imagem_Cliente
    Lbl_Img_Cliente.place(x=10, y=10)

    # Label e Entry do CODIGO
    Var_Cod_Clientes = StringVar()
    LblCod_Clientes = Label(FrClientes, text="COD:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblCod_Clientes.place(x=5, y=5)
    EntCod_Clientes = Entry(FrClientes, font=Fonte12, width=10, textvariable=Var_Cod_Clientes, justify=CENTER,
                            validate='key', validatecommand=cod_unt)
    EntCod_Clientes.place(x=80, y=5)
    EntCod_Clientes.focus()
    EntCod_Clientes.bind("<Escape>", Sair_Clientes)
    EntCod_Clientes.bind("<FocusOut>", Consulta_Existente)

    # Label e Entry da Última Compra do Cliente
    Var_Data = StringVar()
    LblUlt_Compra = Label(FrClientes, text="ÚLT COMPRA:", font=Fonte11B, bg=Cinza_Romano, fg=Gold)
    LblUlt_Compra.place(x=195, y=5)
    Dt_Ult_Compra = DateEntry(FrClientes, date_pattern='dd/MM/yyyy', width=9, bg=Verde, fg=Branco, font=Fonte12,
                              headersbackground=Branco, borderwidth=2, selectbackground=Verde,
                              headersforeground=Cinza60,
                              textvariable=Var_Data)
    Dt_Ult_Compra.place(x=310, y=5)

    # Label e Entry do NOME
    Var_Nome_Clientes = StringVar()
    LblNome_Clientes = Label(FrClientes, text="RAZÃO:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblNome_Clientes.place(x=5, y=40)
    EntNome_Clientes = Entry(FrClientes, font=Fonte12, width=35, textvariable=Var_Nome_Clientes)
    EntNome_Clientes.place(x=80, y=40)
    EntNome_Clientes.bind("<KeyRelease>", Title2)
    EntNome_Clientes.bind("<Escape>", Sair_Clientes)
    EntNome_Clientes.bind("<Tab>", Cursor_1)
    EntNome_Clientes.bind("<FocusOut>", Cursor_1)

    # Campo CEP
    Var_Cep = StringVar()
    LblCep = Label(FrEnd_Cli, text='CEP: *', font=Fonte11B, background=Cinza_Romano, fg=Branco)
    LblCep.place(x=5, y=5)
    ECep = Entry(FrEnd_Cli, font=Fonte11, width=5, validatecommand=cod_unt, validate='key', justify=CENTER)
    ECep.place(x=60, y=5)
    ECep.bind("<KeyRelease>", Hifem)
    LblHifen = Label(FrEnd_Cli, text='-', font=Fonte12B, bg=Cinza_Romano, fg=Branco)
    LblHifen.place(x=105, y=4)
    ECep2 = Entry(FrEnd_Cli, font=Fonte11, width=3, validatecommand=cod_unt, validate='key', justify=CENTER)
    ECep2.place(x=117, y=5)
    ECep2.bind("<Return>", ConsultarCep)

    # Label e Entry da Rua do Cliente
    Var_Rua_Clientes = StringVar()
    LblRua_Cli = Label(FrEnd_Cli, text="RUA:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblRua_Cli.place(x=5, y=40)
    EntRua = Entry(FrEnd_Cli, font=Fonte12, width=29, textvariable=Var_Rua_Clientes, state=DISABLED)
    EntRua.place(x=60, y=40)
    EntRua.bind("<KeyRelease>", Capitalise)

    # Label e Entry do Números do Cliente
    Var_Num_Clientes = StringVar()
    LblNum_Cli = Label(FrEnd_Cli, text="N°", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblNum_Cli.place(x=330, y=40)
    EntNum = Entry(FrEnd_Cli, font=Fonte12, width=6, textvariable=Var_Num_Clientes, validate='key',
                   validatecommand=cod_unt)
    EntNum.place(x=360, y=40)
    EntNum.bind("<FocusOut>", Cursor_2)

    # Label e Entry do Bairro do Cliente
    Var_Bairro_Clientes = StringVar()
    LblBairro_Cli = Label(FrEnd_Cli, text="BAIRRO:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblBairro_Cli.place(x=5, y=75)
    EntBairro = Entry(FrEnd_Cli, font=Fonte12, width=20, textvariable=Var_Bairro_Clientes, state=DISABLED)
    EntBairro.place(x=80, y=75)
    EntBairro.bind("<KeyRelease>", Capitalise2)
    EntBairro.bind("<FocusOut>", Cursor_2)

    # Label e Entry do Cidade do Cliente
    Var_Cidade_Clientes = StringVar()
    LblCidade_Cli = Label(FrEnd_Cli, text="CIDADE:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblCidade_Cli.place(x=5, y=110)
    EntCidade = Entry(FrEnd_Cli, font=Fonte12, width=25, textvariable=Var_Cidade_Clientes, state=DISABLED)
    EntCidade.place(x=80, y=110)

    # Label e Entry do UF do Cliente
    Var_Uf_Cliente = StringVar()
    LblUf_Cli = Label(FrEnd_Cli, text="UF:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblUf_Cli.place(x=320, y=110)
    EntUf = Entry(FrEnd_Cli, font=Fonte12, width=3, state=DISABLED, justify=CENTER)
    EntUf.place(x=350, y=110)
    EntUf.bind("<FocusOut>", Cursor_3)

    # Botão CEP Validar
    Btncep = Button(FrEnd_Cli, bg=Verde, takefocus=False, activebackground=Verde, command=ConsultarCep)
    Btncep.place(x=155, y=5)
    Btncep.config(image=Imagem_Validate)
    Btncep.imagem = Imagem_Validate
    Btncep.bind("<Enter>", Passando_Cliente)
    Btncep.bind("<Leave>", Saindo_Cliente)

    # Label e Entry do Email do Cliente
    Var_Email = StringVar()
    LblEmail = Label(FrClientes, text="EMAIL:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblEmail.place(x=5, y=240)
    EntEmail = Entry(FrClientes, font=Fonte12, width=35, textvariable=Var_Email)
    EntEmail.place(x=80, y=240)
    EntEmail.bind("<F2>", Salvar_Cliente)

    # BOTÕES.....
    btSalvar_Clientes = Button(Tela_Clientes, bg=Verde, image=Foto_Salvar_Clientes, activebackground=Verde,
                               command=Salvar_Cliente, borderwidth=0)
    btSalvar_Clientes.image = Foto_Salvar_Clientes
    btSalvar_Clientes.place(x=325, y=12)
    btSalvar_Clientes.bind("<Enter>", Botao_Salvar_emcima)
    btSalvar_Clientes.bind("<Leave>", Botap_Salvar_saindo)

    btSair_Clientes = Button(Tela_Clientes, image=Foto_Sair_Clientes, bg=Verde, activebackground=Verde,
                             command=Sair_Clientes, borderwidth=0)
    btSair_Clientes.image = Foto_Sair_Clientes
    btSair_Clientes.place(x=384, y=12)
    btSair_Clientes.bind("<Enter>", Botao_Sair_emcima)
    btSair_Clientes.bind("<Leave>", Botap_Sair_saindo)
# ------------------------ FIM ----------------------------------------------------------------------------------------
# ---------------- EXCLUIR CLIENTE ------------------------------------------------------------------------------------
def Excluir_Clientes(event=None):
    Lista_Clientes_Excluir = []

    def Sair_Tela_Ex_Cliente(event=None):
        Tela_Ex_Cliente.destroy()

    def CMBClientes():
        Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
        cursor_Prazos = Conexao.cursor()
        cursor_Prazos.execute('SELECT RAZAO FROM CLIENTES ORDER BY RAZAO')

        for row in cursor_Prazos.fetchall():
            Lista_Clientes_Excluir.append(row[0])

        return Lista_Clientes_Excluir

    def Deletar_Cliente(event=None):

        if VarEx_Cliente.get() == "SELECIONE":
            messagebox.showinfo("VAZIO", "SELECIONE UM CLIENTE PARA EXCLUIR")

        else:
            try:
                Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
                Cursor_Exc_Cliente = Conexao.cursor()
                Deletar_Cli = VarEx_Cliente.get()
                confirm = messagebox.askyesno("CONFIRMAÇÃO", f"VOCÊ DESEJA EXCLUIR O CLIENTE\n{Deletar_Cli}")
                if confirm == True:

                    Cursor_Exc_Cliente.execute("DELETE FROM CLIENTES WHERE RAZAO = '%s'" % Deletar_Cli)
                    Conexao.commit()
                    Conexao.close()
                    Tela_Ex_Cliente.destroy()
                    messagebox.showinfo("SUCESSO", "CLIENTE EXCLUÍDO COM SUCESSO!")

                else:
                    VarEx_Cliente.set("SELECIONE")
                    VarCod_Ex_Cliente.set("")
            except:
                messagebox.showinfo("ERROR", "NÃO HÁ CONEXÃO COM O BANCO DE DADOS!")

    def Select_CMB_Cliente(event=None):

        Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
        Cursor_Cod_Prazo = Conexao.cursor()
        Deletar_Cod_Cliente = VarEx_Cliente.get()
        Cursor_Cod_Prazo.execute("SELECT IDCLIENTE FROM CLIENTES WHERE RAZAO = '%s'" % Deletar_Cod_Cliente)
        for cod in Cursor_Cod_Prazo.fetchall():
            VarCod_Ex_Cliente.set(cod[0])

    Tela_Ex_Cliente = CV(Janela, highlightbackground=Verde, highlightcolor=Verde, bg=Verde)
    Tela_Ex_Cliente.place(x=20, y=20, width=460, height=180)

    # Caminho com Variavel com a foto
    Foto_Ex_Save_Cliente = PhotoImage(file="Imagens//Botoes//Save.png")
    Foto_Sair_Ex_Cliente = PhotoImage(file="Imagens//Botoes//Cancel.png")
    Foto_Ex_Cliente = PhotoImage(file="Imagens//Label//Exc_Cliente.png")

    FrExCliente = LabelFrame(Tela_Ex_Cliente, text="EXCLUIR CLIENTES", bg=Cinza_Romano, fg=Branco, font=Fonte11B)
    FrExCliente.place(x=5, y=70, width=440, height=100)

    # Imagem do Usuario
    Lbl_Exc_Cliente = Label(Tela_Ex_Cliente, image=Foto_Ex_Cliente, border=0, bg=Verde)
    Lbl_Exc_Cliente.image = Foto_Ex_Cliente
    Lbl_Exc_Cliente.place(x=10, y=10)

    # Label e Entry do NOME
    VarCod_Ex_Cliente = StringVar()
    VarCod_Ex_Cliente.set("")
    LblExcCod_Cliente = Label(FrExCliente, text="COD:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblExcCod_Cliente.place(x=5, y=5)
    EntExcCod_Cliente = Entry(FrExCliente, font=Fonte12, width=10, state=DISABLED, textvariable=VarCod_Ex_Cliente,
                              justify=CENTER)
    EntExcCod_Cliente.place(x=80, y=5)
    EntExcCod_Cliente.bind("<Escape>", Sair_Tela_Ex_Cliente)

    # Label e Entry do NOME
    VarEx_Cliente = StringVar()
    VarEx_Cliente.set("")
    LblExcNome_Cliente = Label(FrExCliente, text="NOME:", font=Fonte11B, bg=Cinza_Romano, fg=Branco)
    LblExcNome_Cliente.place(x=5, y=45)
    CMBEx_Cliente = Combobox(FrExCliente, font=Fonte11, width=40, textvariable=VarEx_Cliente)
    CMBEx_Cliente.set("SELECIONE")
    CMBEx_Cliente['values'] = CMBClientes()
    CMBEx_Cliente["state"] = 'readonly'
    CMBEx_Cliente.place(x=80, y=45)
    CMBEx_Cliente.focus()
    CMBEx_Cliente.bind("<<ComboboxSelected>>", Select_CMB_Cliente)
    CMBEx_Cliente.bind("<Escape>", Sair_Tela_Ex_Cliente)
    CMBEx_Cliente.bind("<Return>", Deletar_Cliente)
    FrExCliente.option_add('*TCombobox*Listbox.font', Fonte11)
    FrExCliente.option_add('*TCombobox*Listbox.selectBackground', Verde)
    FrExCliente.option_add('*TCombobox*Listbox.background', Branco)
    FrExCliente.option_add('*TCombobox*Listbox.selectForeground', Branco)
    # -----------------------------------------------------------------------------------------------------------------
    # BOTÕES.....
    # Botão Salvar Prazo
    btExcluir_Prazo = Button(Tela_Ex_Cliente, bg=Verde, image=Foto_Ex_Save_Cliente, activebackground=Verde,
                             command=Deletar_Cliente, borderwidth=0)
    btExcluir_Prazo.image = Foto_Ex_Save_Cliente
    btExcluir_Prazo.place(x=350, y=12)
    # Botão Sair Prazo
    btExcluirSair_Prazo = Button(Tela_Ex_Cliente, image=Foto_Sair_Ex_Cliente, bg=Verde, activebackground=Verde,
                                 command=Sair_Tela_Ex_Cliente, borderwidth=0)
    btExcluirSair_Prazo.image = Foto_Sair_Ex_Cliente
    btExcluirSair_Prazo.place(x=404, y=12)
    # -----------------------------------------------------------------------------------------------------------------
# ------------------------ FIM ----------------------------------------------------------------------------------------
def Cadastro_Ocorrencia():

    def Salvar_BO():
        Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
        Cursor_Salvar_BO = Conexao.cursor()
        Horario = Lbl_Horario['text']
        Data_Orig = datetime.datetime.strptime(Var_Data_Bo.get(), '%d/%m/%Y')
        Data_Form = datetime.datetime.strftime(Data_Orig, '%Y/%m/%d')
        Confirma_Bo = messagebox.askyesno("CONFIRMA", "VOCÊ DESEJA SALVAR ESSA OCORRÊNCIA", parent=Tela_Ocorrencia)
        if Confirma_Bo == True:
            BO = ("INSERT INTO OCORRENCIAS(IDOCORRENCIA, DATA, HORARIO, USUARIO, ASSUNTO, DESCRICAO)"
                  "VALUES(%s, %s, %s, %s, %s, %s);")
            Paramentros_BO = (Var_Cod_BO.get(), Data_Form, Horario, Var_User.get(), Var_Assunto.get(),
                              Ent_Descricao.get("1.0",END))
            Cursor_Salvar_BO.execute(BO, Paramentros_BO)
            Conexao.commit()
            Conexao.close()
            messagebox.showinfo("SUCESSO", "OCORRÊNCIA CADASTRADO COM SUCESSO", parent=Tela_Ocorrencia)
            Tela_Ocorrencia.destroy()
        else:
            Var_Cod_BO.set("")
            Var_Assunto.set("")
            Ent_Descricao.delete('1.0', END)
            Ent_Cod_BO.focus()

    Tela_Ocorrencia = Toplevel()
    Tela_Ocorrencia.geometry("600x400+300+150")
    Tela_Ocorrencia.title("CADASTRO DE OCORRÊNCIAS")
    Tela_Ocorrencia.iconbitmap("Imagens//Icone//Logo_SFundo.ico")
    Tela_Ocorrencia.config(bg=Verde)

    Foto_Save_Bo = PhotoImage(file="Imagens//Botoes//Save.png")

    Fr_Principal = LabelFrame(Tela_Ocorrencia, bg=Verde)
    Fr_Principal.place(x=5, y=5, width=590, height=390)

    Fr_Dt_Hr = LabelFrame(Fr_Principal, bg=Verde, text="DATA E HORÁRIO DA OCORRÊNCIA", fg=Branco, font=Fonte8B)
    Fr_Dt_Hr.place(x=5, y=60, width=580, height=60)

    Fr_Dados = LabelFrame(Fr_Principal, bg=Verde, text="DADOS DA OCORRÊNCIA", fg=Branco, font=Fonte8B)
    Fr_Dados.place(x=5, y=125, width=580, height=250)
    # -----------------------------------------------------------------------------------------------------------------
    # Labels Cod Ocorrencia
    # Label de Assunto
    Var_Cod_BO = StringVar()
    Lbl_Cod_BO = Label(Fr_Principal, text="CÓDIGO:", bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_Cod_BO.place(x=5, y=20)
    Ent_Cod_BO = Entry(Fr_Principal, font=Fonte12, textvariable=Var_Cod_BO, width=10, justify=CENTER)
    Ent_Cod_BO.place(x=100, y=20)
    Ent_Cod_BO.focus()
    # -----------------------------------------------------------------------------------------------------------------
    # Label e Date de DATA da Ocorrencia
    Var_Data_Bo = StringVar()
    Lbl_Data_Bo = Label(Fr_Dt_Hr, text="DATA:", bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_Data_Bo.place(x=5, y=5)
    Ent_Data = DateEntry(Fr_Dt_Hr, date_pattern='dd/MM/yyyy', width=12, bg=Verde, fg=Branco, font=Fonte12,
                              headersbackground=Branco, borderwidth=2, selectbackground=Verde,
                              headersforeground=Cinza60, textvariable=Var_Data_Bo)
    Ent_Data.place(x=80, y=5)
    # -----------------------------------------------------------------------------------------------------------------
    # Labels Horario
    Data = time.localtime()
    Lbl_Hor_Bo = Label(Fr_Dt_Hr, text="HORÁRIO:", bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_Hor_Bo.place(x=250, y=5)
    Lbl_Horario = Label(Fr_Dt_Hr, text=f"{Data.tm_hour} : {Data.tm_min} : {Data.tm_sec}", font=Fonte12B, fg=Gold,
                        bg=Verde)
    Lbl_Horario.place(x=350, y=5)
    # -----------------------------------------------------------------------------------------------------------------
    # Labels Usuário
    Var_User = StringVar()
    Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
    Cursor_Usuario = Conexao.cursor()
    Cursor_Usuario.execute("SELECT NOME FROM LOGADO")
    for log in Cursor_Usuario.fetchall():
        Var_User.set(str(log[0]).title())
    Conexao.close()
    Lbl_User = Label(Fr_Dados, text="USUÁRIO:", bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_User.place(x=5, y=5)
    Ent_User = Entry(Fr_Dados, font=Fonte12, bg=Branco, fg=Preto, textvariable=Var_User, width=35)
    Ent_User.place(x=120, y=5)
    # -----------------------------------------------------------------------------------------------------------------
    # Label de Faixa Separação
    Lbl_Faixa1 = Label(Fr_Dados, text="--"*56, bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_Faixa1.place(x=5, y=27)
    # Label de Faixa Separação
    Lbl_Faixa2 = Label(Fr_Dados, text="--" *56, bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_Faixa2.place(x=5, y=72)
    # -----------------------------------------------------------------------------------------------------------------
    # Label de Assunto
    Var_Assunto = StringVar()
    Lbl_Assunto = Label(Fr_Dados, text="ASSUNTO:", bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_Assunto.place(x=5, y=50)
    Ent_Assunto = Entry(Fr_Dados, font=Fonte12, bg=Branco, fg=Preto, textvariable=Var_Assunto, width=35)
    Ent_Assunto.place(x=120, y=50)
    # -----------------------------------------------------------------------------------------------------------------
    # Label de Descrição
    Lbl_Descricao = Label(Fr_Dados, text="DESCRIÇÃO:", bg=Verde, fg=Branco, font=Fonte12B)
    Lbl_Descricao.place(x=5, y=94)
    Ent_Descricao = Text(Fr_Dados, width=55, height=7, font=Fonte11)
    Ent_Descricao.place(x=120, y=94)

    # BOTÕES.....
    # Botão Salvar Ocorrencia
    btExcluir_Prazo = Button(Fr_Principal, bg=Verde, image=Foto_Save_Bo, activebackground=Verde, borderwidth=0,
                             command=Salvar_BO)
    btExcluir_Prazo.image = Foto_Save_Bo
    btExcluir_Prazo.place(x=524, y=7)

# ------------------------ FIM ----------------------------------------------------------------------------------------
Menu_Main = Menu(Janela)
ConsultaMenu = Menu(Menu_Main, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
CadastroMenu = Menu(Menu_Main, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
EntretenimentoMenu = Menu(Menu_Main, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
GerenciamentoMenu = Menu(Menu_Main, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
GraficoMenu = Menu(Menu_Main, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
Consulta_Vendas = Menu(Menu_Main, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
CatalogoMenu = Menu(Menu_Main, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)

Clientes_Menu = Menu(CadastroMenu, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
Clientes_Menu.add_command(label='INCLUIR', font=Fonte11B, accelerator="Ctrl+C", command=Cadastro_Clientes)
Clientes_Menu.add_command(label='EXCLUIR', font=Fonte11B, command=Excluir_Clientes)

Usuario_Menu = Menu(CadastroMenu, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
Usuario_Menu.add_command(label='INCLUIR', font=Fonte11B, accelerator="Ctrl+U", command=Cadastro_usuario)
Usuario_Menu.add_command(label='EXCLUIR', font=Fonte11B)

Ocorrencia_Menu = Menu(CadastroMenu, background=Cinza_Romano, fg=Branco, tearoff=False, activebackground=Verde)
Ocorrencia_Menu.add_command(label='INCLUIR', font=Fonte11B, command=Cadastro_Ocorrencia)
Ocorrencia_Menu.add_command(label='EXCLUIR', font=Fonte11B)

Menu_Main.add_cascade(label="ARQUIVO", menu=CadastroMenu, font=Fonte11B)
Menu_Main.add_cascade(label="CONSULTAS", menu=ConsultaMenu, font=Fonte11B)
Menu_Main.add_cascade(label="GERENCIAMENTO", menu=GerenciamentoMenu, font=Fonte11B)

ConsultaMenu.add_cascade(label="VENDAS", menu=Consulta_Vendas, font=Fonte11B)

CadastroMenu.add_cascade(label='CLIENTES', menu=Clientes_Menu, font=Fonte11B)
CadastroMenu.add_cascade(label='USUÁRIO', menu=Usuario_Menu, font=Fonte11B)
CadastroMenu.add_cascade(label='OCORRÊNCIA', menu=Ocorrencia_Menu, font=Fonte11B)

CadastroMenu.add_separator()
CadastroMenu.add_command(label="EXIT", font=Fonte12B, activebackground=Verde, command=Sair)
Janela.config(menu=Menu_Main)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Acompanhamento do Mês
LblAcompanhamento = LabelFrame(Janela, tex="ACOMPANHAMENTO", bg=Verde, fg=Branco, font=Fonte10)
LblAcompanhamento.place(x=1205, y=12, width=290, height=310)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Faixa Top
Lbl_Faixa_Top = Label(Janela, bg=Verde)
Lbl_Faixa_Top.place(x=0, y=0, width=1500, height=10)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Faixa Booth
data = time.localtime()
Lbl_Faixa_Boo = Label(Janela, bg=Cinza_Romano, fg=Branco, font=Fonte11)
Lbl_Faixa_Boo["text"] = (f"SOFTWARE - Soluções em Softwares   -   \
{data.tm_mday}/{data.tm_mon}/{data.tm_year}")
Lbl_Faixa_Boo.place(x=0, y=730, width=1500, height=20)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Teclas de Atalhos
Janela.bind_all("<Control-u>", Cadastro_usuario)
Janela.bind_all("<Control-c>", Cadastro_Clientes)
# Desativando o Botão X da Tela
Janela.protocol("WM_DELETE_WINDOW", Desativar)
Janela.iconbitmap("Imagens//Icone//Logo_SFundo.ico")
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Criando Label pra Exibir Usuário Logado
LbUsuario = Label(LblAcompanhamento, text="USUÁRIO LOGADO:", bg=Verde, fg=Branco, font=Fonte8B)
LbUsuario.place(x=5, y=3)

LbLogado = Label(LblAcompanhamento, text="", bg=Verde, fg=Gold, font=Fonte10B)
LbLogado.place(x=5, y=17)

Conexao = pymysql.connect(host="localhost", user="root", passwd="P@ssw0rd", db="ONG")
Cursor_User_Logado = Conexao.cursor()
Cursor_User_Logado.execute("SELECT NOME FROM LOGADO")
for log in Cursor_User_Logado.fetchall():
    LbLogado.config(text=str(log[0]).upper())
Conexao.close()
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# COTAÇÃO DAS MOEDAS INTERNACIONAIS DOLAR E EURO
# ---------------------------------------------------------------------------------------------------------------------
try:
    Requisicao_Cotacao = requests.get("https://economia.awesomeapi.com.br/json/all")
    cotacao = json.loads(Requisicao_Cotacao.text)
    FrCotacao = LabelFrame(LblAcompanhamento, bg=Verde, fg=Branco, text="COTAÇÃO:", font=Fonte11B)
    FrCotacao.place(x=5, y=43, width=280, height=110)

    Foto_Moeda = PhotoImage(file="Imagens//Label//Moeda_Int.png")
    # Label da Imagem da Moeda
    Lbl_Img_Cotacao = Label(FrCotacao, image=Foto_Moeda, border=0, bg=Verde, borderwidth=0)
    Lbl_Img_Cotacao.image = Foto_Moeda
    Lbl_Img_Cotacao.place(x=2, y=0, width=100, height=70)

    LblDolar = Label(FrCotacao, text="DOLÁR:", bg=Verde, fg=Branco, font=Fonte12B, anchor=E)
    LblDolar.place(x=100, y=5, width=70)
    Valor_Dolar = Label(FrCotacao, text="R$  {:.2f}".format(float(cotacao['USD']['high'])), bg=Verde, fg=Branco,
                        font=Fonte14_H)
    Valor_Dolar.place(x=175, y=3)

    LblEuro = Label(FrCotacao, text="EURO:", bg=Verde, fg=Branco, font=Fonte12B, anchor=E)
    LblEuro.place(x=100, y=35, width=70)
    Valor_Euro = Label(FrCotacao, text="R$  {:.2f}".format(float(cotacao['EUR']['high'])), bg=Verde, fg=Branco,
                       font=Fonte14_H)
    Valor_Euro.place(x=175, y=33)

    LblAtualiz = Label(FrCotacao, text="Atualizado : ", bg=Verde, fg=Branco, font=Fonte8, anchor=E)
    LblAtualiz.place(x=10, y=68)
    Last_Atualiz = Label(FrCotacao, text=cotacao['EUR']['create_date'], bg=Verde, fg=Branco, font=Fonte8)
    Last_Atualiz.place(x=100, y=68)
    # ------------------------ FIM ------------------------------------------------------------------------------------
except:
    messagebox.showinfo("ERROR", "SEM CONEXÃO PARA COTAÇÃO DE MOEDAS INTERNACIONAIS\n* "
                                 "POR FAVOR CONECTE A INTERNET E FECHE/ABRA O PROGRAMA NOVAMENTE")

# PREVISÃO DE TEMPO
# ---------------------------------------------------------------------------------------------------------------------
VarCity = StringVar()
def Mostrar_Previsao(event=None):
    try:
        Requisicao_Tempo = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + VarCity.get()
                                        + "&appid=4dbc874d347d4c73de5ce9dc2e36112d")
        Previsao = json.loads(Requisicao_Tempo.text)

        try:
            Id_Imagem = Previsao['weather'][0]['main']
            Calculo = float(Previsao['main']['temp']) - float(273.15)
            Foto_Tempo = PhotoImage(
                file="C:\\Users\\padrao\\PycharmProjects\\Romano\\Imagens\\Tempo\\" + Id_Imagem + ".png")
            Lbl_Img_Tempo.config(image=Foto_Tempo)
            Lbl_Img_Tempo.image = Foto_Tempo
            # Label da Imagem da Temperatura
            Lbl_Temp = Label(FrPrevisao, bg=Verde, text=int(Calculo), font=Fonte20B, width=2, fg=Branco)
            Lbl_Temp.place(x=145, y=45)
            # Label da Imagem do GRaus Celcius
            Lbl_Grau = Label(FrPrevisao, bg=Verde, text="°C", font=Fonte20B, width=2, fg=Branco)
            Lbl_Grau.place(x=190, y=45)
        except:
            messagebox.showinfo("ERROR", "NÃO ENCONTRADA")

    except:
        messagebox.showinfo("ERROR", "SEM CONEXÃO COM A API")
        VarCity.set("")


# Labelframe da Previsão do Tempo
FrPrevisao = LabelFrame(LblAcompanhamento, bg=Verde, fg=Branco, text="TEMPO:", font=Fonte11B)
FrPrevisao.place(x=5, y=160, width=280, height=120)
# Imagem do Botão
Foto_Btn = PhotoImage(file="Imagens//Botoes//Arrow.png")
# Label e Entry da Cidade
LblCity = Label(FrPrevisao, text="CIDADE:", bg=Verde, fg=Branco, font=Fonte11B)
LblCity.place(x=5, y=5)
EntCity = Entry(FrPrevisao, font=Fonte12, width=17, border=2, textvariable=VarCity)
EntCity.place(x=80, y=5)
EntCity.bind("<Return>", Mostrar_Previsao)

# Label da Imagem da Moeda
Lbl_Img_Tempo = Label(FrPrevisao, border=0, bg=Verde)
Lbl_Img_Tempo.place(x=10, y=35, width=80, height=50)

Dicionario_tempo = {"clear sky": "01d", "few Clouds": "02d", "Scattered Clouds": "03d", "Clouds": "04d",
                    "shower rain": "09d", "rain": "10d", "thunderstorm": "11d", "snow": "13d", "mist": "50d"}
# BOTÕES.....
# Botão Mostrar
btn_Mostrar = Button(FrPrevisao, bg=Cinza_Romano, image=Foto_Btn, activebackground=Cinza60, border=0,
                     command=Mostrar_Previsao)
btn_Mostrar.image = Foto_Btn
btn_Mostrar.place(x=245, y=7)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Janela.mainloop()