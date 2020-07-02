import pandas as pd
import requests
import json

translation = {
    'United States of America': 'Estados Unidos',
    'Brazil': 'Brasil',
    'India': 'India',
    'Russian Federation': 'Rússia',
    'United Kingdom': 'Reino Unido',
    'Peru': 'Peru',
    'Chile': 'Chile',
    'Spain': 'Espanha',
    'Italy': 'Itália',
    'Iran, Islamic Republic of': 'Irã',
    'Mexico': 'Mexico',
    'Pakistan': 'Paquistão',
    'Canada': 'Canadá',
    'France': 'França',
    'Turkey': 'Turquia',
    'Germany': 'Alemanha',
    'Saudi Arabia': 'Arábia Saudita',
    'South Africa': 'África do Sul',
    'Bangladesh': 'Bangladesh',
    'Colombia': 'Colômbia'
}


def get_ranking_from_json():
    with open('country_ranking.json') as f:
        dados = json.load(f)
    texto = f'{"País":<20}Casos confirmados\n'
    for j in range(len(dados['Country'])):
        texto += f'{dados["Country"][str(j)]:<20}{dados["TotalConfirmed"][str(j)]}\n'
    return texto


# monta um ranking com base nos dados atuais e salva em arquivo JSON
def create_json_ranking(top=5):
    r = requests.get('https://api.covid19api.com/summary')
    dados = r.json()['Countries']
    df_full = pd.DataFrame.from_dict(dados).sort_values(
        by='TotalConfirmed', ascending=False).head(top).reset_index()
    df = df_full[['Country', 'CountryCode', 'TotalConfirmed', 'NewConfirmed',
                  'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'Date']].copy()
    df.loc[:, 'Country'] = df['Country'].map(lambda x: translation[x])
    df.to_json('country_ranking.json')


if __name__ == '__main__':
    create_json_ranking()
    get_ranking_from_json()
