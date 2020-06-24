import requests
from datetime import date, datetime, timedelta


def time_format(data):
    brazil_tz = timedelta(hours=3)
    data = data.split('.')[0]
    format_data = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    format_data = format_data - brazil_tz

    return format_data


def format_city_name(city):
    city = city.split(' ')
    for pos, item in enumerate(city):
        if item in 'DasDesDisDosDus':
            city[pos] = item.lower()
    return ' '.join(city)


# lista casos no Brasil em data específica
def brazil_recent_cases(to_string=True):
    url = 'https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeralApi'
    r = requests.get(url)
    if r.ok:
        dados = r.json()
        data = dados['dt_updated']
        data = time_format(data)
        confirmados = dados['confirmados']
        obitos = dados['obitos']
        if to_string:
            msg = f'\U00002705 <b>Casos confirmados:</b> {confirmados["total"]}\n' \
                  f'\U00002620 <b>Mortes:</b> {obitos["total"]} ({obitos["novos"]} em 24h)\n' \
                  f'\U0001F504 <b>Recuperados:</b> {confirmados["recuperados"]}\n' \
                  f'\U0001F50D <b>Em acompanhamento:</b> {confirmados["acompanhamento"]}\n' \
                  f'<em>Atualizado em {data.day:0>2}/{data.month:0>2} às {data.time()}</em>'
            return msg
        return dados
    else:
        return None


# lista casos por estado brasileiro
def state_recent_cases(uf, to_string=True):
    uf = uf.lower()
    r = requests.get('https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/' + uf)
    if r.ok:
        dados = r.json()
        if to_string:
            data = dados['datetime']
            data = time_format(data)
            msg = f'\U0001F6A8 <b>Dados recentes de Covid-19 | {dados["state"]} ({dados["uf"]})</b>\n\n' \
                  f'\U00002705 <b>Casos confirmados:</b> {dados["cases"]}\n' \
                  f'\U00002620 <b>Mortes:</b> {dados["deaths"]}\n' \
                  f'<em>Atualizado em {data.day}/{data.month:0>2} às {data.time()}</em>'
            return msg
        return dados

    return None


# lista casos por todos os estados brasileiros
def all_states_cases():
    r = requests.get('https://covid19-brazil-api.now.sh/api/report/v1')
    if r.ok:
        dados = r.json()
        dados = dados['data']
        return dados

    return None


# lista das cidades (API: IBGE)
def cidadesbr():
    r = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios/?orderBy=nome')
    if r.ok:
        return [(item['nome'].upper(), item['microrregiao']['mesorregiao']['UF']['sigla']) for item in r.json()]


# lista casos por cidade (API: brasil.io)
def city_recent_cases(city, state=None, to_string=True):
    city = format_city_name(city.title())
    params = {'city': city, 'state': state, 'is_last': True}
    r = requests.get('https://brasil.io/api/dataset/covid19/caso_full/data/?format=json', params=params)
    if r.ok:
        dados = r.json()
        if to_string:
            try:
                dados = dados['results'][0]
            except IndexError:
                return 'Houve um erro. Tente novamente'
            data = dados['date'].split('-')
            data = f'{data[2]}/{data[1]}'
            msg = f'\U0001F6A8 <b>Dados recentes de Covid-19 | {dados["state"]} ({dados["city"]})</b>\n\n'\
                f'\U00002705 <b>Casos confirmados:</b> {dados["last_available_confirmed"]}'\
                f' ({dados["new_confirmed"]} em 24h)\n'\
                f'\U00002620 <b>Mortes:</b> {dados["last_available_deaths"]} ({dados["new_deaths"]} em 24h)\n'\
                f'<em>Atualizado em {data}</em>'
            return msg
        return dados

    return None


# lista casos por país
def country_cases(pais='brazil'):
    r = requests.get('https://covid19-brazil-api.now.sh/api/report/v1/', params=pais)
    if r.ok:
        dados = r.json()
        dados = dados['data']
        return dados

    return None


# lista casos por todos os países
def all_countries_cases():
    r = requests.get('https://covid19-brazil-api.now.sh/api/report/v1/countries')
    if r.ok:
        dados = r.json()
        dados = dados['data']
        return dados

    return None


if __name__ == '__main__':
    print(brazil_recent_cases())
