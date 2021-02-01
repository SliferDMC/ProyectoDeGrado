import pandas as pd
import numpy as np
import xlrd
import json
from statistics import mode

filePath = "C:\\Users\\migue\\OneDrive\\Escritorio\\BD\\Base_datos_Copia.xls"
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

# Determina si un valor se encuentra contenido en una lista
def is_content(v, array):
    try:
        array.index(v)
        return True
    except ValueError:
        return False

# Realiza la caracterizacion de los estudiantes: Activos, Ausentes y Desertores
# Parametros: documents: listado de documentos del año analizado
#             labels: registros de caracterización del año anterior
def do_characterization(labels, documents):
    result = [[],[]]
    for i in range(len(labels[0])):
        status = labels[0][i]
        doc = labels[1][i]
        if status == 'ACTIVO' or status == 'NUEVO':
            if is_content(doc, documents):
                result[0].append('ACTIVO')
                result[1].append(doc)
            else:
                result[0].append('AUSENTE')
                result[1].append(doc)
        elif status == 'AUSENTE':
            if is_content(doc, documents):
                result[0].append('ACTIVO')
                result[1].append(doc)
            else:
                result[0].append('DESERTOR')
                result[1].append(doc)
        elif status == 'DESERTOR' or status == 'DESERTOR-A':
            if is_content(doc, documents):
                result[0].append('ACTIVO')
                result[1].append(doc)
            else:
                result[0].append('DESERTOR-A')
                result[1].append(doc)
    for doc in documents:
        if not is_content(doc, labels[1]):
            result[0].append('NUEVO')
            result[1].append(doc)
    return result

#############################################################################

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

# Determinar estudiantes desertores de la universidad con respecto al año
### Año 2017_2
labels_2017_2 = [[],[]]

documents_2017_1 = arrays[7][1:,0]
documents_2017_2 = arrays[6][1:,0]
coincidences1 = np.intersect1d(documents_2017_1, documents_2017_2).tolist()

for doc in documents_2017_2:
    if is_content(doc, coincidences1):
        labels_2017_2[0].append('ACTIVO')
        labels_2017_2[1].append(doc)
    else:
        labels_2017_2[0].append('NUEVO')
        labels_2017_2[1].append(doc)

for doc in documents_2017_1:
    if not is_content(doc, coincidences1):
        labels_2017_2[0].append('AUSENTE')
        labels_2017_2[1].append(doc)

### Año 2018_1
documents_2018_1 = arrays[5][1:,0].tolist()
labels_2018_1 = do_characterization(labels_2017_2, documents_2018_1)

### Año 2018_2
documents_2018_2 = arrays[4][1:,0].tolist()
labels_2018_2 = do_characterization(labels_2018_1, documents_2018_2)

### Año 2019_1
documents_2019_1 = arrays[3][1:,0].tolist()
labels_2019_1 = do_characterization(labels_2018_2, documents_2019_1)

### Año 2019_2
documents_2019_2 = arrays[2][1:,0].tolist()
labels_2019_2 = do_characterization(labels_2019_1, documents_2019_2)

### Año 2020_1
documents_2020_1 = arrays[1][1:,0].tolist()
labels_2020_1 = do_characterization(labels_2019_2, documents_2020_1)

### Año 2020_2
documents_2020_2 = arrays[0][1:,0].tolist()
labels_2020_2 = do_characterization(labels_2020_1, documents_2020_2)


























"""
print('labels_2017_1')
print('Cantidad de estudiantes: ', arrays[7].shape)
print('\n')

print('labels_2017_2')
print('Cantidad de estudiantes: ', arrays[6].shape)
print('ACTIVOS: ', labels_2017_2[0].count('ACTIVO'))
print('AUSENTES: ', labels_2017_2[0].count('AUSENTE'))
print('DESERTORES: ', labels_2017_2[0].count('DESERTOR'))
print('NUEVOS: ', labels_2017_2[0].count('NUEVO'))
print('DESERTORES ANTIGUOS: ', labels_2017_2[0].count('DESERTOR-A'))
print('\n')

print('labels_2018_1')
print('Cantidad de estudiantes: ', arrays[5].shape)
print('ACTIVOS: ', labels_2018_1[0].count('ACTIVO'))
print('AUSENTES: ', labels_2018_1[0].count('AUSENTE'))
print('DESERTORES: ', labels_2018_1[0].count('DESERTOR'))
print('NUEVOS: ', labels_2018_1[0].count('NUEVO'))
print('DESERTORES ANTIGUOS: ', labels_2018_1[0].count('DESERTOR-A'))
print('\n')

print('labels_2018_2')
print('Cantidad de estudiantes: ', arrays[4].shape)
print('ACTIVOS: ', labels_2018_2[0].count('ACTIVO'))
print('AUSENTES: ', labels_2018_2[0].count('AUSENTE'))
print('DESERTORES: ', labels_2018_2[0].count('DESERTOR'))
print('NUEVOS: ', labels_2018_2[0].count('NUEVO'))
print('DESERTORES ANTIGUOS: ', labels_2018_2[0].count('DESERTOR-A'))
print('\n')

print('labels_2019_1')
print('Cantidad de estudiantes: ', arrays[3].shape)
print('ACTIVOS: ', labels_2019_1[0].count('ACTIVO'))
print('AUSENTES: ', labels_2019_1[0].count('AUSENTE'))
print('DESERTORES: ', labels_2019_1[0].count('DESERTOR'))
print('NUEVOS: ', labels_2019_1[0].count('NUEVO'))
print('DESERTORES ANTIGUOS: ', labels_2019_1[0].count('DESERTOR-A'))
print('\n')

print('labels_2019_2')
print('Cantidad de estudiantes: ', arrays[2].shape)
print('ACTIVOS: ', labels_2019_2[0].count('ACTIVO'))
print('AUSENTES: ', labels_2019_2[0].count('AUSENTE'))
print('DESERTORES: ', labels_2019_2[0].count('DESERTOR'))
print('NUEVOS: ', labels_2019_2[0].count('NUEVO'))
print('DESERTORES ANTIGUOS: ', labels_2019_2[0].count('DESERTOR-A'))
print('\n')

print('labels_2020_1')
print('Cantidad de estudiantes: ', arrays[1].shape)
print('ACTIVOS: ', labels_2020_1[0].count('ACTIVO'))
print('AUSENTES: ', labels_2020_1[0].count('AUSENTE'))
print('DESERTORES: ', labels_2020_1[0].count('DESERTOR'))
print('NUEVOS: ', labels_2020_1[0].count('NUEVO'))
print('DESERTORES ANTIGUOS: ', labels_2020_1[0].count('DESERTOR-A'))
print('\n')

print('labels_2020_2')
print('Cantidad de estudiantes: ', arrays[0].shape)
print('ACTIVOS: ', labels_2020_2[0].count('ACTIVO'))
print('AUSENTES: ', labels_2020_2[0].count('AUSENTE'))
print('DESERTORES: ', labels_2020_2[0].count('DESERTOR'))
print('NUEVOS: ', labels_2020_2[0].count('NUEVO'))
print('DESERTORES ANTIGUOS: ', labels_2020_2[0].count('DESERTOR-A'))
print('\n')










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