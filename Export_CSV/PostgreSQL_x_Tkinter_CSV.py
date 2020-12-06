import tkinter as tk
from tkinter import filedialog  # Dialogos comuns para permitir ao usuário especificar um arquivo para abrir ou salvar.
from tkinter import simpledialog #Pacote pequena caixa de dialogo
from pandas import DataFrame  # Importando Pandas, somente módulo : Dataframe
import psycopg2 #Pacote Conexão PostgreSQL

#Criando a Conexao com o banco
con = psycopg2.connect(host='', database='', user='', password='')


# Listas vazias, receber dados do banco
cars = []
cars1 = []

# Obtendo um Cursor
cursor = con.cursor()

root = tk.Tk()  # instanciamos a classe TK() atraves da variavel root

# Width: Largura do widget
# Height: Altura do widget
# bg: Cor de fundo do widget
# Relif:Escolhe qual será o estilo da borda de um widget(Raised:aumentado /Sunken:afundado /Flat:plano /Groove:Sulco/ Ridge:cume)
# fg: Cor do texto do widget

canvas1 = tk.Canvas(root, width=300, height=300, bg='lightsteelblue2', relief='raised')
canvas1.pack()


#Funcao botao contas a pagar
def Pagar():
    global pg
    
    def Pergunta(): #Funcao solicitacao periodo usuario, inicial e final
        # Variavel Global
        global periodo1
        global periodo2
        periodo = 'PERÍODO'
        periodo1 = simpledialog.askstring(title="Período",
                                          prompt="Período inicial:")

        periodo2 = simpledialog.askstring(title="Período",
                                          prompt="Período final:")
        

    Pergunta() #Chamada de Funcao

    sql_pagar = '''SELECT 
      p.pagjdocumento  as Numero_documento,
      ''  as codigo_Historico,
      p.pagjobs as historico,
      c.partrazao as nome_fornecedor,
      c.partcnpjcpf as cnpj,
      p.pagjdreconta as codigo_pgto,
      d.drecdescricao as descricao_pgto,
      '' as classificacao_contabil,
      '' as descricao_contabil,
      p.pagjjuro as juros,
      p.pagjdesconto as descontos,
      p.pagjpago as valor_recebido,
      p.pagjpagamento as data
    FROM 
      PAGJ P 
    left join part c on c.PARTCODIGO  = p.PAGJFORNECEDOR   
    left join drec d on p.PAGJDRECONTA = d.DRECCODIGO 
    left join dret t on t.DRETCODIGO = drectitulo

    where p.pagjpagamento BETWEEN '{0}' and '{1}'
    '''

    comando = cursor.execute(sql_pagar.format(periodo1, periodo2)) #Chamada sql + parametros 

    for linha in cursor.fetchall(): #Obtendo e salvando dados em lista : cars1
        cars1.append(linha)

    pg = DataFrame(cars1, columns=['numero_documento', 'codigo_historico', 'historico', 'nome_fornecedor', 'cnpj',
                                   'codigo_pgto', 'descrico_pgto', 'classificacao_contabil', 'descricao_contabil',
                                   'juros', 'descontos', 'valor_recebido', 'data'])

    export_file_path1 = filedialog.asksaveasfilename(defaultextension='.csv')  # Solicitacao do nome do arquivo
    pg.to_csv(export_file_path1, encoding='utf-8', index=False, header=True)
    

#Funcao botao Contas a receber
def Receber():
    global df

    def Pergunta2(): #Funcao solicitacao periodo usuario, inicial e final
        # Variavel Global
        global periodo3
        global periodo4
        periodo = 'PERÍODO'
        periodo3 = simpledialog.askstring(title="Período",
                                          prompt="Período inicial:")

        periodo4 = simpledialog.askstring(title="Período",
                                          prompt="Período final:")
        

    Pergunta2()

    sql_receber = '''
    SELECT 
      r.recjdocumento  as Numero_documento,
      ''  as codigo_Historico,
      r.recjobs as historico,
      c.partrazao as nome_fornecedor,
      c.partcnpjcpf as cnpj,
    case 
      when ff.FATJBXCCRR = 0 and ff.fatjbxcaixa <> 0 then ff.fatjbxcaixa
      when ff.FATJBXCCRR > 0 and ff.fatjbxcaixa = 0 then ff.fatjBXCCRR 
    ELSE 
      999999
    end as codigo_pgto,
    case 
      when ff.fatjBXCCRR = 0 and ff.fatjbxcaixa <> 0 then 'Pgto feito no caixa'
      when ff.fatjBXCCRR > 0 and ff.fatjbxcaixa = 0 then cc.CCRRDESCRICAO 
      when ff.fatjBXCCRR = 0 and ff.fatjbxcaixa = 0 then 'PGTO FEITO NO MAPA: ' || ff.fatjBXMAPA 
    ELSE 
      'Nao Definido'
    end as descricao_pgto,
      r.recjdreconta as classificacao_contabil,
      d.drecdescricao as descricao_contabil,
      r.recjjuros as juros,
      r.recjdesconto as descontos,
      r.recjvalor as valor_recebido,
      substring(CAST(ff.FATJPAGAMENTO as varchar),9,2)  || '/' || substring(CAST(ff.FATJPAGAMENTO as varchar),6,2)  || '/' || substring(CAST(ff.FATJPAGAMENTO as varchar),1,4) as data 
    FROM 
      recj r
    left join fatj ff on ff.FATJCODIGO = r.recjfatura  
    left join part c on c.PARTCODIGO  = ff.FATJCLIENTE  
    left join ccrr cc on cc.CCRRCODIGO = ff.FATJBXCCRR 
    left join drec d on d.DRECCODIGO = r.RECJDRECONTA 
    where ff.FATJPAGAMENTO BETWEEN '{0}' and '{1}'
    '''

    
    recebidas = cursor.execute(sql_receber.format(periodo3, periodo4)) #Obtendo e salvando dados em lista : cars1
    

    for linha in cursor.fetchall(): #Obtendo e salvando dados em lista : cars
        cars.append(linha)

    df = DataFrame(cars, columns=['numero_documento', 'codigo_historico', 'historico', 'nome_fornecedor', 'cnpj',
                                  'codigo_pgto', 'descrico_pgto', 'classificacao_contabil', 'descricao_contabil',
                                  'juros', 'descontos', 'valor_recebido', 'data'])

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')  # Solicitacao do nome do arquivo
    df.to_csv(export_file_path, index=False, header=True)

#chamando comando: funcao pagar
contas_a_pagar = tk.Button(text='CONTAS A PAGAR', command=Pagar, bg='green', fg='white',
                             font=('helvetica', 12, 'bold'))  # Nome do Botão em verde , e fonte da letra
canvas1.create_window(150, 150, window=contas_a_pagar)

contas_a_receber = tk.Button(text="CONTAS A RECEBER", command=Receber, bg='green', fg='White', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 80, window=contas_a_receber) #chamando funcao receber

# Criar botao de Quit, destruir o Root
quit1 = tk.Button(text="SAIR", command=root.destroy, fg="red")
canvas1.create_window(150, 200, window=quit1)

root.mainloop()  # método root.mainloop() para exibirmos a tela. Sem o event loop, a interface não sera exibida.

# desconectando...
cursor.close()
con.close()
