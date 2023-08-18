import numpy as np
from cvxopt import matrix, solvers

def calculo_regressao_linear(Usina, mes, num_phis ,total_anos, num_anos, imprime):

  #-----> Função Objetivo

  # Parte linear

  q = matrix(np.zeros(num_anos + num_phis))

  # Parte quadrática

  P = 2*np.eye(num_anos + num_phis)

  for i in range(num_phis):
    P[i][i] = 1e-6

  # print("P:", np.array(P))
  P = matrix(P)
  
  



  def recorte(mes, nome):
    

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



  recorte_Aeq = recorte(mes, 'Aeq')
  matriz_id_1 = np.eye(num_anos)

  Aeq = matrix(np.concatenate((recorte_Aeq, matriz_id_1), axis=1))

  Beq = matrix(recorte(mes, 'Beq'))
  Beq = Beq*1.0


  #-----> Restrições de Canalização ( -inf < phi < inf  e  -inf < erro < inf)

  matriz_id_2 = np.eye(num_anos + num_phis)

  G = matrix(np.concatenate((-1*matriz_id_2, matriz_id_2), axis=0))

  h = list()
  for i in range(num_anos + num_phis):
    h.append(1e10)
    # h.append(np.inf)
  for i in range(num_anos + num_phis):
    h.append(1e10)
    # h.append(np.inf)
  h = matrix(h)

  # Imprime as informações das matrizes

  if imprime == True:
    print('P: ',P)
    print('q: ',q)
    print('G: ',G)
    print('h: ',h)
    print('Aeq: ',Aeq)
    print('Beq: ',Beq)
    print(' ')
    print('Type P: ',type(P))
    print('Type q: ',type(q))
    print('Type G: ',type(G))
    print('Type h: ',type(h))
    print('Type Aeq: ',type(Aeq))
    print('Type Beq: ',type(Beq))
    print(' ')
    print('Tamanho P: ',np.shape(P))
    print('Tamanho q: ',np.shape(q))
    print('Tamanho G: ',np.shape(G))
    print('Tamanho h: ',np.shape(h))
    print('Tamanho Aeq: ',np.shape(Aeq))
    print('Tamanho Beq: ',np.shape(Beq))



  # Resolve o Problema de Otimização Quadrática

  solvers.options['show_progress'] = False

  sol = solvers.qp(P, q, G, h, Aeq, Beq)

  resultados = sol['x']

  return resultados