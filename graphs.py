import base64
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Graph:
    all_graphs = dict()
    caption = {
        'graph1.jpg': 'Casos novos de COVID-19 por data de notificação',
        'graph2.jpg': 'Casos acumulados de COVID-19 por data de notificação',
        'graph3.jpg': 'Óbitos de COVID-19 por data de notificação',
        'graph4.jpg': 'Óbitos acumulados de COVID-19 por data de notificação'
    }


def execute_script(driver, image):
    return driver.execute_script("return arguments[0].toDataURL('image/jpg').substring(21);", image)


def download_graphs():
    chrome_options = Options()
    chrome_options.headless = True

    print('Abrindo o navegador...')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print('Acessando o site...')
    driver.get('https://covid.saude.gov.br')
    sleep(10)

    print('Iniciando coleta de elementos...')
    image = driver.find_element_by_xpath(
        '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/painel-geral-component/div/div[3]/div[1]/div[1]/chart-bars-component/div/div/canvas'
    )
    image2 = driver.find_element_by_xpath(
        '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/painel-geral-component/div/div[4]/div[1]/div[1]/chart-line-component/div/div/canvas'
    )
    image3 = driver.find_element_by_xpath(
        '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/painel-geral-component/div/div[9]/div[1]/div[1]/chart-bars-component/div/div/canvas'
    )
    image4 = driver.find_element_by_xpath(
        '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/painel-geral-component/div/div[10]/div[1]/div[1]/chart-line-component/div/div/canvas'
    )
    print('Elementos coletados com sucesso!')

    print('Iniciando conversão da imagem...')
    image_base64 = execute_script(driver, image)
    image2_base64 = execute_script(driver, image2)
    image3_base64 = execute_script(driver, image3)
    image4_base64 = execute_script(driver, image4)
    print('Imagens convertidas com sucesso!')

    driver.close()
    print('Navegador fechado')

    print('Decodificando bytes...')
    graph1 = base64.b64decode(image_base64)
    graph2 = base64.b64decode(image2_base64)
    graph3 = base64.b64decode(image3_base64)
    graph4 = base64.b64decode(image4_base64)
    graphs = {'graph1': graph1, 'graph2': graph2,
              'graph3': graph3, 'graph4': graph4}
    print('Bytes decodificados com sucesso!')

    print('Salvando em arquivo...')
    for name, img in graphs.items():
        with open(f'images/{name}.jpg', 'wb') as f:
            f.write(img)
    print('Arquivos salvos com sucesso!')


if __name__ == '__main__':
    download_graphs()
    Graph.all_graphs = dict()
