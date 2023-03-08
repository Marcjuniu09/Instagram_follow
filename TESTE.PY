from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
serv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=serv)

ini_folow =  [] #Lista de quem eu comecei a seguir
dt_time_flw = [] #Lista de data e hora que eu comecei a seguir
dt_time_unf = [] #Lista de data e hora que eu deixei de seguir
st_follow = [] #Lista de status de quem eu comecei a seguir (sim ou não)
dex_folow = [] #Lista de quem eu deixei de seguir
current_followers = [] #Lista de seguidores atuais
id_acount = 'j.barbosaa0'
pass_acount = 'Workpass123!'
work_acount = 'j.barbosaa0'
acount_follow = 'majuu.qurz'
contador = 0
scroll = 0 
contador_unf = 0
scroll_unf = 0
contador_st = 1
scroll_st = 0
contador_crt = 0

#Parte que leva para a página de login
driver.get('https://www.instagram.com/')
time.sleep(2)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(id_acount)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(pass_acount)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[3]').click()
time.sleep(4)

#Salvando a lista de seguidores atuais
def save_current_followers(username, driver):
    driver.get(f'https://www.instagram.com/{username}/followers/')
    time.sleep(3)
    fBody_st = driver.find_element("xpath", "//div[@class='_aano']") 

    while scroll_st < 2:  
        for _ in range(0, 6):
            contador_crt += 1
            try:
                name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{contador_crt}]/div[2]/div[1]/div/div/div/div/a/span/div').text
                time.sleep(2)
                if name not in current_followers:
                    current_followers.append(name)
            except:
                print('Xpath alterado')
                break
        scroll_st += 1
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody_st) 
        
    return current_followers

#Seguindo as pessoas da conta que eu quero
def follow(username, driver):

    driver.get(f'https://www.instagram.com/{username}/followers/')
    time.sleep(4)
    fBody = driver.find_element("xpath", "//div[@class='_aano']")  # encontra o corpo da lista de seguidores

    while scroll < 3: 
        for _ in range(0, 6):
            contador += 1
            name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div[2]/div[1]/div/div/div/div/a/span/div').text
            try:
                if driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div[3]/button/div/div').text == 'Seguir':
                    driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div[3]/button/div/div').click()
                    ini_folow.append(name)
                    dt_time_flw.append(datetime.now())
                    time.sleep(2)
                else:
                    continue
            except:
                print('Xpath alterado')
                break
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)  # executa o script que rola a lista de seguidores para baixo
        time.sleep(2)  # espera 2 segundos para o carregamento da página
        scroll += 1  
    return ini_folow, dt_time_flw

#Status de quem eu comecei a seguir, se está seguindo ou não e se já seguia
def status_follow(username, driver):
    driver.get(f'https://www.instagram.com/{username}/followers/')
    time.sleep(2)
    fBody_st = driver.find_element("xpath", "//div[@class='_aano']") 

    while scroll_st < 2:  
        for _ in range(0, 6):
            name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador_st}]/div[2]/div[1]/div/div/div[1]/div/a/span/div').text
            time.sleep(2)
            if name in ini_folow:
                st_follow.append('SIM')
            else:
                if name in current_followers:
                    st_follow.append('Já seguia')
                else:
                    st_follow.append('Não')
        scroll_st += 1
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody_st) 
        return st_follow

#Deixando de seguir quem eu comecei a seguir
def unfollow():
    df = pd.read_csv('dataframe.csv')
    driver.get(f'https://www.instagram.com/{work_acount}/following/')
    time.sleep(2)
    fBody_unf = driver.find_element("xpath", "//div[@class='_aano']")

    while scroll_unf < 4: 
        for _ in range(0, 6):
            contador_unf += 1
            time.sleep(2)
            name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{contador_unf}]/div[2]/div[1]/div/div/div/div/a/span/div').text
            try:
                if name in ini_folow:
                    driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div/div[{contador_unf}]/div[3]/button/div/div').click() 
                    time.sleep(2)
                    driver.find_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]').click()
                    time.sleep(2)
                else:
                    continue
            except:
                print('Xpath alterado')
                break
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody_unf)
        time.sleep(2)
        scroll_unf += 1


data = {
    'Seguindo': ini_folow,
    'Data e Hora': dt_time_flw,
    'Seguidores Atuais': current_followers
}
df = pd.DataFrame(data)
df.to_csv('dataframe.csv', index=False)
time.sleep(4)