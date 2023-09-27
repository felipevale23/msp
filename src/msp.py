import numpy as np
import pandas as pd
import time
import math
import matplotlib.pyplot as plot
from pint import UnitRegistry
ureg = UnitRegistry()

t = time.process_time()

# i. Leitura dos dados
file=open("line_parameters.txt","r")
line_parameters = file.read()

# Tensão de Linha (kV); Comprimento (km); Impedância (ohm/km); Potência na Carga (kVA)
lineArray = line_parameters.split()
lineSize = len(lineArray)

# Preenchendo as variáveis
V = np.zeros(((lineSize+1),10))
Z = np.zeros(((lineSize+1)),dtype=np.clongdouble)
S = np.zeros(((lineSize+1)),dtype=np.clongdouble)
R = np.zeros(((lineSize+1)))
X = np.zeros(((lineSize+1)))
P = np.zeros(((lineSize+1)))
Q = np.zeros(((lineSize+1)))
L = np.zeros(((lineSize+1)))
A = np.zeros(((lineSize+1),10), dtype=np.longdouble)
B = np.zeros(((lineSize+1),10), dtype=np.longdouble)
delta_P = np.zeros(((lineSize+1),10))
delta_Q = np.zeros(((lineSize+1),10))
erro = np.zeros((lineSize))
attempt = 0


# ii. Fluxo de Potência

V_linha = 13.8 * 1000
V[0][0] = V_linha

for x in reversed(range(lineSize)):
    valuesArray = lineArray[x].split(";")
    L[x] = valuesArray[1]
    Z[x] = complex(valuesArray[2]) * L[x]
    S[x] = complex(valuesArray[3]) * 1000
    for y in range(lineSize):
        P[x] += np.real(S[y])
        Q[x] += np.imag(S[y])
        R[x] += np.real(Z[y]) 
        X[x] += np.imag(Z[y])

for z in reversed(range(lineSize)):
    print(z,"-",(z+1),(S[z]/1000).round(decimals=4),"P:",(P[z]/1000).round(decimals=4),"Q:",(Q[z]/1000).round(decimals=4),"R:",(R[z]).round(decimals=4),"X:",(X[z]).round(decimals=4))

# Forward

i = 0
j = 0
delta_P[0][0] = 0
delta_Q[0][0] = 0

while j < (lineSize) :

    print("\n","Determinando as Tensões na Barra:")

    print("\n","Barra:",j,"-",(j+1))
    print("\nV",j,":",V[j][i].round(decimals=4))

    while i < 10 :
        
        A[j][i] = (((0.5)*(V[j][0]**2))-((P[j] + delta_P[j][i])*(R[j]))-((Q[j] + delta_Q[j][i])*(X[j])))
        B[j][i] = (((P[j])**2)+((Q[j])**2))*(((R[j])**2)+((X[j])**2))
        
        aux0 = (A[j][i]**2)-B[j][i]
        aux1 = np.sqrt(aux0)
        aux2 = A[j][i]+aux1
        V[j+1][i] = np.sqrt(aux2)  

        delta_P[j][i+1] = R[j]*(((P[j]**2)+(Q[j]**2))/(V[j+1][i]**2))
        delta_Q[j][i+1] = (X[j]/R[j])*delta_P[j][i+1] 

        erro[j] = abs(delta_P[j][i+1] - delta_P[j][i])

        if erro[j] < 1:
            print("\nInteração: ",attempt,"\nerro:", erro[j])
            i = 10
            
        else :
            i += 1
            attempt += 1

    i = 0
    j += 1


elapsed_time = time.process_time() - t

print("\nTempo de Execução: ",math.trunc(elapsed_time * 1000), "ms")
