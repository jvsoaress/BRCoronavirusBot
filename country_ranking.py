import pandas as pd
import requests
import json

translation = {
    'United States of America': 'Estados Unidos',
    'Brazil': 'Brasil',
    'India': 'India',
    'Russian Federation': 'Rússia',
    'United Kingdom': 'Reino Unido'
}

def get_ranking_from_json():
    with open('country_ranking.json') as f:
        dados = json.load(f)
    print(dados)
    texto = f"""{'País':<30}{'Casos confirmados'}
{dados['Country'][str(0)]:<30}{dados['TotalConfirmed'][str(0)]}
{dados['Country'][str(1)]:<30}{dados['TotalConfirmed'][str(1)]}
    """
    print(texto)

# monta um ranking com base nos dados atuais e salva em arquivo JSON
if __name__ == '__main__':
    r = requests.get('https://api.covid19api.com/summary')
    dados = r.json()['Countries']
    df_full = pd.DataFrame.from_dict(dados).sort_values(
        by='TotalConfirmed', ascending=False).head(5).reset_index()
    df = df_full[['Country', 'CountryCode', 'TotalConfirmed', 'NewConfirmed',
                  'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'Date']]
    df.to_json('country_ranking.json')

    print(get_ranking_from_json())
