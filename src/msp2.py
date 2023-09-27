import numpy as np
import pandas as pd
import time
import math
import matplotlib.pyplot as plot
from pint import UnitRegistry
ureg = UnitRegistry()

t = time.process_time()

# i. Leitura dos dados
file = open("line_parameters2.txt","r")
line_parameters = file.read()
file.close()

# Tensão de Linha (kV); Comprimento (km); Impedância (ohm/km); Potência na Carga (kVA)
lineArray = line_parameters.split()
lineSize = len(lineArray)

# Preenchendo as variáveis
V = np.zeros(((lineSize),10))
Z = np.zeros(((lineSize)),dtype=np.clongdouble)
S = np.zeros(((lineSize)),dtype=np.clongdouble)
P = np.zeros(((lineSize)))
Q = np.zeros(((lineSize)))
L = np.zeros(((lineSize)))
A = np.zeros(((lineSize),10))
B = np.zeros(((lineSize),10))
delta_P = np.zeros(((lineSize),10))
delta_Q = np.zeros(((lineSize),10))

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

for z in reversed(range(lineSize)):
    print(z,"-",(z+1),(S[z]/1000).round(decimals=4),(P[z]/1000).round(decimals=4),(Q[z]/1000).round(decimals=4))

# Forward

i = 0
j = 0
erro = 1

print("\n","Forward:")
print("\n","Barra:",j,"-",(j+1))
print("\nV",j,":",V[j][i].round(decimals=4))
print("P E Q:",np.real(P[j]/1000).round(decimals=4),"kW", np.real(Q[j]/1000).round(decimals=4),"kvar")
print("Delta_P",i,":", delta_P[j][i].round(decimals=4), "\nDelta_Q",i,":",delta_Q[j][i].round(decimals=4))

while erro >= 1:

    # print("\n",(i+1),"Interação:\n")

    # iii. Tensão na Barra

    P[j] = P[j] + delta_P[j][i]
    Q[j] = Q[j] + delta_Q[j][i]

    # print("P E Q:",np.real(P[j]/1000).round(decimals=4),"kW", np.real(Q[j]/1000).round(decimals=4),"kvar")

    A[j][i] = (((1/2)*(V[j][0]**2))-(np.real(P[j])*np.real(Z[j]))-(np.real(Q[j])*np.imag(Z[j])))
    B[j][i] = ((np.real(P[j])**2)+(np.real(Q[j])**2))*((np.real(Z[j])**2)+(np.imag(Z[j])**2))

    aux0 = (A[j][i]**2)-B[j][i]
    aux1 = np.sqrt(abs(aux0))
    aux2 = A[j][i]+aux1
    V[j][i+1] = np.sqrt(abs(aux2))

    # iv. Perdas
    delta_P[j][i+1] = np.real((np.real(Z[j])*((np.real(P[j])**2)+(np.real(Q[j])**2)))/((V[j][i+1])**2))
    delta_Q[j][i+1] = np.real((np.imag(Z[j])/np.real(Z[j]))*delta_P[j][i+1])
    erro = np.sqrt((delta_P[j][i+1] - delta_P[j][i])**2)

    # print("Tensão V",i+1,":",np.real(V[j][i+1]).round(decimals=4) * ureg.Unit("volt"),"\nDelta_P",i+1,":", delta_P[j][i+1].round(decimals=4) * ureg.Unit("watt"), "\nDelta_Q",i+1,":",delta_Q[j][i+1].round(decimals=4), "var","\nErro:",np.real(erro).round(decimals=4))

    if erro > 1:
        if i == 8:
            j += 1
            V[j][0] = V[j-1][i+1]
            delta_P[j][0] = delta_P[j-1][i+1]
            delta_Q[j][0] = delta_Q[j-1][i+1]
            i = 0
        i += 1
    elif erro < 1:  
        if j == (lineSize-1): break
        j += 1
        V[j][0] = V[j-1][i+1]
        delta_P[j][0] = delta_P[j-1][i+1]
        delta_Q[j][0] = delta_Q[j-1][i+1]
        print("\n",(i+1),"Interação:\n")
        print("P E Q:",np.real(P[j-1]/1000).round(decimals=4),"kW", np.real(Q[j-1]/1000).round(decimals=4),"kvar")
        print("Tensão V",i+1,":",np.real(V[j-1][i+1]).round(decimals=4) * ureg.Unit("volt"),"\nDelta_P",i+1,":", delta_P[j-1][i+1].round(decimals=4) * ureg.Unit("watt"), "\nDelta_Q",i+1,":",delta_Q[j-1][i+1].round(decimals=4), "var","\nErro:",np.real(erro).round(decimals=4))
        erro = 1
        i = 0
        print("\n","Barra:",j,"-",(j+1))
        print("V",j,":",V[j][0].round(decimals=4))
        print("P E Q:",np.real(P[j]/1000).round(decimals=4),"kW", np.real(Q[j]/1000).round(decimals=4),"kvar")

# backward

delta_P = np.zeros((lineSize,10))
delta_Q = np.zeros((lineSize,10))
i = 0
j = lineSize - 1
erro = 1

print("\nTensões em todas as Barras\n")

for x in range(lineSize):
    print(x,"-",(x+1), V[x][0].round(decimals=4))


print("\n","Backward:")
print("\n","Barra:",j,"-",(j+1))
print("P E Q:",(P/1000).round(decimals=4),"kW", (Q/1000).round(decimals=4),"kvar")
print("Delta_P",i,":", delta_P[j][i].round(decimals=4), "\nDelta_Q",i,":",delta_Q[j][i].round(decimals=4))

while erro >= 1:

    # print("\n",(i+1),"Interação:\n")

    # iii. Tensão na Barra

    P[j] = P[j] + delta_P[j][i]
    Q[j] = Q[j] + delta_Q[j][i]

    # print("P E Q:",np.real(P[j]/1000).round(decimals=4),"kW", np.real(Q[j]/1000).round(decimals=4),"kvar")

    A[j][i] = (((1/2)*(V[j][0]**2))-(np.real(P[j])*np.real(Z[j]))-(np.real(Q[j])*np.imag(Z[j])))
    B[j][i] = ((np.real(P[j])**2)+(np.real(Q[j])**2))*((np.real(Z[j])**2)+(np.imag(Z[j])**2))

    aux0 = (A[j][i]**2)-B[j][i]

    aux1 = np.sqrt(abs(aux0))
    
    aux2 = A[j][i]+aux1

    V[j][i+1] = np.sqrt(abs(aux2))

    # iv. Perdas
    delta_P[j][i+1] = np.real((np.real(Z[j])*((np.real(P[j])**2)+(np.real(Q[j])**2)))/((V[j][i+1])**2))
    delta_Q[j][i+1] = np.real((np.imag(Z[j])/np.real(Z[j]))*delta_P[j][i+1])
    erro = np.sqrt((delta_P[j][i+1] - delta_P[j][i])**2)

    # print("Tensão V",i+1,":",np.real(V[j][i+1]).round(decimals=4) * ureg.Unit("volt"),"\nDelta_P",i+1,":", delta_P[j][i+1].round(decimals=4) * ureg.Unit("watt"), "\nDelta_Q",i+1,":",delta_Q[j][i+1].round(decimals=4), "var","\nErro:",np.real(erro).round(decimals=4))

    if erro > 1:
        if i == 8:
            j += 1
            V[j][0] = V[j-1][i+1]
            delta_P[j][0] = delta_P[j-1][i+1]
            delta_Q[j][0] = delta_Q[j-1][i+1]
            i = 0
        i += 1
    elif erro < 1:    
        if j == 0: break
        j -= 1
        V[j][0] = V[j-1][i+1]
        delta_P[j][0] = delta_P[j-1][i+1]
        delta_Q[j][0] = delta_Q[j-1][i+1]
        print("\n",(i+1),"Interação:\n")
        print("P E Q:",np.real(P[j+1]/1000).round(decimals=4),"kW", np.real(Q[j+1]/1000).round(decimals=4),"kvar")
        print("Tensão V",i+1,":",np.real(V[j+1][i+1]).round(decimals=4) * ureg.Unit("volt"),"\nDelta_P",i+1,":", delta_P[j+1][i+1].round(decimals=4) * ureg.Unit("watt"), "\nDelta_Q",i+1,":",delta_Q[j+1][i+1].round(decimals=4), "var","\nErro:",np.real(erro).round(decimals=4))
        i = 0
        erro = 1
        print("\n","Barra:",j,"-",(j+1))
        print("V",j,":",V[j][0].round(decimals=4))
        print("P E Q:",np.real(P[j]/1000).round(decimals=4),"kW", np.real(Q[j]/1000).round(decimals=4),"kvar")

print("\n-----------------------------------------------")

print("\nResultados:")

print("\nTensões em todas as Barras")
for x in range(lineSize):
    print(x,"-",(x+1), V[x][0].round(decimals=4))

print("\nCargas em todas as Barras")
print("P E Q:",(P/1000).round(decimals=4),"kW", (Q/1000).round(decimals=4),"kvar")

elapsed_time = time.process_time() - t

print("\nTempo de Execução: ",math.trunc(elapsed_time * 1000), "ms")

