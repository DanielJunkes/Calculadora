import customtkinter as ctk

#configuração inicial da tela
tela = ctk.CTk()
tela.title('Calculadora')
tela.geometry("400x500")
tela.minsize(400, 500)
tela.grid_columnconfigure((0, 1, 2, 3), weight=1)
tela.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

def apagar(): #apgar todo o texto
    label.configure(text='')

def apagarUltimo(): #apagar o ultimo digito
    text = label.cget('text')
    texto = ''
    for i in range(len(text)-1):
        texto += text[i]
    label.configure(text=texto)
def montarOperacao(digito): #configura o texto para ser possivel realizar as operacoes
    operacao = ""
    operacao += label.cget('text')
    if len(operacao) == 0:
        if not digito in ('×÷+-,'): #impede comecar operacao com sinal aritmetico
            operacao += digito
    elif (operacao.endswith('×') or operacao.endswith('+') or operacao.endswith('-')
            or operacao.endswith('÷') or operacao.endswith(',')): #se o ultimo digito for um sinal aritmetico e o digito clicado tbm for,
        if not digito in ('×÷+-,'):                               #substitui o sinal antigo pelo novo
            operacao += digito
        else:
            apagarUltimo()
            operacao = label.cget('text')
            operacao += digito
    else:
        operacao += digito
    label.configure(text=operacao)
def operacoes(operacao, conta):
    indexOp = conta.index(operacao) #procura o primeiro sinal aritmetico q foi recebido
    indexI = 0  #index inicial padrao da operacao
    indexF = len(conta) #index final padrao da operacao
    for i in range(indexOp - 1, -1, -1):  #procura o index incial percorrendo a string do sinal ate o inicio
        if conta[i] == '-' and i == 0:    # ex: 4+4/2, no final do for, o index inicial seria 1 pois encontrou o +
            indexI = i                    # e a expressao seria 4/2
            break
        elif conta[i] == '+' or conta[i] == '/' or conta[i] == '*' or conta[i] == '-':  #apos encontrar outro sinal, encerra o for
            indexI = i + 1
            break
    for i in range(indexOp + 1, indexF, +1): #procura o index final percorrendo a string do sinal ate o final dela,
                                            # ex: 4/4+2, no final do for o index final vai ser 4 e a expressao seria 4/4
        if conta[i] == '+' or conta[i] == '/' or conta[i] == '*' or conta[i] == '-': #apos encontrar outro sinal, encerra o for
            indexF = i
            break
    n1 = float(conta[indexI:indexOp])
    n2 = float(conta[indexOp + 1:indexF])
    expressao = conta[indexI:indexF] #pega a expressao q sera resolvida para substituir na string
    resultado = 0
    if operacao == '/':
        resultado = n1 / n2
    elif operacao == '*':
        resultado = n1 * n2
    elif operacao == '+':
        resultado = n1 + n2
    elif operacao == '-':
        resultado = n1 - n2
    return conta.replace(expressao, str(resultado)) #substitui a expressao resolvida pelo resultado, ex: 4+4/2, resolvemos o 4/2.
                                                    #A string ficaria 4+2
def resolver():
    conta = ''
    conta += label.cget('text')
    if '×' in conta or '÷' in conta or ',' in conta:  #substitui os simbolos para simbolos usaveis
        conta = conta.replace('×', '*')
        conta = conta.replace('÷', '/')
        conta = conta.replace(',', '.')
    while '/' in conta or '*' in conta:
        if '/' in conta:
            conta = operacoes('/', conta)
        if '*' in conta:
            conta = operacoes('*', conta)
    while '+' in conta or '-' in conta[1:]:
        indexSoma = 999 #verifica se ocorrera a soma ou a subtração primeiro caso tenha as 2 opcoes
        indexSub = 999
        if '+' in conta:
            indexSoma = conta.index('+')
        if '-' in conta[1:]:
            indexSub = conta.index('-')
        if indexSoma < indexSub:
            conta = operacoes('+', conta)
            if indexSub != 999:
                conta = operacoes('-', conta)
        else:
            conta = operacoes('-', conta)
            if indexSoma != 999:
                conta = operacoes('+', conta)

    if '.0' in conta and conta.endswith('0'): #remove o . de numeros inteiros
        aux = float(conta)
        conta = str(int(aux))
    else:
        conta = conta.replace('.', ',')
    label.configure(text=conta)

#layout da calculadora
frame = ctk.CTkFrame(tela, corner_radius=10)
frame.grid(row=0, rowspan=2, column=0, columnspan=4, padx=10, pady=20, sticky='ewns')
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

label = ctk.CTkLabel(frame, text="", font=(None, 30))
label.grid(row=0, column=0, padx=(0, 15), sticky='e')

num = 1
for i in range(5, 2, -1):
    for j in range(3):
        if j == 0:
            btn = ctk.CTkButton(tela, text=num, font=(None, 30))
            btn.configure(command=lambda x=str(num): montarOperacao(x))
            btn.grid(row=i, column=j, padx=(10, 10), pady=(0, 10), sticky='nswe')
        else:
            btn = ctk.CTkButton(tela, text=num, font=(None, 30))
            btn.configure(command=lambda x=str(num): montarOperacao(x))
            btn.grid(row=i, column=j, padx=(0, 10), pady=(0, 10), sticky='nswe')
        num += 1

btnApagar = ctk.CTkButton(tela, text='C', font=(None, 30), fg_color='transparent', border_color='gray',
                     border_width=2, corner_radius=10, text_color='red', hover_color='#0d0d0d',
                     command=apagar)
btnApagar.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky='nswe')
btnDivisao = ctk.CTkButton(tela, text='÷', width=90, height=60, font=(None, 30), fg_color='transparent', border_color='gray',
                           border_width=2, corner_radius=10, hover_color='#0d0d0d')
btnDivisao.configure(command=lambda x="÷": montarOperacao(x))
btnDivisao.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky='nswe')
btnMultiplicacao = ctk.CTkButton(tela, text='×', width=90, height=60, font=(None, 30), fg_color='transparent', border_color='gray',
                                 border_width=2, corner_radius=10, hover_color='#0d0d0d')
btnMultiplicacao.configure(command=lambda x="×": montarOperacao(x))
btnMultiplicacao.grid(row=2, column=2, padx=(0, 10), pady=(0, 10), sticky='nswe')

btnApagarUltimo = ctk.CTkButton(tela, text='←', font=(None, 30), fg_color='transparent', border_color='gray',
                                border_width=2, corner_radius=10, hover_color='#0d0d0d', command=apagarUltimo)
btnApagarUltimo.grid(row=2, column=3, padx=(0, 10), pady=(0, 10), sticky='nswe')

btnSoma = ctk.CTkButton(tela, text='+', font=(None, 30), fg_color='transparent', border_color='gray',
                        border_width=2, corner_radius=10, hover_color='#0d0d0d')
btnSoma.configure(command=lambda x="+": montarOperacao(x))
btnSoma.grid(row=3, column=3, padx=(0, 10), pady=(0, 10), sticky='nswe')

btnSubtracao = ctk.CTkButton(tela, text='-', font=(None, 30), fg_color='transparent', border_color='gray',
                             border_width=2, corner_radius=10, hover_color='#0d0d0d')
btnSubtracao.configure(command=lambda x="-": montarOperacao(x))
btnSubtracao.grid(row=4, column=3, padx=(0, 10), pady=(0, 10), sticky='nswe')

btnVirgula = ctk.CTkButton(tela, text=',', font=(None, 30), fg_color='transparent', border_color='gray',
                           border_width=2, corner_radius=10, hover_color='#0d0d0d')
btnVirgula.configure(command=lambda x=",": montarOperacao(x))
btnVirgula.grid(row=5, column=3, padx=(0, 10), pady=(0, 10), sticky='nswe')

btn0 = ctk.CTkButton(tela, text=0, font=(None, 30))
btn0.configure(command=lambda x=str(0): montarOperacao(x))
btn0.grid(row=6, column=1, padx=(0, 10), pady=(0, 10), sticky='nswe')

btnIgual = ctk.CTkButton(tela, text='=', font=(None, 30), fg_color='transparent', border_color='gray',
                         border_width=2, corner_radius=10, hover_color='#0d0d0d', command=resolver)
btnIgual.grid(row=6, column=3, padx=(0, 10), pady=(0, 10), sticky='nswe')

tela.mainloop()