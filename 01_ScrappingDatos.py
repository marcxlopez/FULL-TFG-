from distutils.log import info
import time
import os
from datetime import datetime, timedelta
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

import urllib 
from urllib.parse import urlparse 
from urllib.parse import parse_qs


# Web scrapper for infinite scrolling page  SERGI
#PATH = "E:\chromedriver\chromedriver.exe"
#DATASETS_DIR = "E:\\DOCENCIA\\TFG Alumnos\\MARC LOPEZ\\REPOSITORIO\\data"
#DATASETS_RAW_DIR = f'{DATASETS_DIR}\\HotelesIBIZA'

#web scrapper MARC

PATH = r"C:\Users\marcl\Desktop\TFG\WEB SCRAPPING\webscrapping2\chromedriver.exe"
#DATASETS_DIR = r"C:\Users\\marcl\Desktop\TFG\GITHUB TFG\PREPROCESSING-TFG\data"
#DATASETS_RAW_DIR = f'{DATASETS_DIR}\\HotelesIBIZA2'######IR CAMBIANDO NUMERO 


OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("--start-maximized")

# A CONTINUACIÓN, ACCEDEMOS A CADA UNA DE ESAS URLS, PARA EXTRAER LA INFORMACIÓN NECESARIA
nombresHotel = []
estrellas = []
ratios = []
ratiosTexto = []
direcciones = []
ammenities = []
serviciosPrincipales = []
familias = []
lugaresInteres = []
transporte = []
tamanyoAlojamiento = []
mascotas = []
internet = []
aparcamiento = []
masHab = []
ocioInstalaciones = []
ocioCercanias = []
habitaciones = []
checkIn = []
checkOut = []
coordenadas = []
precios = []

# url = 'https://es.hoteles.com/search.do?destination-id=' + id_poblacio + '&q-check-in='+ check_in.strftime("%Y-%m-%d") +'&q-check-out=' + check_out.strftime("%Y-%m-%d") + '&q-rooms=' + str(hab) + '&q-room-0-adults=' + str(senior) + '&q-room-0-children=' + str(child) + '&sort-order=BEST_SELLER'
hab = 1
senior = 2
child = 0
id_poblacio = "1641629" 
check_in = datetime.strptime('2022-08-10', "%Y-%m-%d")
check_out = datetime.strptime('2022-08-11', "%Y-%m-%d")
check_Final = datetime.strptime('2022-08-31',"%Y-%m-%d")
sigo = True 

#empezamos bucle de dias 
while sigo == True:
    

    URL_BASE = "https://es.hoteles.com/search.do"
    parameters = {
        'destination-id': id_poblacio,
        'q-check-in':  check_in.strftime("%Y-%m-%d"),
        'q-check-out': check_out.strftime("%Y-%m-%d"),
        'q-rooms': hab,
        'q-room-0-adults': senior,
        'q-room-0-children': child,
        'f-price-max':170,
        'sort-order': 'BEST_SELLER'
    }
    
    url = URL_BASE + '?' + urllib.parse.urlencode(parameters)
    
    print('URL=>', url)
    
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=OPTIONS)
    driver.get(url)
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1
    
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        time.sleep(4)
        #CERRAMOS LAS COOKIES 
        element = driver.find_element_by_xpath("""/html/body/div[1]/div[2]/div[2]/button[2]""")
        #aceptarcook.click()
        driver.execute_script("arguments[0].click();", element)
        i += 1
        print('page number=>', i)
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        print('screen_height:', screen_height*i, 'scroll_height:', scroll_height)
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break
    
    
    # Extraer urls 
    # //ul/li/div/div/a
    
    urls = [ link.get_attribute('href') for link in driver.find_elements_by_xpath("//ul/li/div/div/a")]
    
    # for url in urls:
    #   print(url)
        
    for hotel in urls:
        # Abrimos el hotel
        driver.get(hotel)
    
        # Extraemos las coordenadas
        urlsGoogle = [link.get_attribute('src') for link in driver.find_elements_by_xpath('//*[@id="overview1"]/div[2]/section[1]/section/div/button/div/span/img')] 
        for url in urlsGoogle: 
            print("google-maps=>", url) 
            parsed_url = urlparse(url) 
            captured_value = parse_qs(parsed_url.query) 
            coords = captured_value.get("center")
            print("coordenadas=>", coords)
        coordenadas.append(coords)
    
        # Realizamos el scroll para poder obtener toda la información
        ## screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        ## driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        
        # EXTRAEMOS LA INFORMACIÓN NECESARIA DE CADA CAMPO
        ## CHECK - IN
        checkIn.append(check_in)
        
        ## CHECK - OUT
        checkOut.append(check_out)
        
        ## NOMBRE HOTEL
        try:
            nombresHotel.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[2]/div[1]/div[1]/h1').text)
        except:
            nombresHotel.append('')
        
        ## ESTRELLAS HOTEL
        try :
            estrellas.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[2]/div[1]/div[1]/button/span').text)
        except: 
            estrellas.append('')
        
    	## NOMBRE HOTEL
        try:
            precios.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[2]/div[2]/div[1]/div/div/span').text)
        except:
            precios.append('')
    		
        ## RATIO PUNTUACION
        try:
            ratios.append(driver.find_element_by_xpath('//*[@id="seoReviews4"]/div/div[1]/div/span[1]').text)
        except:
            ratios.append('')
        
        ## RATIO TEXTO
        try:
            ratiosTexto.append(driver.find_element_by_xpath('//*[@id="seoReviews4"]/div/div[1]/div/span[2]/span[1]').text)
        except:
            ratiosTexto.append('')
        
        ## DIRECCION
        try:
            direcciones.append(driver.find_element_by_xpath('//*[@id="overview1"]/div[2]/section[1]/section/div/div/div/span/span[2]').text)
        except:
            direcciones.append('')
        
        ## AMMENITIES
        try:
            ammenities.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[7]/div[1]/ul').text)
        except:
            ammenities.append('')
        
        ## SERVICIOS PRINCIPALES
        try:
            serviciosPrincipales.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[7]/div[2]/div/div[1]/ul').text)
        except:
            serviciosPrincipales.append('')
        
        ## PARA FAMILIAS 
        try:
            familias.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[7]/div[2]/div/div[2]/ul').text)
        except:
            familias.append('')
        
        ## LUGARES DE INTERÉS
        try:
            lugaresInteres.append(driver.find_element_by_xpath('//*[@id="location3"]/div/div[1]/div[1]/ul').text)
        except:
            lugaresInteres.append('')
        
        ## TRANSPORTE
        try:
            transporte.append(driver.find_element_by_xpath('//*[@id="location3"]/div/div[1]/div[1]/div').text)
        except:
            transporte.append('')
        
        try:
            tamanyoAlojamiento.append(driver.find_element_by_xpath('//*[@id="info5"]/section/div/ul[1]').text)
        except:
            tamanyoAlojamiento.append('')
            
        try:
            mascotas.append(driver.find_element_by_xpath('//*[@id="info5"]/section/div/ul[5]').text)
        except:
            mascotas.append('')
        
        try:
            internet.append(driver.find_element_by_xpath('//*[@id="info5"]/section/div/ul[6]').text)
        except:
            internet.append('')
        
        try:
            aparcamiento.append(driver.find_element_by_xpath('//*[@id="info5"]/section/div/ul[7]').text)
        except:
            aparcamiento.append('')
            
        try:
            masHab.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[10]/section[4]/section/div/ul[6]').text)
        except:
            masHab.append('')
        
        try:
            ocioInstalaciones.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[10]/section[5]/section/div/div[1]/ul[1]').text)
        except:
            ocioInstalaciones.append('')
        
        try:
            ocioCercanias.append(driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/section[10]/section[5]/section/div/div[1]/ul[2]').text)
        except:
            ocioCercanias.append('')
        
        ### >>>> FALTARIA AÑADIR MAS INFORMACIÓN <<<<<<
        try:
            # habitaciones.append(driver.find_element_by_xpath('//*[@id="roomsAndRates2"]/section/ul').text)
            habitaciones.append(driver.find_element(by=By.CLASS_NAME, value='_2sLoz1').text)
        except:
            habitaciones.append('')
             
    # CERRAMOS LA WEB
    driver.close()
    
    #SEGUIMOS CON EL BUCLE SUMANDO UN DIA A CHEKCIN Y CHECK OUT
    if (check_in < check_Final) :
        sigo = True 
        check_in = check_in + timedelta(days=1)
        check_out = check_out + timedelta(days=1)
    else :
        sigo = False
        

# AGREGAMOS TODA LA INFORMACIÓN EN UN DATA FRAME
dict = {'Hotel': nombresHotel, 'checkIn': checkIn, 'checkOut': checkOut, 
        'Estrellas': estrellas, 'Ratio': ratios, 
        'Ratio_descr': ratiosTexto, 'Direcciones': direcciones, "Ammenities":ammenities, 
        'Servicios_Principales':serviciosPrincipales, 'CaractFamilias':familias, 
        'lugaresInteres':lugaresInteres, 'Transporte':transporte, 'tamanyo': tamanyoAlojamiento, 
        'mascotas':mascotas, 'internet':internet,  'aparcamiento':aparcamiento, 
        'masHab':masHab, 'ocioInstalaciones':ocioInstalaciones, 'ocioCercanias':ocioCercanias, 
        'habitaciones':habitaciones, 'coordenadas':coordenadas, 'precio':precios} 

hoteles = pd.DataFrame(dict)

# Guardamos en csv los datos
#hoteles.to_csv(DATASETS_RAW_DIR + '.csv', sep = ";", decimal = ".")
hoteles.to_csv(r'C:\Users\marcl\Desktop\TFG\GITHUB TFG\data\HotelesIBIZA4.csv', sep=";", decimal = ".")
# Guardamos en formato de pickle
hoteles.to_pickle(r'C:\Users\marcl\Desktop\TFG\GITHUB TFG\data\HotelesIBIZA4.pkl')
