import numpy as np
import pandas as pd
from statistics import mode
from matplotlib import pyplot as plt

l = [1,2,3,4,5,5,5,4]
array = np.array([1,2,3])
array2 = np.array([[1.2345,2,3],[4,5,6],[7,8,9],['hola','pedrin', 'como']])
df = pd.DataFrame(array)


np.savetxt('../matriz.txt', array2, fmt='%s')
"""
p = np.loadtxt('matriz.txt', skiprows=0, dtype=str)

print(array2)
print(p)
"""







"""
x = [1,2,3,4,5]
y = [6,7,8,9,10.11]

plt.plot(x, y, 'ro')
plt.xlabel('eje x')
plt.ylabel('eje y')
plt.show()
"""









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
