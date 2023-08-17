import numpy as np
from cvxopt import matrix


def recorte(Usina, mes, nome, num_phis, total_anos):
  num_mes = mes - 1

  if (nome == 'Aeq'):
    if num_mes - num_phis >= 0:
      recorte = Usina['vazoes'][1:total_anos, num_mes-num_phis:num_mes]
      # Para espelhar a matriz e ficar com os dados de trás para frente
      recorte = recorte[:, ::-1]
      return recorte
    else:
      recorte_ano_atual = Usina['vazoes'][1:total_anos, 0:num_mes]
      # Para espelhar a matriz e ficar com os dados de trás para frente
      recorte_ano_atual = recorte_ano_atual[:, ::-1]

      recorte_ano_anterior = Usina['vazoes'][0:total_anos -
                                             1, (num_mes-num_phis):]
      # Para espelhar a matriz e ficar com os dados de trás para frente
      recorte_ano_anterior = recorte_ano_anterior[:, ::-1]

      recorte = matrix(np.concatenate(
          (recorte_ano_atual, recorte_ano_anterior), axis=1))
      return recorte

  if (nome == 'Beq'):
    recorte = Usina['vazoes'][1:total_anos, num_mes:num_mes+1]
    return recorte
