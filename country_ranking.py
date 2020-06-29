import pandas as pd
import requests

if __name__ == '__main__':
    def country_ranking():
        r = requests.get('https://api.covid19api.com/summary')
        dados = r.json()['Countries']
        df_full = pd.DataFrame.from_dict(dados).sort_values(
            by='TotalConfirmed', ascending=False).head(5).reset_index()
        df = df_full[['Country', 'CountryCode', 'TotalConfirmed', 'NewConfirmed',
                    'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'NewRecovered', 'Date']]
        df.to_json('country_ranking.json')
