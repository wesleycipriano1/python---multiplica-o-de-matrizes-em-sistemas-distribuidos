import socket
import threading
import pickle
import os

# Função para multiplicar a parte das matrizes
def multiplicar_parte(parte_a, parte_b, start_row, end_row, resultados, thread_index):
    matriz_resultado = []
    for i in range(start_row, end_row):
        linha_resultado = []
        for j in range(len(parte_b)):
            elemento = 0.0
            for k in range(len(parte_b[0])):
                elemento += parte_a[i][k] * parte_b[j][k]
            linha_resultado.append(elemento)
        matriz_resultado.append(linha_resultado)
    resultados[thread_index] = matriz_resultado

# Configurações do servidor
host = '127.0.0.1'  # Endereço do servidor
port = 12345       # Porta do servidor

# Conectar ao servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Receber a parte da matriz a
serialized_parte_a = client_socket.recv(8192)  # Tamanho do buffer
parte_a = pickle.loads(serialized_parte_a)
print("Parte A:")
print(parte_a)

# Receber a parte da matriz b
serialized_parte_b = client_socket.recv(8192)  # Tamanho do buffer
parte_b = pickle.loads(serialized_parte_b)
print("Parte B:")
print(parte_b)

# Configurar threads
num_cores = os.cpu_count()
num_threads = 1  # Usar uma thread por core

# Dividir as linhas da matriz a para as threads
linhas_por_thread = len(parte_a) // num_threads
threads = []
resultados = [None] * num_threads  # Lista para armazenar os resultados de cada thread

# Multiplicar usando threads
for i in range(num_threads):
    start_row = i * linhas_por_thread
    end_row = (i + 1) * linhas_por_thread if i < num_threads - 1 else len(parte_a)
    thread = threading.Thread(target=multiplicar_parte,
                              args=(parte_a, parte_b, start_row, end_row, resultados, i))
    threads.append(thread)
    thread.start()

# Aguardar todas as threads terminarem
for thread in threads:
    thread.join()

# Unir os resultados das threads
resultado_final = [elemento for linha in resultados for elemento in linha[0]]

print("Resultado Final:")
print(resultado_final)

# Enviar o resultado para o servidor
serialized_resultado = pickle.dumps(resultado_final)
client_socket.send(serialized_resultado)

print("Resultado enviado para o servidor.")

# Fechar a conexão
client_socket.close()
