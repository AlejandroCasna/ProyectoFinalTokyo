import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import warnings
from selenium.common.exceptions import NoSuchElementException
from unidecode import unidecode

warnings.filterwarnings("ignore")



''' Funcion scraping:Obligatoriamente pasar URL.

Parametro por defecto = Jugadores.
Parametros opcionales: 
Parametro1:Equipo.
Parametro1:Estadistica_jugador.
Parametro1:Estadistica_equipo.
Parametro1:Clasificacion.
Parametro1:Jugadores.


los parametros son tipo str.


Funcion hacer click llamada en todas las funciones'''

def hacer_clic(driver, by_locator):
    try:
        driver.find_element(*by_locator).click()
        
    except NoSuchElementException:
        print('hola')
    except Exception as e:
        print(f"Error al hacer clic: {e}")
        

def scraping(url, parametro='jugadores'):
    opciones = Options()
    opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
    opciones.add_experimental_option('useAutomationExtension', False)
    opciones.add_argument('--incognito')
    opciones.add_argument('--start-maximized')

    try:
        driver = webdriver.Chrome(options=opciones)
        driver.get(url)

        if not hacer_clic(driver, (By.ID, 'lnkCookie')):
            print('No se pudo hacer clic en el botón de cookies.')
    except Exception as e:
        print(f"Error durante la navegación: {e}")
        
    superLiga_Masculino = []  
    if parametro == 'jugadores':
        equipos = driver.find_elements(By.CLASS_NAME, 'rlvI')[0:14]
        for i in range(14):
                
            e = driver.find_elements(By.CLASS_NAME, 'rlvI')[i]
            
            print(e.text)
            
            e.click()
            
            print('Estoy dentro.')
            
            time.sleep(1)
        
            superLiga_Masculino.append(driver.find_elements(By.CLASS_NAME , 't-row')[3].text.split('\n'))
            
            print('Extraigo')
            
            time.sleep(1)
            
            driver.get(url)
        
            time.sleep(1)
        print('Scraping exitoso')
        return superLiga_Masculino
        

    elif parametro == 'equipo':
        equipos = driver.find_element(By.CSS_SELECTOR,'#ctl00_Content_Main_ctl00_Content_Main_CompetitonTeams_Name_TeamListViewPanel > div > div').text.split('\n')
        print('Scraping exitoso')
        return equipos

    elif parametro == 'estadistica_jugador':
        datos_por_pagina = {}
        for i in range(1, 6):
            hacer_clic(driver, (By.XPATH, f'//*[@id="ctl00_Content_Main_RLB_PlayerStats"]/div/ul/li[{i}]/a'))
            time.sleep(2)

            datos_pagina_actual = []

            try:
                datos_pagina_actual = driver.find_element(By.CSS_SELECTOR, '#RG_PlayerRanking_Libero').text.split('\n')
            except:
                pass

            if not datos_pagina_actual:
                try:
                    datos_pagina_actual = driver.find_element(By.CSS_SELECTOR, '#RG_PlayerRanking_Wingspiker_m').text.split('\n')
                except:
                    pass

            if not datos_pagina_actual:
                try:
                    datos_pagina_actual = driver.find_element(By.CSS_SELECTOR, '#RG_PlayerRanking_Opposite').text.split('\n')
                except:
                    pass

            if not datos_pagina_actual:
                try:
                    datos_pagina_actual = driver.find_element(By.CSS_SELECTOR, '#RG_PlayerRanking_MiddleBlocker_m').text.split('\n')
                except:
                    pass

            if not datos_pagina_actual:
                try:
                    datos_pagina_actual = driver.find_element(By.CSS_SELECTOR, '#RG_PlayerRanking_Setter').text.split('\n')
                except:
                    pass

            datos_por_pagina[i] = datos_pagina_actual
            driver.back()
            time.sleep(2)
            driver.get(url)

        print('Scraping exitoso')
        return datos_por_pagina

    elif parametro == 'clasificacion':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#tournament-table-tabs-and-content'))
        )
        clas = driver.find_element(By.XPATH,'//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div/div/div[2]').text.split('\n')
        print('Scraping exitoso')
        return clas

    elif parametro == 'estadistica_equipo':
        hacer_clic(driver, (By.XPATH, '//*[@id="RTS_Statistics_StatsType"]/div/ul/li[2]/a/span/span/span'))
        time.sleep(2)
        clas = driver.find_element(By.CSS_SELECTOR, '#RG_Stats_Recap').text.split('\n')
        print('Scraping exitoso')
        return clas
    
    else:
        print('algo anda mal')
    


def scraping_jornadas(url):
    opciones = Options()
    opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
    opciones.add_experimental_option('useAutomationExtension', False)
    opciones.add_argument('--incognito')
    opciones.add_argument('--start-maximized')
   
    driver = webdriver.Chrome(options=opciones)
    driver.get(url)

    hacer_clic(driver,(By.XPATH, '//*[@id="jornadas"]'))
    hacer_clic(driver, (By.XPATH, '//*[@id="jornadas"]/option[1]'))
    print(2)
    data = driver.find_element(By.XPATH, '//*[@id="CPContenido_rptPlugins_PanPlugin_0"]/div').text.split('\n')[52:]
 

    jornadas = []
    for i in data:
        if 'JORNADA' in i:
            temp = []
            temp.append(i)
            jornadas.append(temp)
        else:
            temp.append(i)

    dataframes_por_jornada = {}

    for jornada in jornadas:
        fechas = []
        horas = []
        enfrentamientos = []

        for i in range(1, len(jornada), 4):
            fecha = jornada[i + 1]
            hora = jornada[i + 2]
            enfrentamiento = jornada[i + 3]

            fechas.append(fecha)
            horas.append(hora)
            enfrentamientos.append(enfrentamiento)

        df = pd.DataFrame({'fecha': fechas, 'hora': horas, 'enfrentamiento': enfrentamientos})

        num_jornada = int(jornada[0].split()[-1])

        dataframes_por_jornada[num_jornada] = df

    
    df_final = pd.concat(dataframes_por_jornada.values(), ignore_index=True)

    print('Scraping exitoso')
    return df_final


        













