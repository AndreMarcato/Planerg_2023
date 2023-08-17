from funcs import *
from PySDDP.Pen import Newave
import numpy as np
from cvxopt import matrix, solvers
from utils.calculo_regressao_linear import calculo_regressao_linear
from utils.calculo_previsao import calculo_previsao
import matplotlib.pyplot as plt

## Vai instalar o PySDDP caso não esteja instalado
install_pysddp()

## Caminho para o arquivo com as afluencias do Newave
file_path = './NewaveAugust2023/'

PMOAGO2023 = Newave(file_path)
## Seleciionar a usina desejada

Usina = PMOAGO2023.confhd.get('Furnas')
# Total de anos (descartando os 2 anos mais recentes)
total_anos = (np.shape(Usina['vazoes'])[0]) - 2
print("Total de anos: ", total_anos)

# Número de anos considerados (excluindo 1931 e os últimos dois anos - 2022 e 2023)
## 1931 é usado somente para calcular os phis de 1932, não calculamos seu erro
num_anos = total_anos - 1
print("Número de anos considerados: ", num_anos)

# Número de phis considerados (num_meses = num_phis)
num_phis = 5
print("Número de phis considerados: ", num_phis)

# Mês escolhido
meses = {'Jan': 0, 'Fev': 1, 'Mar': 2, 'Abr': 3, 'Mai': 4, 'Jun': 5,
         'Jul': 6, 'Ago': 7, 'Set': 8, 'Out': 9, 'Nov': 10, 'Dez': 11}

mes = meses['Mar']

print("Mês escolhido: ", mes)
resultado = calculo_regressao_linear(Usina, mes, num_phis, total_anos, num_anos, imprime=False)

Z = calculo_previsao(Usina, resultado, mes, num_phis, ano_previsao=2021)










## plotar o grafico de barras com os valores de Z para cada mes
## plotar o grafico de barras com os valores de Z para cada mes e o valor real
## plotar o grafico de barras com os valores de Z para cada mes e o valor real e o erro
