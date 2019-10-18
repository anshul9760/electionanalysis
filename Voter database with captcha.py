# Importing Libraries 
import os
import time
import shutil
import base64
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup as soup
from io import BytesIO
from selenium import webdriver
from pytesseract import image_to_string
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


options = Options()
options.headless = False


download_dir = # Enter directory # Change accordingly

profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
               "download.default_directory": download_dir , "download.extensions_to_open": "applications/pdf"}  #For pdf downloading
options.add_experimental_option("prefs", profile)  # Optional argument, if not specified will search path.
driver = webdriver.Chrome(options=options)



driver.get("websites with captchas")   #selected URLs
page = driver.page_source
pagesource = soup(page)
district=[]   # district array
dist=pagesource.find_all('select', {"name": "ctl00$Content$DistrictList"})
district=dist[0].find_all('option')


listofdistricts=[]
for i in range(1,len(district)):
    listofdistricts.append(district[i].text)



def captcha():
    elem = driver.find_elements_by_tag_name('img')
    elem[1]
    loc  = elem[1].location
    size = elem[1].size
    left  = loc['x']+95
    top   = loc['y']+78
    width = size['width']
    height = size['height']
    box = (int(left), int(top), int(left+width-20), int(top+height))
    screenshot = driver.get_screenshot_as_base64()
    img = Image.open(BytesIO(base64.b64decode(screenshot)))
    area = img.crop(box)
    image_file = area.convert('L')
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    keys = pytesseract.image_to_string(image_file, lang = 'eng')
    capbox=driver.find_element_by_name("ctl00$Content$txtcaptcha")
    capbox.send_keys(keys)
    submit = driver.find_element_by_name("ctl00$Content$OpenButton")
    submit.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 's')
    time.sleep(10)
    if os.path.isfile("W:\\Zenk\\ViewPDF.aspx") is False:
        time.sleep(3)
        refresh = driver.find_element_by_id("uu")
        refresh.click()
        select = Select(driver.find_element_by_name("ctl00$Content$DistrictList"))
        select.select_by_visible_text(i)
        select = Select(driver.find_element_by_name("ctl00$Content$AssemblyList"))
        select.select_by_visible_text(j)
        select = Select(driver.find_element_by_name("ctl00$Content$PartList"))
        select.select_by_visible_text(partlk[k].text)
        captcha()
    else:
        time.sleep(10)
        shutil.move('W:\\Zenk\\ViewPDF.aspx','W:\\Zenk\\'+i+'\\'+j+'\\ViewPDF.aspx')
        os.rename('W:\\Zenk\\'+i+'\\'+j+'\\ViewPDF.aspx','W:\\Zenk\\'+i+'\\'+j+'\\'+partlk[k].text+'.pdf')
        print("File ",partlk[k].text,' saved successfully')
		
		
		
		
for i in listofdistricts:
    if os.path.isdir("W:\\Zenk\\"+i) is False : os.mkdir("W:\\Zenk\\"+i)
    select = Select(driver.find_element_by_name("ctl00$Content$DistrictList"))
    select.select_by_visible_text(i)
    page = driver.page_source
    pagesource = soup(page)
    assmb=[]
    asm=pagesource.find_all('select', {"name": "ctl00$Content$AssemblyList"})
    assmb=asm[0].find_all('option')
    tempassembly=[]
    for j in range(1,len(assmb)):
        tempassembly.append(assmb[j].text)
    for j in tempassembly:
        select = Select(driver.find_element_by_name("ctl00$Content$AssemblyList"))
        select.select_by_visible_text(j)
        page2 = driver.page_source
        pagesource2 = soup(page2)
        partlk=[]
        pt=pagesource2.find_all('select', {"name": "ctl00$Content$PartList"})
        partlk=pt[0].find_all('option')
        tp=[]
        if os.path.isdir("W:\\Zenk\\"+i+"\\"+j) is False : os.mkdir("W:\\Zenk\\"+i+"\\"+j)
        for k in range(1,len(partlk)):
            select = Select(driver.find_element_by_name("ctl00$Content$PartList"))
            select.select_by_visible_text(partlk[k].text)
            time.sleep(3)
            captcha()
            
		
		
