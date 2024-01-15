import threading
import os
import time

# Obter o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Definir o diretório de trabalho para o diretório do script
# tive que fazer isso pq meu vscode não tava achando as matrizes,mesmo estando na mesma pasta,talvez em outra programa não precise 
os.chdir(script_dir)

def carregar_matriz(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        matrix_size = int(lines[0].split()[0])  
        matrix = []

        for line in lines[1:]:
            row = [float(x) for x in line.strip().split()]  
            matrix.append(row)

    return matrix

def multiplicar_linha(matrix1, row_index, matrix2):
    result_row = []
    for j in range(len(matrix2[0])):
        element = 0.0
        for k in range(len(matrix2)):
            element += matrix1[row_index][k] * matrix2[k][j]
        result_row.append(element)
    return result_row


def multiplicar_matriz(matrix1, matrix2, num_threads):
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Numero de colunas da matriz diferente do numero de linhas da matriz a ser multiplicada")

    result = []
    threads = []

    linhas_por_thread = len(matrix1) // num_threads

    for i in range(num_threads):
        start_row = i * linhas_por_thread
        end_row = (i + 1) * linhas_por_thread if i < num_threads - 1 else len(matrix1)
        
        thread = threading.Thread(target=lambda start=start_row, end=end_row: 
                                  result.extend(multiplicar_linha(matrix1, row_idx, matrix2) for row_idx in range(start, end)))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return result



# Carregar as matrizes dos arquivos
arquivo_matriz_a = '1024.txt'
arquivo_matriz_b = '1024.txt'

matrix_a = carregar_matriz(arquivo_matriz_a)
matrix_b = carregar_matriz(arquivo_matriz_b)
num_rows_a = len(matrix_a)  
num_cols_a = len(matrix_a[0])  

num_rows_b = len(matrix_b)  
num_cols_b = len(matrix_b[0])  

# aqui pega o numero de nucleos e da pra mudar de p2 ate p4 só variando os valores
num_threads = os.cpu_count()//2


# Mede o tempo
tempo_inicial = time.time()

resultado = multiplicar_matriz(matrix_a, matrix_b, num_threads)
tempo_final = time.time()
tempo_de_multiplicacao = tempo_final - tempo_inicial


for row in resultado:
    print(row)

print("Matriz Resultante:")
for row in resultado:
    print(" ".join(str(element) for element in row))
print("\n")
# como consigo alterar o numero de threads apenas manipulando a variavel com a quantidade de nucles do processador
# fazer umas condicionais apenas mudando o rotulo de impressão é mais rapido,poderia tbm pedir do usuario pra digitar e ver qual varia ele quer,mas não achei pertinente 
if(num_threads==(os.cpu_count())):
    variacao="p2"
if(num_threads==(os.cpu_count()*2)):
    variacao="p3"
if(num_threads==(os.cpu_count()//2)):
    variacao="p4"
print("variação ",variacao)
print("foram usadas ",num_threads," threads ao total")
print("computadores remotos= ",0)
print("tempo total de multiplicaçação é ",tempo_de_multiplicacao," segundos")
print("numero de linhas= ",num_rows_a)
print("numero de colunas= ",num_cols_b)
