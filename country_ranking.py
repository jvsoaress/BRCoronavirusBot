import pandas as pd
import requests
import json
import flag

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
    texto = '<b>\U0001F6A8 Ranking dos países com Covid-19</b>\n\n'
    texto += f'<code>   {"País":<17}Casos</code>\n'
    for j in range(len(dados['Country'])):
        bandeira = flag.flag(dados['CountryCode'][str(j)])
        texto += f'<code>{bandeira} {dados["Country"][str(j)]:<17}{dados["TotalConfirmed"][str(j)]}</code>\n'
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
