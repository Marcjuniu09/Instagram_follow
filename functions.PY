from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
serv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=serv)

id_acount = 'j.barbosaa0'
pass_acount = 'Workpass123!'
work_acount = 'j.barbosaa0'
acount_follow = 'majuu.qurz'


#Parte que leva para a página de login
driver.get('https://www.instagram.com/')
time.sleep(2)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(id_acount)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(pass_acount)
driver.find_element('xpath', '//*[@id="loginForm"]/div/div[3]').click()
time.sleep(4)

#Salvando a lista de seguidores atuais
def save_current_followers(username, driver):
    """
    Salva a lista de seguidores atuais
    name é o nome do usuário que ele tá salvando
    contador_crt é meio que pra ir pegando os nomes dos seguidores. Basicamente é uma forma de iterar
    scroll_st é pra parar o loop quando o xpath mudar ou quando chegar no final da lista
    """
    driver.get(f'https://www.instagram.com/{username}/followers/')
    time.sleep(3)
    fBody_st = driver.find_element("xpath", "//div[@class='_aano']") 
    contador_crt = 0
    scroll_st = 0
    current_followers = [] #Lista de seguidores atuais
    cont_interrupt = 0 #Contador para parar o loop quando o xpath mudar

    while scroll_st < 1:  
        for _ in range(0, 6):
            contador_crt += 1
            try:
                time.sleep(2)
                name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador_crt}]/div/div/div/div[2]/div/div/div[1]/span/div/div[1]/div/a/span/div').text
                time.sleep(2)
                print(name)
                if name not in current_followers:
                    current_followers.append(name)
            except:
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody_st) 
                cont_interrupt += 1
                if cont_interrupt == 5:
                    print('Xpath alterado')
                    scroll_st += 1
                    break
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody_st) 
    data = {
    'Seguidores Atuais': current_followers
        }
    df = pd.DataFrame(data)
    df.to_csv('dataframe.csv', index=False)

#Seguindo as pessoas da conta que eu quero
def follow(username, driver):
    """
    Segue as pessoas da conta que eu quero
    name é o nome do usuário que vai começar a seguir
    contador serve basicamente pra iterar na lista de seguidores
    scroll é pra parar o loop quando o xpath mudar ou quando chegar no final da lista
    For sempre executa 6 vezes porque é o número de seguidores que aparece na tela antes de rolar a página
    tempo é o tempo que o bot vai esperar pra seguir o próximo usuário, e sempre vai ser um número aleatório entre 0 e 40
    """
    tempo = int(randint(3,40))
    driver.get(f'https://www.instagram.com/{username}/followers/')
    time.sleep(4)
    fBody = driver.find_element("xpath", "//div[@class='_aano']")  # encontra o corpo da lista de seguidores
    contador = 0
    scroll = 0
    ini_folow =  [] #Lista de quem eu comecei a seguir
    dt_time_flw = [] #Lista de data e hora que eu comecei a seguir
    cont_interrupt_flw = 0 #Contador para parar o loop quando o xpath mudar

    while scroll < 1: 
        for _ in range(0, 6):
            contador += 1
            name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div/div/div/div[2]/div/div/div[1]/span/div/div/div/a/span/div').text # encontra o nome do seguidor
            try:
                if driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div/div/div/div[3]/div/button/div/div').text == 'Seguir': # verifica se o botão de seguir está escrito 'Seguir'
                    time.sleep(int(tempo))
                    driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador}]/div/div/div/div[3]/div/button/div/div').click() # clica no botão de seguir
                    ini_folow.append(name)
                    dt_time_flw.append(datetime.now())
                    time.sleep(2)
                else:
                    continue
            except:
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)  # executa o script que rola a lista de seguidores para baixo
                cont_interrupt_flw += 1
                if cont_interrupt_flw == 5:
                    print('Xpath alterado')
                    scroll += 1  
                    break
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)  # executa o script que rola a lista de seguidores para baixo
        time.sleep(2)  # espera 2 segundos para o carregamento da página

        data = {
        'Seguindo': ini_folow
        }

    df = pd.DataFrame(data)
    df.to_csv('dataframe.csv', index=False)
    return ini_folow


#Status de quem eu comecei a seguir, se está seguindo ou não e se já seguia
def status_follow(username, driver):
    """
    Verifica se as pessoas que eu comecei a seguir estão seguindo de volta
    name é o nome do usuário que eu comecei a seguir
    contador_st é o contador para iterar
    scroll_st é pra parar o loop quando o xpath mudar ou quando chegar no final da lista
    Essa função verifica se o nome tá na lista de seguidores atuais, se não tiver, ela verifica se o nome tá na lista de seguidores que eu comecei a seguir, 
    se não tiver, ela adiciona 'Não' na lista de status de quem eu comecei a seguir e se tiver, ela adiciona 'Já seguia' na lista de status de quem eu comecei a seguir 
    """
    driver.get(f'https://www.instagram.com/{username}/followers/')
    time.sleep(2)
    fBody_st = driver.find_element("xpath", "//div[@class='_aano']") 
    contador_st = 1
    scroll_st = 0
    st_follow = [] #Lista de status de quem eu comecei a seguir (sim ou não)

    
    while scroll_st < 1:  
        for _ in range(0, 6):
            try:    
                name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador_st}]/div/div/div/div[2]/div/div/div[1]/span/div/div[1]/div/a/span/div').text
                time.sleep(2)
                if name in df['Seguindo'].values:
                    st_follow.append('SIM')
                else:
                    if name in df['Seguidores Atuais'].values:
                        st_follow.append('Já seguia')
                    else:
                        st_follow.append('Não')
            except:
                print('Xpath alterado')
                scroll_st += 1
                break
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody_st) 
        return st_follow


#Deixando de seguir quem eu comecei a seguir
def unfollow():
    """
    Função para deixar de seguir quem eu comecei a seguir, verifica se o nome está na lista de pessoas que estou seguindo, se tiver, ele clica no botão de deixar de seguir
    """
    df = pd.read_csv('dataframe.csv')
    driver.get(f'https://www.instagram.com/{work_acount}/following/')
    time.sleep(2)
    fBody_unf = driver.find_element("xpath", "//div[@class='_aano']")
    contador_unf = 1
    scroll_unf = 0
    tempo_unf = int(randint(0, 40))
    while scroll_unf < 1: 
        for _ in range(0, 6):
            contador_unf += 1
            time.sleep(2)
            name = driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador_unf}]/div/div/div/div[2]/div/div/div[1]/span/div/div[1]/div/a/span/div').text
            try:
                if name in df['Seguindo'].values:
                    driver.find_element('xpath', f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{contador_unf}]/div/div/div/div[3]/div/button/div/div').click() 
                    time.sleep(3)
                    driver.find_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/button[1]').click()
                    time.sleep(tempo_unf)
                else:
                    continue
            except:
                print('Xpath alterado')
                scroll_unf += 1
                break
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody_unf)
        time.sleep(2)
        scroll_unf += 1


