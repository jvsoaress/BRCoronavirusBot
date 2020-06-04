import requests
from datetime import date, datetime, timedelta


def time_format(data):
    brazil_tz = timedelta(hours=3)
    data = data.split('.')[0]
    format_data = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    format_data = format_data - brazil_tz

    return format_data

def date_format(data):
    data = data.split('-')
    return f"{data[2]}/{data[1]}/{data[0]}"


# lista casos no Brasil em data específica
def brazil_recent_cases(to_string=True):
    hoje = str(date.today())
    hoje = hoje.split('-')
    hoje = ''.join(hoje)
    r = requests.get('https://covid19-brazil-api.now.sh/api/report/v1/brazil/', params=hoje)
    if r.ok:
        dados = r.json()
        dados = dados['data']
        if to_string:
            data = dados['updated_at']
            data = time_format(data)
            msg = f'\U00002705 <b>Casos confirmados:</b> {dados["confirmed"]}\n' \
                  f'\U00002620 <b>Mortes:</b> {dados["deaths"]}\n' \
                  f'\U0001F504 <b>Recuperados:</b> {dados["recovered"]}\n' \
                  f'<em>Atualizado em {data.day}/{data.month:0>2} às {data.time()}</em>'
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

# lista das cidades:
def cidadesbr():
    r = requests.get('https://brasil.io/api/dataset/covid19/caso_full/data/?format=json')
    if r.ok:
        return [item['city'] for item in r.json()['results']]

# lista casos por cidade (API: brasil.io)
def city_recent_cases(city, to_string=True):
    # uf = uf.lower()
    r = requests.get('https://brasil.io/api/dataset/covid19/caso_full/data/?format=json')
    if r.ok:
        dados = r.json()
        if to_string:
            dados = dados["results"]
            data = []
            for item in dados:
                if item['city'] == city:
                    dados = item
                    data = item['date']
                    data = date_format(data)
            msg = f'\U0001F6A8 <b>Dados recentes de Covid-19 | {dados["state"]} ({dados["city"]})</b>\n\n' \
                  f'\U00002705 <b>Casos confirmados:</b> {dados["last_available_confirmed"]}\n' \
                  f'\U00002620 <b>Mortes:</b> {dados["last_available_deaths"]}\n' \
                  f'<em>{data}</em>'
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
    print(state_recent_cases('SP'))
