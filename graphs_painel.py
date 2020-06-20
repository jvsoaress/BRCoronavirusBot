import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator


class Grafico:
    def __init__(self):
        self.__df = self.__read_data()
        self.__filename = 'default'
        self.__fig = plt.figure(figsize=(14, 8))
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

    def casos_novos(self):
        df = self.__df['casosNovos']
        title = 'Casos novos de Covid-19 por data de notificação'
        self.__filename = 'casos-novos'
        color = 'g'
        self.__bar_plot(df, title, color)

    def obitos_acumulados(self, semilog=False):
        df = self.__df['obitosAcumulado']
        title = 'Óbitos acumulados de Covid-19 por data de notificação'
        self.__filename = 'obitos-acumulados'
        color = 'm'
        if semilog:
            self.__semilog_plot(df, color)
        else:
            self.__line_plot(df, color)

    def obitos_novos(self):
        df = self.__df['obitosNovos']
        title = 'Óbitos novos de Covid-19 por data de notificação'
        self.__filename = 'obitos-novos'
        color = 'm'
        self.__bar_plot(df, title, color)

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

    def all_graphs(self):
        self.casos_acumulados()
        self.casos_novos()
        self.obitos_acumulados()
        self.obitos_novos()

    def casos_full(self):
        self.__fig.set_size_inches(14, 14)

        self.__ax = plt.subplot('211')
        self.casos_acumulados()

        self.__ax = plt.subplot('212')
        self.casos_novos()

        self.__filename = 'casos-full'

    def obitos_full(self):
        self.__fig.set_size_inches(14, 14)

        self.__ax = plt.subplot('211')
        df1 = self.__df['obitosAcumulado']
        title = 'Óbitos acumulados de Covid-19 por data de notificação'
        color = 'm'
        self.__line_plot(df1, title, color)

        self.__ax = plt.subplot('212')
        df2 = self.__df['obitosNovos']
        title = 'Óbitos novos de Covid-19 por data de notificação'
        color = 'm'
        self.__bar_plot(df2, title, color)

        self.__filename = 'obitos-full'

    def save_as_png(self):
        plt.savefig(f'images/{self.__filename}.png')
        print(f'Arquivo <{self.__filename}> salvo.')
        self.__filename = 'default'


if __name__ == '__main__':
    graficos = Grafico()
    graficos.casos_full()
    graficos.save_as_png()

    # x = range(10, 100, 10)
    # y = list(map(lambda x: x**2, x))
    # plt.subplot('211')
    # plt.plot(x, y)
    # plt.show()
