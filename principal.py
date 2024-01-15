import socket
import threading
import pickle
import os

# Obter o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Definir o diretório de trabalho para o diretório do script
os.chdir(script_dir)

def carregar_matriz(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        # Primeira linha contém o tamanho da matriz
        size = [int(x) for x in lines[0].strip().split()]
        num_rows, num_cols = size

        # Inicializar a matriz com zeros
        matrix = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]

        for i in range(1, len(lines)):
            row = [float(x) for x in lines[i].strip().split()]
            matrix[i-1] = row

    return matrix, num_rows, num_cols

def dividir_matriz(matriz, partes):
    tamanho_parte = len(matriz) // partes
    partes_divididas = [matriz[i:i + tamanho_parte] for i in range(0, len(matriz), tamanho_parte)]
    return partes_divididas

def atender_cliente(client_socket, parte_a, parte_b):
    serialized_parte_a = pickle.dumps(parte_a)
    serialized_parte_b = pickle.dumps(parte_b)
    
    client_socket.send(serialized_parte_a)
    client_socket.send(serialized_parte_b)
    print("\n matriz a enviada")
    print("\n matriz b enviada")

    # Receber o sinal do cliente
    client_signal = client_socket.recv(15)  # Tamanho do buffer
    if client_signal == b'Ready':
        # O cliente está pronto para enviar o resultado

        # Receber o resultado do cliente
        serialized_resultado = client_socket.recv(4096)  # Tamanho do buffer
        resultado = pickle.loads(serialized_resultado)

        print("Resultado recebido do cliente:", resultado)

    client_socket.close()

MAX_CLIENTS = 4
clientes_conectados = 0

# Carregar as matrizes dos arquivos
arquivo_matriz_a = '4.txt'
arquivo_matriz_b = '4.txt'

matriz_a, num_rows_a, num_cols_a = carregar_matriz(arquivo_matriz_a)
matriz_b, num_rows_b, num_cols_b = carregar_matriz(arquivo_matriz_b)

# Dividir as matrizes para serem multiplicadas pelos clientes
partes_a = dividir_matriz(matriz_a, MAX_CLIENTS)
partes_b = dividir_matriz(matriz_b, MAX_CLIENTS)

# Configurações do servidor
host = '127.0.0.1'  # Endereço do servidor
port = 12345       # Porta do servidor

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Aguardando conexões de até {MAX_CLIENTS} clientes...")

# Função para lidar com um cliente
def lidar_com_cliente(client_socket):
    global clientes_conectados

    # Obtenha uma parte da matriz para este cliente
    parte_a_cliente = partes_a.pop(0)  # Pega a próxima parte da matriz a
    parte_b_cliente = partes_b.pop(0)  # Pega a próxima parte da matriz b

    # Envie as partes da matriz para o cliente
    serialized_parte_a = pickle.dumps(parte_a_cliente)
    serialized_parte_b = pickle.dumps(parte_b_cliente)
    client_socket.send(serialized_parte_a)
    client_socket.send(serialized_parte_b)


    # Incremente o contador de clientes conectados
    clientes_conectados += 1
    print(f"Cliente {clientes_conectados} conectado.")
    


    # Receber o resultado do cliente
    serialized_resultado = client_socket.recv(8192)  # Tamanho do buffer
    resultado = pickle.loads(serialized_resultado)
    
    print("Resultado recebido do cliente:", resultado)
    
    client_socket.close()

# Aceitar conexões e criar threads para atender cada cliente
while clientes_conectados < MAX_CLIENTS:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=lidar_com_cliente, args=(client_socket,))
    client_thread.start()
