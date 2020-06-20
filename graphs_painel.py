import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator


class Grafico:
    def __init__(self, show_graph=False):
        self.__df = self.__read_data()
        self.__filename = 'default'
        self.__show_graph = show_graph
        self.__title = 'Título'
        self.__color = 'b'

    def casos_acumulados(self, semilog=False):
        df = self.__df['casosAcumulado']
        self.__title = 'Casos acumulados de Covid-19 por data de notificação'
        self.__filename = 'casos-acumulados'
        self.__color = 'g'
        if semilog:
            self.__semilog_plot(df)
        else:
            self.__line_plot(df)

    def casos_novos(self):
        df = self.__df['casosNovos']
        self.__title = 'Casos novos de Covid-19 por data de notificação'
        self.__filename = 'casos-novos'
        self.__color = 'g'
        self.__bar_plot(df)

    def obitos_acumulados(self, semilog=False):
        df = self.__df['obitosAcumulado']
        self.__title = 'Óbitos acumulados de Covid-19 por data de notificação'
        self.__filename = 'obitos-acumulados'
        self.__color = 'm'
        if semilog:
            self.__semilog_plot(df)
        else:
            self.__line_plot(df)

    def obitos_novos(self):
        df = self.__df['obitosNovos']
        self.__title = 'Óbitos novos de Covid-19 por data de notificação'
        self.__filename = 'obitos-novos'
        self.__color = 'm'
        self.__bar_plot(df)

    def __semilog_plot(self, df):
        self.__filename += '-log'
        plt.semilogy(df)
        plt.title(self.__title + ' (escala logarítmica)')
        plt.gcf().set_size_inches(12, 7)
        self.save_as_png()
        if self.__show_graph:
            plt.show()

    def __line_plot(self, df):
        plt.plot(df, linewidth=4.0, color=self.__color)
        plt.title(self.__title)
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m'))
        plt.gcf().set_size_inches(12, 7)
        self.save_as_png()
        if self.__show_graph:
            plt.show()

    def __bar_plot(self, df):
        plt.bar(df.index, df, color=self.__color)
        plt.title(self.__title)
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m'))
        plt.gcf().set_size_inches(12, 7)
        self.save_as_png()
        if self.__show_graph:
            plt.show()

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
        df1 = self.__df['casosAcumulado']
        plt.subplot('211')
        plt.plot(df1, color='g')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m'))
        plt.title(self.__title)
        df2 = self.__df['casosNovos']
        plt.subplot('212')
        plt.bar(df2.index, df2, color='g')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m'))
        plt.title(self.__title)
        plt.gcf().set_size_inches(12, 7)
        self.__filename = 'casos-full'
        self.save_as_png()
        if self.__show_graph:
            plt.show()

    def obitos(self):
        pass

    def save_as_png(self):
        plt.savefig(f'images/{self.__filename}.png')
        print(f'Arquivo <{self.__filename}> salvo com sucesso!')
        self.__filename = 'default'


if __name__ == '__main__':
    graficos = Grafico(show_graph=True)
    graficos.casos_full()

    # x = range(10, 100, 10)
    # y = list(map(lambda x: x**2, x))
    # plt.subplot('211')
    # plt.plot(x, y)
    # plt.show()
