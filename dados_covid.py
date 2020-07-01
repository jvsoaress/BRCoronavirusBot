import json
import requests
import pandas as pd


def get_file_url():
    headers = {'x-parse-application-id': 'unAFkcaNDeXajurGB7LChj8SgQYS2ptm'}
    url = 'https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral'

    r = requests.get(url, headers=headers)
    dados = r.json()['results'][0]
    arquivo_url = dados['arquivo']['url']

    print('URL encontrada, baixando arquivo...')
    return arquivo_url


def download_file():
    arquivo_url = get_file_url()
    arquivo = requests.get(arquivo_url)
    with open('HIST_PAINEL_COVIDBR.xlsx', 'wb') as f:
        f.write(arquivo.content)
    print('Arquivo baixado.')


def read_data():
    download_file()
    df = pd.read_excel('HIST_PAINEL_COVIDBR.xlsx')
    df = df[['data', 'regiao', 'casosAcumulado',
             'casosNovos', 'obitosAcumulado', 'obitosNovos']]
    brasil_df = df[df['regiao'] == 'Brasil'].set_index('data')
    print('Dados lidos com sucesso!')
    return brasil_df


def update_graphs_from_json(graphs_metadata):
    with open('graphs.json', 'w') as f:
        json.dump(graphs_metadata, f, ensure_ascii=False)
    print('Arquivo JSON atualizado com sucesso!')


def get_graphs_from_json():
    with open('graphs.json', 'r') as f:
        graphs_metadata = json.load(f)
        return graphs_metadata


if __name__ == '__main__':
    pass
