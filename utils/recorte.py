import numpy as np
from cvxopt import matrix


def recorte(mes, nome, Usina, num_phis, total_anos):
  
  if (nome == 'Aeq'):
    if mes - num_phis >= 0:
      recorte =  Usina['vazoes'][1:total_anos, mes-num_phis:mes]
      recorte = recorte[:, ::-1]                               # Para espelhar a matriz e ficar com os dados de trás para frente
      return recorte
    else:
      recorte_ano_atual    =  Usina['vazoes'][1:total_anos, 0:mes]
      recorte_ano_atual = recorte_ano_atual[:, ::-1]           # Para espelhar a matriz e ficar com os dados de trás para frente
      recorte_ano_anterior =  Usina['vazoes'][0:total_anos-1, (mes-num_phis):]
      recorte_ano_anterior = recorte_ano_anterior[:, ::-1]     # Para espelhar a matriz e ficar com os dados de trás para frente
      recorte = matrix(np.concatenate((recorte_ano_atual, recorte_ano_anterior), axis=1))
      return recorte
  if (nome == 'Beq'):
    recorte = Usina['vazoes'][1:total_anos, mes:mes+1]
    return recorte

