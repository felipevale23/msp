import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from pint import UnitRegistry
ureg = UnitRegistry()

# i. Leitura dos dados
file=open("line_parameters.txt","r")
line_parameters = file.read()

# Tensão de Linha (kV); Comprimento (km); Impedância (ohm/km); Potência na Carga (kVA)
lineArray = line_parameters.split()
valuesArray = lineArray[1].split(";")

# Declarando as variáveis
V_linha = complex(valuesArray[0])
L = float(valuesArray[1])
Z_linha = complex(valuesArray[2])
Z = Z_linha*L
S_carga = complex(valuesArray[3])

print(V_linha * ureg.Unit("kilovolts"))
print(L * ureg.Unit("km"))
print(Z_linha * ureg.Unit("ohm/km"))
print(S_carga * ureg.Unit("volt ampere"))
file.close()

# ii. Fluxo de Potência

# iii. Tensão na Barra

A = (((1/2)*((np.real(V_linha*1000)**2)+(np.imag(V_linha*1000)**2)))-(np.real(S_carga*1000)*np.real(Z))-(np.imag(S_carga*1000)*np.imag(Z)))
B = ((np.real(S_carga*1000)**2)+(np.imag(S_carga*1000)**2))*((np.real(Z)**2)+(np.imag(Z)**2))

aux0 = (A**2)-B
aux1 = np.sqrt(aux0)
aux2 = A+aux1
V1_linha =  np.sqrt(aux2)

# iv. Perdas

delta_P = (np.real(Z)*((np.real(S_carga*1000)**2)+(np.imag(S_carga*1000)**2)))/((V1_linha)**2)
delta_Q = (np.imag(Z)/np.real(Z))*delta_P
print(V1_linha * ureg.Unit("volt"), delta_P * ureg.Unit("watt"), delta_Q, "var")