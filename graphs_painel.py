import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

from sys import argv


class Grafico:
    def __init__(self, figsize=(14, 8)):
        self.__df = self.__read_data()
        self.__filename = 'default'
        self.__fig = plt.figure(figsize=figsize)
        self.__ax = plt.subplot()

    def casos_acumulados(self, semilog=False):
        df = self.__df['casosAcumulado']
        title = 'Casos acumulados de Covid-19 por data de notificação'
        self.__filename = 'casos-acumulados'
        color = 'g'
        if semilog:
            self.__semilog_plot(df, title, color)
        else:
            self.__line_plot(df, title, color)
        return self

    def casos_novos(self):
        df = self.__df['casosNovos']
        title = 'Casos novos de Covid-19 por data de notificação'
        self.__filename = 'casos-novos'
        color = 'g'
        self.__bar_plot(df, title, color)
        return self

    def obitos_acumulados(self, semilog=False):
        df = self.__df['obitosAcumulado']
        title = 'Óbitos acumulados de Covid-19 por data de notificação'
        self.__filename = 'obitos-acumulados'
        color = 'm'
        if semilog:
            self.__semilog_plot(df, title, color)
        else:
            self.__line_plot(df, title, color)
        return self

    def obitos_novos(self):
        df = self.__df['obitosNovos']
        title = 'Óbitos novos de Covid-19 por data de notificação'
        self.__filename = 'obitos-novos'
        color = 'm'
        self.__bar_plot(df, title, color)
        return self

    def casos_full(self):
        self.__fig.set_size_inches(14, 14)

        self.__ax = plt.subplot('211')
        self.casos_acumulados()

        self.__ax = plt.subplot('212')
        self.casos_novos()

        self.__filename = 'casos-full'
        return self

    def obitos_full(self):
        self.__fig.set_size_inches(14, 14)

        self.__ax = plt.subplot('211')
        self.obitos_acumulados()

        self.__ax = plt.subplot('212')
        self.obitos_novos()

        self.__filename = 'obitos-full'
        return self

    def __semilog_plot(self, df, title, color='b'):
        self.__filename += '-log'
        self.__ax.semilogy(df, color=color)
        self.__ax.set_title(title + ' (escala logarítmica)')
        self.__ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))

    def __line_plot(self, df, title, color):
        self.__ax.plot(df, linewidth=4.0, color=color)
        self.__ax.set_title(title)
        self.__ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.__ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))

    def __bar_plot(self, df, title, color):
        self.__ax.bar(df.index, df, color=color)
        self.__ax.set_title(title)
        self.__ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.__ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))

    def __read_data(self):
        df = pd.read_excel('~/Desktop/painel-covid.xlsx')
        df = df[['data', 'regiao', 'casosAcumulado',
                 'casosNovos', 'obitosAcumulado', 'obitosNovos']]
        brasil_df = df[df['regiao'] == 'Brasil'].set_index('data')
        print('Dados lidos com sucesso!')
        return brasil_df

    def save_as_png(self):
        self.__fig.savefig(f'images/{self.__filename}.png')
        print(f'Arquivo <{self.__filename}> salvo.')
        self.__filename = 'default'
        plt.cla()


if __name__ == '__main__':
    graficos = Grafico()
    if 'casos_acumulados' in argv:
        graficos.casos_acumulados().save_as_png()
    if 'casos_novos' in argv:
        graficos.casos_novos().save_as_png()
    if 'obitos_acumulados' in argv:
        graficos.obitos_acumulados().save_as_png()
    if 'obitos_novos' in argv:
        graficos.obitos_novos().save_as_png()
    if 'casos_full' in argv:
        graficos.casos_full().save_as_png()
    if 'obitos_full' in argv:
        graficos.obitos_full().save_as_png()
