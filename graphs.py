import base64
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('/home/jovi/Downloads/chromedriver')
driver.get('https://covid.saude.gov.br')
sleep(5)
canvas = driver.find_element_by_xpath('/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/painel-geral-component/div/div[3]/div[2]/div[1]/chart-bars-component/div/div/canvas')

# get the canvas as a PNG base64 string
canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
driver.close()
# decode
canvas_png = base64.b64decode(canvas_base64)

# save to a file
with open("images/canvas.png", 'wb') as f:
    f.write(canvas_png)