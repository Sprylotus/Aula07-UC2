import os

os.system('cls')

import pandas as pd
import numpy as np


try:
    print('Obtendo dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    df_roubo_veiculo = df_roubo_veiculo.groupby(['munic']).sum(['roubo_veiculo']).reset_index()
    print(df_roubo_veiculo.head())
    print('\nDados obtidos com sucesso!')

except ImportError as e:
  print(f'Erro ao obter dados: {e}')
  exit()

try:
   print('\nCalculando informações sobre padrão de roubo de veículos...')
   array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
   media_roubo_veiculo = np.mean(array_roubo_veiculo)
   mediana_roubo_veiculo = np.median(array_roubo_veiculo)
   distancia = abs(media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo

   maximo = np.max(array_roubo_veiculo) 
   minimo = np.min(array_roubo_veiculo) 
   amplitude = maximo - minimo 

   q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')
   q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
   q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')
   
   iqr = q3 - q1
   limite_superior = q3 + (1.5 * iqr)
   limite_inferior = q1 - (1.5 * iqr)

   df_roubo_veiculo_outliners_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']< limite_inferior]
   df_roubo_veiculo_outliners_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

   print('Média: ', media_roubo_veiculo)
   print('Mediana: ', mediana_roubo_veiculo)
   print('Distância entre média e mediana', distancia)

   print('\nMEDIDAS DE DISPERSÃO')
   print(30*'-')
   print('Máximo: ', maximo)
   print('Mínimo: ', minimo)
   print('Amplitude total: ', amplitude)

   print('\nMEDIDAS DE POSIÇÃO: ')
   print(30*'-')
   print('Mínimo: ', minimo)
   print(f'Limite inferior: {limite_inferior}') 
   print(f'Q1 (25%): {q1}')
   print(f'Q2 (50%): {q2}')
   print(f'Q3 (75%): {q3}')
   print(f'IQR: {iqr}')
   print(f'Limite superior: {limite_superior}')
   print('Máximo: ', maximo)

   print('\nMUNICÍPIOS COM OUTLINERS INFERIORES: ')
   print(30*'-')
   if len(df_roubo_veiculo_outliners_inferiores) == 0:
      print('Não existem outliners inferiores!')
   else:
      print(df_roubo_veiculo_outliners_inferiores.sort_values(by='roubo_veiculo', ascending=True))

   print('\nMUNICÍPIOS COM OUTLINERS SUPERIORES: ')
   print(30*'-')
   if len(df_roubo_veiculo_outliners_superiores) == 0:
      print('Não existem outliners superiores!')
   else:
      print(df_roubo_veiculo_outliners_superiores.sort_values(by='roubo_veiculo', ascending=False))    

except ImportError as e:
   print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
   exit()