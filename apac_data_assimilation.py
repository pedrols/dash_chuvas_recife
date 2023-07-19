# %%
import pandas as pd
import numpy as np
import os
import seaborn as sns

# %%

# Dicionário de conversão de meses
meses_siglas = {m:str(n+1) for n, m in enumerate(
    ['jan', 'fev', 'mar', 'abr', 'mai', 'jun',
    'jul', 'ago', 'set', 'out', 'nov', 'dez'])}

# Testar validade de datas
def valid_dates(date_string):
    try:
        return pd.to_datetime(date_string, format='%d/%m/%Y')
    except ValueError:
        return np.nan

# Converter números com vírgula para float
converter_numeros = lambda c: np.nan if c == '-' else float(c.replace(',','.'))

# Função pra ler e converter dados para séries temporais
def processar_dados(fname):

    # ler arquivo
    df = pd.read_csv(fname, encoding='latin-1')

    # converte rótulos de colunas de texto em número
    df.columns = [int(el) if el.isdigit() else el for el in df.columns]

    # converter valores para float
    df.loc[:,1:31] = df.loc[:,1:31].applymap(converter_numeros)

    # vetorizar dataframe (nomes de colunas para colunas)
    df_melted = df[['Posto', 'Mês/Ano', *list(range(1,31))]].\
        melt(id_vars=['Posto', 'Mês/Ano'], var_name='Dia', value_name='Valor')

    # trocar siglas de mes por número
    mes_ano = df_melted['Mês/Ano'].replace(meses_siglas, regex=True)

    # concatenar str de datas
    datas = df_melted['Dia'].astype(str) + '/' + mes_ano

    # converter pra timestamps e identificar datas inválidas
    df_melted['Data'] = datas.apply(valid_dates)

    # dropando datas inválidas
    df_melted = df_melted[['Data', 'Posto', 'Valor']].dropna(subset=['Data'])

    # pivotando nome dos postos para colunas
    return df_melted.pivot_table(index= 'Data', columns='Posto', values='Valor') 

# %%

fnames = ['apac/'+f for f in os.listdir('apac')]

processar_dados(fnames[6])

# %%

dfres = pd.DataFrame()
for file in fnames:
    dfl = processar_dados(file)
    dfres = pd.concat([dfres, dfl], axis=0)

# %%

dfres.to_csv('apac_pluvio.csv')
# %%

dft = pd.read_csv('apac_pluvio.csv', parse_dates=['Data']).set_index('Data')

dft

# %%

dft.T

# %%

sns.heatmap(dft.T)
# %%
