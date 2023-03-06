  from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
  

serv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=serv)

id_acount = 'j.barbosaa0'
pass_acount = 'Workpass123!'
work_acount = 'j.barbosaa0'

driver.get('https://www.instagram.com/')
time.sleep(2)

driver.find_element('xpath', '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(id_acount)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(pass_acount)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[3]').click()
time.sleep(4)
driver.get('https://www.instagram.com/unbpaquera/followers/')
time.sleep(4)

fBody = driver.find_element("xpath", "//div[@class='_aano']")  # encontra o corpo da lista de seguidores

contador = 1
scroll = 0  # inicializa a variável de controle de scroll
ini_folow = []
dex_folow = []
dt_time_flw = []
dt_time_unf = []
while scroll < 2:  # enquanto o número de scrolls for menor que 5
    for _ in range(0, 6):
        name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div[2]/div[1]/div/div/div/div/a/span/div').text
        try:
            if driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div[3]/button/div/div').text == 'Seguir':
                driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div[3]/button/div/div').click()
                ini_folow.append(name)
                dt_time_flw.append(datetime.now())
                time.sleep(2)
            else:
                dt_time_unf.append(datetime.now())
                dex_folow.append(name)            
                driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div[3]/button/div/div').click()
                time.sleep(2)
                driver.find_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]').click()
                time.sleep(2)
            contador += 1
        except:
            print('Xpath alterado')
            break
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)  # executa o script que rola a lista de seguidores para baixo
    time.sleep(2)  # espera 2 segundos para o carregamento da página
    scroll += 1  # incrementa a variável de controle de scroll em 1 unidade


