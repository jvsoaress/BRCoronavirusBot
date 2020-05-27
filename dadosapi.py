import requests
from datetime import date, datetime


def format_day(dia):
    dia = dia.split('-')
    mes, dia = dia[1], dia[2]
    return f'{dia}/{mes}'


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
            data = data.split('T')
            dia = data[0]
            dia = format_day(dia)
            hora = data[1].split('.')[0]

            msg = f'\U00002705 <b>Casos confirmados:</b> {dados["confirmed"]}\n' \
                  f'\U00002620 <b>Mortes:</b> {dados["deaths"]}\n' \
                  f'\U0001F504 <b>Recuperados:</b> {dados["recovered"]}\n' \
                  f'<em>Atualizado em {dia} às {hora}</em>'
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

