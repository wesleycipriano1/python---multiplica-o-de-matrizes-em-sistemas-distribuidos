import socket
import threading
#import pickle
import os
import json

# Obter o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Definir o diretório de trabalho para o diretório do script
os.chdir(script_dir)

def carregar_matriz(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        
        size = [int(x) for x in lines[0].strip().split()]
        num_rows, num_cols = size

        
        matrix = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]

        for i in range(1, len(lines)):
            row = [float(x) for x in lines[i].strip().split()]
            matrix[i-1] = row

    return matrix, num_rows, num_cols

def dividir_matriz(matriz, partes, eixo=0):
    tamanho_parte = len(matriz) // partes
    partes_divididas = []

    if eixo == 0:  
        partes_divididas = [matriz[i:i + tamanho_parte] for i in range(0, len(matriz), tamanho_parte)]
    elif eixo == 1:  
        partes_divididas = [list(map(list, zip(*matriz)))[i:i + tamanho_parte] for i in range(0, len(matriz[0]), tamanho_parte)]

    return partes_divididas


def atender_cliente(client_socket, parte_a, parte_b):
    
    serialized_parte_a = json.dumps(parte_a)
    serialized_parte_b = json.dumps(parte_b)

    # Enviar as partes da matriz
    client_socket.send(serialized_parte_a.encode('utf-8'))
    client_socket.send(serialized_parte_b.encode('utf-8'))

    print("\n matriz a enviada")
    print("\n matriz b enviada")

    
    client_signal = client_socket.recv(15)  
    if client_signal == b'Ready':
        

    
        serialized_resultado = client_socket.recv(81920).decode('utf-8')  
        resultado = json.loads(serialized_resultado)

        print("Resultado recebido do cliente:", resultado)

    client_socket.close()


MAX_CLIENTS = 2 # ppra teste eu botei dois cliente,usei a aboragem cliente servidor pra ficar mais facil do que por computador central e remotos
clientes_conectados = 0

# Carregar as matrizes dos arquivos
arquivo_matriz_a = '1024.txt'
arquivo_matriz_b = arquivo_matriz_a

matriz_a, num_rows_a, num_cols_a = carregar_matriz(arquivo_matriz_a)
matriz_b, num_rows_b, num_cols_b = carregar_matriz(arquivo_matriz_b)


partes_a = dividir_matriz(matriz_a, MAX_CLIENTS, eixo=0)
partes_b = dividir_matriz(matriz_b, MAX_CLIENTS, eixo=1)

# Configurações do servidor

#host = '192.168.0.108'  # Endereço do servidor rodar em rede 
host='127.0.0.1' #rodar local
port = 12345    # Porta do servidor

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Aguardando conexões de até {MAX_CLIENTS} clientes...")


threads_clientes = []
matriz_resultante=[]

tempo_total_cliente = 0
numero_total_de_threads= 0

def lidar_com_cliente(client_socket):
    global clientes_conectados
    global tempo_total_cliente
    global numero_total_de_threads

    
    if partes_a and partes_b:
        parte_a_cliente = partes_a.pop(0)  
        parte_b_cliente = partes_b.pop(0)  

        
        serialized_parte_a = json.dumps(parte_a_cliente)
        serialized_parte_b = json.dumps(parte_b_cliente)

        
        client_socket.send(serialized_parte_a.encode('utf-8'))
        client_socket.send(serialized_parte_b.encode('utf-8'))

        
        clientes_conectados += 1
        print(f"Cliente {clientes_conectados} conectado.")
        BUFFER_SIZE = 41943040  #alterando o valor do buffer aumenta o tamanho da matriz a ser calculada,como optei por fazer a de 1024 deixei o buffer assim,
        # porem esse valor suporta ate 40 megas,e da pra fazer a maior tranquilamente caso de estouro só multiplicar por dois que suporta 80 megas
        
        serialized_dados = client_socket.recv(BUFFER_SIZE)  
        dados_cliente = json.loads(serialized_dados.decode('utf-8'))

        resultado_cliente = dados_cliente["resultado"]
        tempo_de_execucao = dados_cliente["tempo_de_execucao"]

        # Soma o tempo de execução deste cliente ao tempo total
        tempo_total_cliente += tempo_de_execucao

        num_threads = dados_cliente["num_threads"]
        numero_total_de_threads += num_threads

        # Imprimir as informações que vem do cliente,usei isso s[o pra debugar mais facil,entender o que o cliente tava retornando]
        print(f"Resultado recebido do cliente {clientes_conectados}:")
        for row in resultado_cliente:
            print(row)

        print(f"Tempo de execução do cliente {clientes_conectados}: {tempo_de_execucao} segundos")
        print(f"Número de threads do cliente {clientes_conectados}: {num_threads}")
        matriz_resultante.extend(resultado_cliente)

    client_socket.close()




while clientes_conectados < MAX_CLIENTS:
    client_socket, client_address = server_socket.accept()

    
    client_thread = threading.Thread(target=lidar_com_cliente, args=(client_socket,))
    threads_clientes.append(client_thread)
    client_thread.start()


for thread in threads_clientes:
    thread.join()
print("\nMatriz Final:")
for row in matriz_resultante:
    print(row)
print("\n")
print("variação p5")
print("foram usadas ",numero_total_de_threads," threads ao total")
print("computadores remotos= ",MAX_CLIENTS)
print("tempo total de multiplicaçação é ",tempo_total_cliente," segundos")
print("numero de linhas= ",num_rows_a)
print("numero de colunas= ",num_cols_b)


server_socket.close()