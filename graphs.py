from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

from dados_covid import read_data_from_ms, update_graphs_in_json

from sys import argv


class Grafico:
    def __init__(self, figsize=(14, 10)):
        self.__df = read_data_from_ms()
        self.__filename = 'default'
        self.__fig = plt.figure(figsize=figsize)
        self.__ax = plt.subplot()
        self.funcoes = {
            'casos_acumulados': self.casos_acumulados,
            'casos_novos': self.casos_novos,
            'mortes_acumuladas': self.mortes_acumuladas,
            'mortes_novas': self.mortes_novas,
            'casos_full': self.casos_full,
            'mortes_full': self.mortes_full
        }

    @property
    def filename(self):
        return self.__filename

    @property
    def caption(self):
        caption = self.__filename.capitalize().replace('-', ' ')
        caption = caption.replace('full', '').strip()
        return caption

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

    def mortes_acumuladas(self, ax=None, semilog=False):
        if ax is None:
            ax = self.__ax
        df = self.__df['obitosAcumulado']
        title = 'Óbitos acumulados de Covid-19 por data de notificação'
        self.__filename = 'mortes-acumuladas'
        color = 'm'
        if semilog:
            self.__semilog_plot(df, ax, title, color)
        else:
            self.__line_plot(df, ax, title, color)
        return self

    def mortes_novas(self, ax=None):
        if ax is None:
            ax = self.__ax
        df = self.__df['obitosNovos']
        title = 'Óbitos novos de Covid-19 por data de notificação'
        self.__filename = 'mortes-novas'
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

    def mortes_full(self):
        fig, (ax1, ax2) = plt.subplots(2, 1)
        fig.set_size_inches((12, 12))
        self.mortes_acumuladas(ax1)
        self.mortes_novas(ax2)

        self.__filename = 'mortes-full'
        return self

    def __semilog_plot(self, df, ax, title, color='b'):
        plt.style.use('fivethirtyeight')
        self.__filename += '-log'
        self.__ax.semilogy(df, color=color)
        self.__ax.set_title(title + ' (escala logarítmica)')
        self.__ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))

    def __line_plot(self, df, ax, title, color):
        ax.plot(df, linewidth=4.0, color=color)
        ax.set_title(title)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))
        ax.yaxis.grid(True)

    def __bar_plot(self, df, ax, title, color):
        ax.bar(df.index, df, color=color)
        ax.set_title(title)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_formatter(DateFormatter('%d/%m'))
        ax.yaxis.grid(True)

    def save_as_png(self):
        plt.savefig(f'images/{self.__filename}.png')
        print(f'Arquivo <{self.__filename}> salvo.')
        self.__filename = 'default'
        plt.cla()


if __name__ == '__main__':
    graphs_metadata = {}
    graficos = Grafico()
    if len(argv) > 1:
        for k, function in graficos.funcoes.items():
            if k in argv:
                arquivo = function()
                filename = arquivo.filename
                caption = arquivo.caption
                arquivo.save_as_png()
                graphs_metadata[filename] = {'id': None, 'caption': caption}
    else:
        keys = 'casos_full', 'mortes_full'
        for function in keys:
            arquivo = graficos.funcoes[function]()
            filename = arquivo.filename
            caption = arquivo.caption
            arquivo.save_as_png()
            graphs_metadata[filename] = {'id': None, 'caption': caption}

    update_graphs_in_json(graphs_metadata)
