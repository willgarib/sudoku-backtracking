from time import process_time

def LeiaMatrizLocal(NomeArquivo):
    """ Função que transforma a sequência de caracteres presente no arquivo (NomeArquivo) em uma lista de listas """
    
    # retorna a matriz lida se ok ou uma lista vazia senão
    
    # abrir o arquivo para leitura
    try:
        arq = open(NomeArquivo, "r")
    except:
        return [] # retorna lista vazia se deu erro
    
    # inicia matriz SudoKu a ser lida
    mat = [9 * [0] for k in range(9)]
    
    # ler cada uma das linhas do arquivo
    i = 0
    for linha in arq:
        v = linha.split()
        
        # Verivica se tem 9 elementos
        if len(v) != 9: return []       # lista vazia pois não está OK
        
        # transforma de str para int
        for j in range(len(v)):
            try: mat[i][j] = int(v[j])  # O elemento pode ser um 'str'
            except: return [] 
        i = i + 1
        
    # Verifica se estão entre '1' e '9'
    i = 0
    while True:
        for j in range(9):
            elem = mat[i][j]
            if elem < 0 or elem > 9: return []
        i = i + 1
        if i > 8: break
            
    # fechar arquivo e retorna a matriz lida e parcialmente consistida      
    arq.close()
    return mat
def TestaModelo(S):
    """ Função que verifica se a matriz é um modelo de susoku """
    
    for i in range(len(S)): # i = linhas
        for j in range(len(S[0])): # j = colunas
            # Se o elemento ainda não foi calculado não verifica
            if S[i][j] == 0: continue
            # Valida o número que esta na posição (i,j) na própria posição
            if not Valida(S, S[i][j], (i, j)): return False
    return True
def primt(Titulo, Mat):
    """ Função que imprime qualquer mariz utilizando um formato com melhor visualização """

    # Impime o Título
    print(30 * "-")
    print(" * * *", Titulo, "* * *")
    print()

    # Imprime a matriz destacando os quadrados internos (3x3)
    for i in range(len(Mat)): # i = linhas
        print(" ", end="")    
        for j in range(len(Mat[0])): # j = colunas
            if (j + 1) % 3 != 0: print(Mat[i][j], " ", end="")
            else: print(Mat[i][j], "   ", end="") # Separa a lateral do quadrado
        print() # Pula de linha
        
        if (i + 1) % 3 == 0: print() # Separa a parte de baixo do quadrado
def Valida(S, num, pos):
    """ Valida a possibilidade do número (num) na posição (pos) (Obs: (pos) é uma dupla) """
    
    # Checar linha
    for i in range(len(S[0])): # i = colunas
        # Se encontra o número (num) em uma posição != (pos), procurando na linha, retorna False
        if S[pos[0]][i] == num and pos[1] != i:
            return False

    # Checar coluna
    for i in range(len(S)): # i = linhas
        # Se encontra o número (num) em uma posição != (pos), procurando na coluna, retorna False
        if S[i][pos[1]] == num and pos[0] != i:
            return False

    # Checar box
    box_x = pos[1] // 3 # 'índice' do quadrado = (box_x,box_y)
    box_y = pos[0] // 3 # [box_k pertence a {0,1,2} for k in [x,y]]

    for i in range(box_y*3, box_y*3 + 3): # i = linhas do quadrado (i,j)
        for j in range(box_x * 3, box_x*3 + 3): # j = linhas do quadrado (i,j)
            # Se encontra o número (num) em uma posição != (pos), procurando no quadrado, retorna False
            if S[i][j] == num and (i,j) != pos:
                return False
            
    # Se NÂO encontra o número (num) em uma posição inválida, retorna True
    return True
def EncontraProximo(S):
    """ Retorna o indice (i, j) da próxima ocorrencia de zero no modelo """
    
    for i in range(len(S)): # i = 'linhas'
        for j in range(len(S[0])): # j = 'colunas'
            # Se o elemento (i,j) da matriz for  0  retorna sua localização 
            if S[i][j] == 0:
                return i, j  # linha, coluna

    return None
def Sudoku(S):
    """ Função que realmente resolve o problema """

    # Procura uma posição vazia
    encontra = EncontraProximo(S)

    # Se NÂO encontra, testa a solução e imprime. Zera a última posição para o teste do proximo condidato e retorna 
    if not encontra:
        if TestaModelo(S):  # Testa a resolução 
            global cont
            cont = cont + 1
            primt("Solução " + str(cont), S)
        S[8][8] = 0
        linha, coluna = 8, 8
        return False
    # Se encontra, define a posição a ser calculada
    else:
        linha, coluna = encontra

    # Testa todos os números possíveis
    for i in range(1,10):
        if Valida(S, i, (linha, coluna)):
            S[linha][coluna] = i

            # Resolve novamente o problema agora com uma casa a mais preenchida (Caso já esteja resolvido, retorna True) 
            if Sudoku(S):
                return True

            # Prepara a posição para um novo número
            S[linha][coluna] = 0

    # Retorna False após todos os números serem testados
    return False
def main():
    """ Função que inicia as referencias necessárias e efetua o loop requerido """
    
    global cont
    
    while True:
        print()

        # Inicia as referencias necessárias
        arq = input("Nome do arquivo que contém o sudoku: ")
        if arq == "fim": break
        s = LeiaMatrizLocal(arq)

        # Se houver algum erro no arquivo, solicita um novo arquivo
        if len(s) == 0 or not TestaModelo(s):
            print("Há um erro no arquivo, não existem soluções para este")
            print(53 * "-")
            continue

        # Imprimr a matriz do arquivo (arq)
        primt("Matriz inicial", s)

        # Procura soluções e, caso encontre, as imprime  (Conta o tempo da resolução)
        t1 = process_time()
        Sudoku(s)
        t2 = process_time()

        # Indica a quantidade de soluçoes enconrtradas e que foram verificadas
        if cont == 0: print("Não existem soluções")
        elif cont == 1: print("A solução foi verificada")
        else: print("Todas as " + str(cont) + " soluções foram verificadas")
        print("Resolução em " + str(t2 - t1) + " segundos")

        # Zera o contador de soluções
        cont = 0
        
        
        
cont = 0

main()
