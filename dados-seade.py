import requests
import csv


def download_data():
    with open('dados-covid19.csv', 'wb') as arquivo:
        r = requests.get('http://www.seade.gov.br/wp-content/uploads/2020/05/Dados-covid-19-estado.csv')
        dados = r.content
        arquivo.write(dados)


def show_data():
    with open('dados-covid19.csv', errors='ignore') as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=';')
        for linha in leitor:
            if linha['Data'] != '':
                print(linha)


if __name__ == '__main__':
    show_data()