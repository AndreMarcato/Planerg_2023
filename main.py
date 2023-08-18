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
# num_phis = 11
# print("Número de phis considerados: ", num_phis)

ano_previsao=2010

# Mês escolhido
meses = {'Jan': 0, 'Fev': 1, 'Mar': 2, 'Abr': 3, 'Mai': 4, 'Jun': 5,
         'Jul': 6, 'Ago': 7, 'Set': 8, 'Out': 9, 'Nov': 10, 'Dez': 11}

mes = meses['Mai']

z_values = []
real_values = []





anos_previsao = [2001, 2005, 2010, 2015, 2020, 2021,2022,2023]
phis_values = [1, 3, 5, 7, 9, 11]

for ano_previsao in anos_previsao:
    real_values = []
    
    # Calculando os valores reais uma vez, já que eles são constantes
    for mes_name, mes_value in meses.items():
        real_value = Usina['vazoes'][ano_previsao-1931][mes_value]
        real_values.append(real_value)

    # Criando a figura
    plt.figure(figsize=(10, 5))

    # Plotando os valores reais
    plt.plot(meses.keys(), real_values, alpha=1, label='Real', marker='o', linewidth=1.3)

    # Loop para variar o número de phis e calcular as previsões
    for phi in phis_values:
        z_values = []
        for mes_name, mes_value in meses.items():
            resultado = calculo_regressao_linear(Usina, mes_value, phi, total_anos, num_anos, imprime=False)
            Z = calculo_previsao(Usina, resultado, mes_value, phi, ano_previsao)
            z_values.append(Z)

        plt.plot(meses.keys(), z_values, alpha=1, label=f'Previsão (phis={phi})', marker='o', linestyle='dashed', linewidth=1.2)

    plt.title(f'Valores da Previsão e Valores Reais para Cada Mês - Ano {ano_previsao}')
    plt.xlabel('Mês')
    plt.ylabel('Valor')
    plt.grid()
    plt.legend()
plt.show()


