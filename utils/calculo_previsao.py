def calculo_previsao(Usina, resultado, mes, num_phis, ano_previsao=2021):
  
    meses = {0: 'Janeiro', 1: 'Fevereiro', 2: 'Março', 3: 'Abril', 4: 'Maio', 5: 'Junho',
              6: 'Julho', 7: 'Agosto', 8: 'Setembro', 9: 'Outubro', 10: 'Novembro', 11: 'Dezembro'}
  
    phis = resultado[0: num_phis]
    #print('Phis: ', phis)
    
    erros = resultado[num_phis:]
    #print('Erros: ', erros)

    Z = 0.
    phis_ano_anterior = abs((mes+1) - num_phis) + 1

    # se ficar no mesmo n
    if ((mes+1) - num_phis >= 0):
        for i in range(num_phis):
            Z += phis[i] * Usina['vazoes'][ano_previsao-1931][mes-i-1]
        Z += erros[ano_previsao-1932]
    else:
        for i in range(num_phis-phis_ano_anterior):
            Z += phis[i] * Usina['vazoes'][ano_previsao-1931][mes-i-1]
        for i in range(phis_ano_anterior):
            Z += phis[phis_ano_anterior-i] * Usina['vazoes'][ano_previsao-1-1931][12-i-1]
        Z += erros[ano_previsao-1932]

    print(f"Previsão calculada para o mês {meses[mes]} do ano de {ano_previsao} ", Z)
    print("Valor Exato extraído do PySDDP:", Usina['vazoes'][2021-1931][mes])

    return Z
