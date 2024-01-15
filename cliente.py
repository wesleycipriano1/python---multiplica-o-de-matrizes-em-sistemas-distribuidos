import socket
import threading
#import pickle
import os
import time
import json

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
#server_ip = '45.163.116.96'  # Endereço IP público para rodar em rede
server_ip='127.0.0.1' #rodar local
server_port = 12345 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))


BUFFER_SIZE = 41943040



serialized_parte_a = client_socket.recv(BUFFER_SIZE)  
parte_a_str = serialized_parte_a.decode('utf-8')
parte_a = json.loads(parte_a_str)

print("Parte A:")#alguns desses prints foram somente pra verificar o que tava sendo recebido
print(parte_a)

serialized_parte_b= client_socket.recv(BUFFER_SIZE)  
parte_b_str = serialized_parte_b.decode('utf-8')
parte_b= json.loads(parte_b_str)  

print("Parte B:")
print(parte_b)





num_cores = os.cpu_count()
num_threads = 1  


linhas_por_thread = len(parte_a) // num_threads
threads = []
resultados = [None] * num_threads  

start_time = time.time()


for i in range(num_threads):
    start_row = i * linhas_por_thread
    end_row = (i + 1) * linhas_por_thread if i < num_threads - 1 else len(parte_a)
    thread = threading.Thread(target=multiplicar_parte,
                              args=(parte_a, parte_b, start_row, end_row, resultados, i))
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()
    
resultado_final = [[sum(x * y for x, y in zip(row_a, col_b)) for col_b in parte_b] for row_a in parte_a]


end_time = time.time()
tempo_de_execucao = end_time - start_time


dados_para_enviar = {
    "resultado": resultado_final,
    "tempo_de_execucao": tempo_de_execucao,
    "num_threads": num_cores
}
serialized_dados = json.dumps(dados_para_enviar)


client_socket.send(serialized_dados.encode('utf-8'))

print("Resultado e informações enviados para o servidor.")


client_socket.close()






