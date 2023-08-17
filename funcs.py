from cvxopt import matrix, solvers
import numpy as np

# Function to install PySDDP library if needed
def install_pysddp():
    """
    Installs the PySDDP library.
    """
    # The following command is specific to Colab environment and may not be needed in other environments
    try:
        import PySDDP
        print("PySDDP is already installed.")
    except ImportError:
        # Uncomment the next line if you want to install PySDDP in your environment
        # !pip install PySDDP
        print("PySDDP has been installed.")

# Function to configure paths and read data
def configure_paths_and_read_data(file_path):
    """
    Configures the paths and reads the data from the specified file path.

    :param file_path: Path to the Newave data file
    :return: PMO object containing the data
    """
    import os
    from PySDDP.Pen import Newave

    # Check if the file path exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file path '{file_path}' does not exist.")

    # Create a Newave object
    PMO = Newave(file_path)

    return PMO

# Function to visualize data of the specified plant
def visualize_plant_data(PMO, plant_name):
    """
    Visualizes the data of the specified plant.

    :param PMO: PMO object containing the data
    :param plant_name: Name of the target plant
    :return: None
    """
    # Get the plant data
    plant_data = PMO.confhd.get(plant_name)

    # Print keys and vazoes of the plant
    print(plant_data.keys())
    import numpy as np
    print(plant_data['vazoes'])
    print(np.shape(plant_data['vazoes']))

    # Plot the vazoes of the plant
    PMO.confhd.plot_vaz(plant_data)
    return plant_data

def optimize_autoregressive_model(Usina, mes_alvo, ordem_modelo, plant_name, imprime=False):
    """
    Optimizes the autoregressive model for the specified plant and parameters.

    :param Usina: Usina object containing the data
    :param mes_alvo: Target month (e.g., 8 for August)
    :param ordem_modelo: Order of the model (e.g., 3 for 3 previous months)
    :param plant_name: Name of the target plant
    :param imprime: Whether to print debugging information (default: False)
    :return: Optimization results
    """
    PMO = Usina.confhd.get(plant_name)
    total_anos = PMO['vazoes'].shape[0] - 1 # Assuming the shape corresponds to the total number of years

    # Call the optimization function
    resultados = calculo_regressao_linear(PMO, mes_alvo, ordem_modelo, total_anos, imprime)

    return resultados
    
def recorte(Usina, mes, num_phis, total_anos, nome):
  num_mes = mes - 1
  if (nome == 'Aeq'):
    if num_mes - num_phis >= 0:
      recorte =  Usina['vazoes'][1:total_anos, num_mes-num_phis:num_mes]
      recorte = recorte[:, ::-1]                               # Para espelhar a matriz e ficar com os dados de trás para frente
      return recorte
    else:
      recorte_ano_atual    =  Usina['vazoes'][1:total_anos, 0:num_mes]
      recorte_ano_atual = recorte_ano_atual[:, ::-1]           # Para espelhar a matriz e ficar com os dados de trás para frente
      recorte_ano_anterior =  Usina['vazoes'][0:total_anos-1, (num_mes-num_phis):]
      recorte_ano_anterior = recorte_ano_anterior[:, ::-1]     # Para espelhar a matriz e ficar com os dados de trás para frente
      recorte = matrix(np.concatenate((recorte_ano_atual, recorte_ano_anterior), axis=1))
      return recorte
  if (nome == 'Beq'):
    recorte = Usina['vazoes'][1:total_anos, num_mes:num_mes+1]
    return recorte

def calculo_regressao_linear(Usina, mes, num_phis, num_anos, imprime=False):
  #-----> Função Objetivo
  # Parte linear

  q = matrix(np.zeros(num_anos + num_phis))

  # Parte quadrática

  P = 2*np.eye(num_anos + num_phis)

  for i in range(num_phis):
    P[i][i] = 0


  P = matrix(P)

    # Use recorte function
  recorte_Aeq = recorte(Usina, mes, num_phis, num_anos, 'Aeq')
    
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

