


import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)



def load_matrix_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        matrix_size = int(lines[0].split()[0])  
        matrix = []

        for line in lines[1:]:
            row = [float(x) for x in line.strip().split()]
            matrix.append(row)

    return matrix




filename_matrix_a = 'm1.txt'
filename_matrix_b = 'm1.txt'

matrix_a = load_matrix_from_file(filename_matrix_a)
matrix_b = load_matrix_from_file(filename_matrix_b)

def multiply_matrices(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Numero de coluna da matriz 1 é diferente do numero de linhas da matriz 2")

    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            element = 0
            for k in range(len(matrix2)):
                element += matrix1[i][k] * matrix2[k][j]
            row.append(element)
        result.append(row)

    return result


filename_matrix_a = '1024.txt'
filename_matrix_b = '1024.txt'

matrix_a = load_matrix_from_file(filename_matrix_a)
matrix_b = load_matrix_from_file(filename_matrix_b)
num_rows_a = len(matrix_a)  
num_cols_a = len(matrix_a[0])  

num_rows_b = len(matrix_b)  
num_cols_b = len(matrix_b[0])

tempo_inicial = time.time()
resultado = multiply_matrices(matrix_a, matrix_b)
tempo_final = time.time()
tempo_de_multiplicacao = tempo_final - tempo_inicial


for row in resultado:
    print(row)
print("\n")
print("variação p1")
print("foram usadas ",0," threads ao total")
print("computadores remotos= ",0)
print("tempo total de multiplicaçação é ",tempo_de_multiplicacao," segundos")
print("numero de linhas= ",num_rows_a)
print("numero de colunas= ",num_cols_b)
