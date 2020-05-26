import requests


def send_recent_data():
    params = {'city_ibge_code': 3550308, 'is_last': True}
    r = requests.get('https://brasil.io/api/dataset/covid19/caso/data/', params=params)
    dados = r.json()
    dados = dados['results'][0]

    return f'Casos confirmados: {dados["confirmed"]}\n' \
           f'Casos confirmados por 100 mil habitantes: {dados["confirmed_per_100k_inhabitants"]}\n' \
           f'Mortes: {dados["deaths"]}\n' \
           f'Taxa de mortalidade: {dados["death_rate"]}'


send_recent_data()