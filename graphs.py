import base64
from selenium import webdriver
from time import sleep


def download_graphs():
    driver = webdriver.Chrome('/home/jovi/Downloads/chromedriver')
    driver.get('https://covid.saude.gov.br')
    sleep(5)

    image = driver.find_element_by_xpath(
        '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/painel-geral-component/div/div[3]/div[2]/div[1]/chart-bars-component/div/div/canvas'
    )
    image2 = driver.find_element_by_xpath(
        '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/painel-geral-component/div/div[4]/div[1]/div[1]/chart-line-component/div/div/canvas'
    )

    # get the image as a PNG base64 string
    image_base64 = driver.execute_script(
        "return arguments[0].toDataURL('image/jpg').substring(21);", image)

    image2_base64 = driver.execute_script(
        "return arguments[0].toDataURL('image/jpg').substring(21);", image2)

    driver.close()

    # decode
    graph1 = base64.b64decode(image_base64)
    graph2 = base64.b64decode(image2_base64)
    graphs = {'graph1': graph1, 'graph2': graph2}

    # save to a file
    for name, img in graphs.items():
        with open(f'images/{name}.jpg', 'wb') as f:
            f.write(img)


if __name__ == '__main__':
    download_graphs()
