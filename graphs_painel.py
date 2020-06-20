from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

from covid_data import read_data

from sys import argv


class Grafico:
    def __init__(self, figsize=(14, 10)):
        self.__df = read_data()
        self.__filename = 'default'
        self.__fig = plt.figure(figsize=figsize)
        self.__ax = plt.subplot()
        self.__funcoes = {
            'casos_acumulados': graficos.casos_acumulados,
            'casos_novos': graficos.casos_novos,
            'obitos_acumulados': graficos.obitos_acumulados,
            'obitos_novos': graficos.obitos_novos,
            'casos_full': graficos.casos_full,
            'obitos_full': graficos.obitos_full
        }

    def casos_acumulados(self, ax=None, semilog=False):
        if ax is None:
            ax = self.__ax
        df = self.__df['casosAcumulado']
        title = 'Casos acumulados de Covid-19 por data de notificação'
        self.__filename = 'casos-acumulados'
        color = 'g'
        if semilog:
            self.__semilog_plot(df, ax, title, color)
        else:
            self.__line_plot(df, ax, title, color)
        return self

    def casos_novos(self, ax=None):
        if ax is None:
            ax = self.__ax
        df = self.__df['casosNovos']
        title = 'Casos novos de Covid-19 por data de notificação'
        self.__filename = 'casos-novos'
        color = 'g'
        self.__bar_plot(df, ax, title, color)
        return self

    def obitos_acumulados(self, ax=None, semilog=False):
        if ax is None:
            ax = self.__ax
        df = self.__df['obitosAcumulado']
        title = 'Óbitos acumulados de Covid-19 por data de notificação'
        self.__filename = 'obitos-acumulados'
        color = 'm'
        if semilog:
            self.__semilog_plot(df, ax, title, color)
        else:
            self.__line_plot(df, ax, title, color)
        return self

    def obitos_novos(self, ax=None):
        if ax is None:
            ax = self.__ax
        df = self.__df['obitosNovos']
        title = 'Óbitos novos de Covid-19 por data de notificação'
        self.__filename = 'obitos-novos'
        color = 'm'
        self.__bar_plot(df, ax, title, color)
        return self

    def casos_full(self):
        fig, (ax1, ax2) = plt.subplots(2, 1)
        fig.set_size_inches((12, 12))
        self.casos_acumulados(ax1)
        self.casos_novos(ax2)

        self.__filename = 'casos-full'
        return self

    def obitos_full(self):
        fig, (ax1, ax2) = plt.subplots(2, 1)
        fig.set_size_inches((12, 12))
        self.obitos_acumulados(ax1)
        self.obitos_novos(ax2)

        self.__filename = 'obitos-full'
        return self

    def __semilog_plot(self, df, ax, title, color='b'):
        self.__filename += '-log'
        self.__ax.semilogy(df, color=color)
        self.__ax.set_title(title + ' (escala logarítmica)')
        self.__ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))

    def __line_plot(self, df, ax, title, color):
        ax.plot(df, linewidth=4.0, color=color)
        ax.set_title(title)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))

    def __bar_plot(self, df, ax, title, color):
        ax.bar(df.index, df, color=color)
        ax.set_title(title)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))

    def save_as_png(self):
        plt.savefig(f'images/{self.__filename}.png')
        print(f'Arquivo <{self.__filename}> salvo.')
        self.__filename = 'default'
        plt.cla()


if __name__ == '__main__':
    graficos = Grafico()
    for k, function in graficos.entrada.items():
        if k in argv:
            function().save_as_png()
