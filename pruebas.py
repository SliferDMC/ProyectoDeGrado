import numpy as np
import pandas as pd
from statistics import mode

def is_Number(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def calculate_average(array):
    avr = 0
    cont = 0
    for i in array:
        if is_Number(i):
            avr += float(i)
            cont += 1
    return avr/cont

def vector_is_number_or_string(array):
    for i in array:
        if is_Number(i):
            return True
    return False

def complete_void(array, v):
    for i in range(len(array)):
        if array[i] == '-':
            array[i] = v
    return array



array = np.array([['Numero','vacio','palabras'],[1,2,3],[4,'-',6],[7,'hola','hola']])
array2 = np.array([['3,2', 'hola'],['2,3','8']])
df = pd.DataFrame(array)

a = '2'

b = float(a)

print(b)

















"""
print(df)
print(df.shape)

df.drop(columns=[0,1], inplace=True)

print(df)
print(df.shape)

aux = 1
aux += 1
print(df.shape, aux)


for i in range(len(array)):
    for j in range(len(array)):
        print(array[i,j])

df = pd.DataFrame(array)

df.drop(columns=0, inplace=True)
print(df)
"""
