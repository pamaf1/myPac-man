import pandas as pd
import numpy as np


data = pd.read_csv("result.csv")
# data2 = np.genfromtxt("data.csv",delimiter=',')

# arrayOfRepetitions = np.unique(data['score'], return_counts = True)

# x = [] 
# for i in arrayOfRepetitions[0]:
#     x.append(int(i))

# n = [] 
# for i in arrayOfRepetitions[1]:
#     n.append(i)

# print(x)
# print(n)

# arra = 0
# for item in range(len(x)):
#     arra += n[item]*x[item]
#     #(x[item] - xv)**2 #(N[item] * (x[item]  2)) - xv ** 2

# Mat = arra / len(data['score'])
# print('Мат ожидание:', Mat)

xv = sum(data['time'])/len(data['time'])
print('Вибіркове середнє: ',xv)

# arra1 = 0
# for item in range(len(x)):
#     arra1 += n[item]*((x[item]-xv))**2
#     #(x[item] - xv)**2 #(N[item] * (x[item]  2)) - xv ** 2

# D = arra1 / len(data['score'])
# print('Дисперсія:',D)