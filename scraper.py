import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

option = Options()
option.headless = True
option.add_argument("--window-size=1000,1000")
s = Service('.\drivers\chromedriver.exe')
driver = webdriver.Chrome(options=option,service=s)

urls = ['https://www.flashscore.com.br/futebol/portugal/liga-portugal-2021-2022/resultados/']

for url in urls:
    driver.get(url)
    time.sleep(2)
    
    try:
        driver.find_element(by=By.XPATH,value="//*[@id='onetrust-accept-btn-handler']").click()
        time.sleep(1)
    except:
        pass

    while True:
        try:
            element = driver.find_element(by=By.XPATH,value="//*[@id='lsadvert-zid-805']/div/div[2]")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            time.sleep(1)
            driver.find_element(by=By.XPATH,value="//*[@id='live-table']/div[1]/div/div/a").click()
            time.sleep(2)
        except:
            break

    elemento_links = driver.find_element(by=By.XPATH,value="//*[@id='live-table']/div[1]/div/div")
    html_links = elemento_links.get_attribute('outerHTML')

    soup = BeautifulSoup(html_links,'html.parser')
    links_partidas = []
    for i in soup.findAll(title="Clique para detalhes do jogo!"):
        links_partidas.append('https://www.flashscore.com.br/jogo/' + str(i.get('id')[4:]) + '/#/resumo-de-jogo/estatisticas-de-jogo/')

    soups = []
    for link in links_partidas:
        driver.get(link)
        time.sleep(2)

        partida_html = driver.find_element(by=By.XPATH,value="//*[@id='detail']")
        partida_html = partida_html.get_attribute('outerHTML')
        partida_soup = BeautifulSoup(partida_html,'html.parser') 
        soups.append(partida_soup)

    driver.quit()

    data = []
    for soup in soups:
        estatisticas = {}
        estatisticas['rodada'] = soup.find('span',class_='tournamentHeader__country').a.getText().strip().split()[-1]
        estatisticas['mandante'] = soup.find('div',class_='duelParticipant__home').find('a',class_='participant__participantName participant__overflow').get_text().strip()
        estatisticas['visitante'] = soup.find('div',class_='duelParticipant__away').find('a',class_='participant__participantName participant__overflow').get_text().strip()
        estatisticas['gols_man'] = soup.find('div',class_='detailScore__wrapper').findAll('span')[0].get_text().strip()
        estatisticas['gols_vis'] = soup.find('div',class_='detailScore__wrapper').findAll('span')[2].get_text().strip()
        rows = soup.findAll('div',class_='stat__row')
        for row in rows:
            nome = row.find('div',class_='stat__categoryName').get_text().strip()
            estatisticas[nome + str('_man')] = row.find('div',class_='stat__homeValue').get_text().strip()
            estatisticas[nome + str('_vis')] = row.find('div',class_='stat__awayValue').get_text().strip()
        data.append(estatisticas)

    data = pd.DataFrame(data)
    
    pais = url.split('/')[4]
    liga = url.split('/')[5]
    nome_arquivo = pais+'_'+liga
    data.to_csv(str('./data/'+nome_arquivo+'.csv'),sep=';',encoding='utf-8',index=False)
