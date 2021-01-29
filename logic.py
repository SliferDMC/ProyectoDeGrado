import pandas as pd
import numpy as np
import xlrd
import json
from statistics import mode

filePath = "C:\\Users\\migue\\OneDrive\\Escritorio\\Proyecto de Grado\\Base_datos_Copia.xls"
openFile = xlrd.open_workbook(filePath)

indexSheets = ["2020_02", "2020_01", "2019_02", "2019_01", "2018_02", "2018_01", "2017_02", "2017_01"]

sheets = []
dfs = []
arrays = []

# Función encargada de convertir un vector de DataFrame a un vector de arreglos de numpy
def convert_DataFrames_to_npArrays(dataFrames):
    npArrays = []
    for i in range(len(dataFrames)):
        npArrays.append(np.array(dataFrames[i]))
    return npArrays

# Función encargada de convertir un vector de arreglos de numpy a un vector de DataFrame
def convert_npArrays_to_DataFrames(npArrays):
    dataFrames = []
    for i in range(len(npArrays)):
        dataFrames.append(pd.DataFrame(npArrays[i]))
    return dataFrames

# Calcula el procentaje de datos que hay en un vector
def calculate_data_porcent_of_vector(vector):
    size = len(vector)
    cont = 0
    for i in range(len(vector)):
        if vector[i] != '-':
            cont +=1
    return (cont*100)/size

# Determina si un vector esta compuesto por números o cadenas. True = números, False = cadenas
def vector_is_number_or_string(array):
    for i in array:
        if is_Number(i):
            return True
    return False

# Determina si un valor es numero o no
def is_Number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Calcula el promedio de un vector
def calculate_average(array):
    avr = 0
    cont = 0
    for i in array:
        if is_Number(i):
            avr += float(i)
            cont += 1
    return avr/cont

# Calcula la moda de un vector ignorando espacios vacios
def calculate_mode(array):
    values = []
    for i in array:
        if i != '-':
            values.append(i)
    return mode(values)

# Completa los espacios vacios con el valor especificado
def complete_void(array, v):
    for i in range(len(array)):
        if array[i] == '-':
            array[i] = v
    return array

# Carga de los datos de la BD y conversion a un vector de DataFrame
for i in range(len(indexSheets)):
    sheets.append(openFile.sheet_by_name(indexSheets[i]))
    dfs.append(pd.DataFrame(sheets[i]))

arrays = convert_DataFrames_to_npArrays(dfs)

#Limpieza de carcteres y fragmentos de texto dentro de cada uno de los campos
for array in arrays:
    for i in range(len(array)):
        for j in range(len(array[0])):
            array[i,j] = str(array[i,j]).replace('text:','').replace('\'','').replace(',','.')

dfs = convert_npArrays_to_DataFrames(arrays)

#Eliminación de características que no son útiles
for df in dfs:
    df.drop(columns=[0,1,2,3,4,5,12,18,19,20,22,57,58], inplace=True)

# Eliminación de columnas que poseen menos del 70% de los datos
for p in range(len(arrays)):
    arrays = convert_DataFrames_to_npArrays(dfs)
    dfs = convert_npArrays_to_DataFrames(arrays)
    for j in range(len(arrays[p][0])):
        porcent = calculate_data_porcent_of_vector(arrays[p][:,j])
        if porcent < 70:
            for df in dfs:
                df.drop(columns=j, inplace=True)

# Eliminación de filas que poseen menos del 70% de los datos
for p in range(len(arrays)):
    arrays = convert_DataFrames_to_npArrays(dfs)
    dfs = convert_npArrays_to_DataFrames(arrays)
    for i in range(len(arrays[p])):
        porcent = calculate_data_porcent_of_vector(arrays[p][i,:])
        if porcent < 70:
            for df in dfs:
                df.drop(index=j, inplace=True)

arrays = convert_DataFrames_to_npArrays(dfs)

# Completar los datos cuantitativos en las celdas faltantes con el promedio de los datos de las columnas respectivas.
# Completar los datos cualitativos en las celdas faltantes con la moda de los datos de las columnas respectivas.
for p in range(len(arrays)):
    for j in range(len(arrays[p][0])):
        if vector_is_number_or_string(arrays[p][:,j]):
            avr = calculate_average(arrays[p][:,j])
            arrays[p][:,j] = complete_void(arrays[p][:,j], avr)
        else:
            m = calculate_mode(arrays[p][:,j])
            arrays[p][:,j] = complete_void(arrays[p][:,j], m)

dfs = convert_npArrays_to_DataFrames(arrays)












"""
cont1 = 0
for array in arrays:
    for j in range(len(array[0])):
        for i in array[:,j]:
            if i == '-':
                cont1 += 1    
print(cont1)

doc = 1
for array in arrays:
    aux = 1
    for i in array[:,6]:
        if i != 'COLOMBIA':
            aux +=1
    print(aux, doc)
    doc += 1
"""