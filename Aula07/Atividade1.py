import os

os.system('cls')

import pandas as pd
import numpy as np


try:
   print('Obtendo dados...')
   ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
   df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
   df_estelionato = df_ocorrencias[['estelionato', 'mes_ano']]
   df_estelionato = df_estelionato.groupby(['mes_ano']).sum(['estelionato']).reset_index()
   print(df_estelionato.head())
   print('\nDados obtidos com sucesso!')

except ImportError as e:
  print(f'Erro ao obter dados: {e}')
  exit()

try:
   df_estelionato_mes_ano = df_estelionato.groupby(['mes_ano']).sum().reset_index()
   print(df_estelionato)
   array_estelionato = np.array(df_estelionato_mes_ano['estelionato'])
   print('\nCalculando informações sobre padrão de estelionatos...')
   media_estelionato = (np.mean(array_estelionato))
   mediana_estelionato = (np.median(array_estelionato))
   distancia = abs(media_estelionato - mediana_estelionato) / mediana_estelionato * 100
   
   q1 = np.quantile(array_estelionato, 0.25, method='weibull')
   q2 = np.quantile(array_estelionato, 0.50, method='weibull')
   q3 = np.quantile(array_estelionato, 0.75, method='weibull')

   df_mes_ano_acima_q3 = df_estelionato_mes_ano[df_estelionato_mes_ano['estelionato'] > q3]
   df_mes_ano_abaixo_q1 = df_estelionato_mes_ano[df_estelionato_mes_ano['estelionato'] < q1]

   print('\nMEDIDAS DE TENDÊNCIA CENTRAL: ')
   print(30*'-') 
   print(f'A média dos estelionatos registrados são de {media_estelionato:.2f}')
   print(f'A mediana dos estelionatos registrados são de {mediana_estelionato:.2f}')
   print(f'Índice de verificação de tendência central: {distancia:.2f}%')
   
   print('\nMEDIDAS DE POSIÇÃO: ')
   print(30*'-') 
   print('Q1 (25%): ', q1)
   print('Q2 (50%): ', q2)
   print('Q3 (75%): ', q3)

   print('\nMAIORES MESES E ANOS: ')
   print(30*'-')
   print(df_mes_ano_acima_q3.sort_values(by='estelionato', ascending=False))

   print('\nMENORES MESES E ANOS: ')
   print(30*'-')
   print(df_mes_ano_abaixo_q1.sort_values(by='estelionato')) 

   print('\nCONCLUSÃO: ') 
   print('Baseando-se nos dados apresentados, é correto afirmar que há uma assimetria considerável, tendo em vista o padrão instável de ocorrências de estelionato ao longo do tempo')
except ImportError as e:
   print(f'Erro ao obter informações sobre padrão de estelionatos: {e}')
   exit()