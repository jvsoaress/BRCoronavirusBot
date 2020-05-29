import requests
from datetime import date, datetime, timedelta


def time_format(data):
    brazil_tz = timedelta(hours=3)
    data = data.split('.')[0]
    format_data = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    format_data = format_data - brazil_tz

    return format_data


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


# lista casos por todos os estados brasileiros
def all_states_cases():
    r = requests.get('https://covid19-brazil-api.now.sh/api/report/v1')
    if r.ok:
        dados = r.json()
        dados = dados['data']
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
