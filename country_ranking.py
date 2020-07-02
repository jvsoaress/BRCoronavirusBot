import pandas as pd
import requests
import json


# monta um ranking com base nos dados atuais e salva em arquivo JSON
def create_json_ranking():
    translation = {
        'United States of America': 'Estados Unidos',
        'Brazil': 'Brasil',
        'India': 'Índia',
        'Russian Federation': 'Rússia',
        'United Kingdom': 'Reino Unido',
        'Peru': 'Peru',
        'Chile': 'Chile',
        'Spain': 'Espanha',
        'Italy': 'Itália',
        'Iran, Islamic Republic of': 'Irã',
        'Mexico': 'México',
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

    r = requests.get('https://api.covid19api.com/summary')
    dados = r.json()['Countries']
    df_full = pd.DataFrame.from_dict(dados).sort_values(
        by='TotalConfirmed', ascending=False).head(15).reset_index()
    df = df_full[['Country', 'CountryCode', 'TotalConfirmed', 'NewConfirmed',
                  'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'Date']].copy()
    df.loc[:, 'Country'] = df['Country'].map(lambda x: translation[x])
    df.to_json('country_ranking.json')
    print('Arquivo <country_ranking.json> criado com sucesso!')


if __name__ == '__main__':
    create_json_ranking()
