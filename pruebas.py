import numpy as np
import pandas as pd
from statistics import mode

l = [1,2,3,4,5,5,5,4]
array = np.array([1,2,3])
array2 = np.array([[1,2,3],[4,5,6],[7,8,9]])
df = pd.DataFrame(array)
a = np.intersect1d(array, array2).tolist()

print(array2.shape)
print(l.count(1))
print(l.count(4))
print(l.count(6))















"""
a.append(1)

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
