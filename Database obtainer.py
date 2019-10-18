# Not functional without a coder
import time
import os
import csv
import base64
import fnmatch
import pytesseract
from PIL import Image 
from pdf2image import convert_from_path
import fnmatch
from bs4 import BeautifulSoup as soup
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = False

def captcha():
    elem = driver.find_element_by_id('captchaEpicImg')
    loc  = elem.location
    size = elem.size
    left  = loc['x']+30
    top   = loc['y']+70
    width = size['width']+10
    height = size['height']+10
    box = (int(left), int(top), int(left+width), int(top+height))
    screenshot = driver.get_screenshot_as_base64()
    img = Image.open(BytesIO(base64.b64decode(screenshot)))
    area1 = img.crop(box)
    area=area1.convert('L')
    captchakey=pytesseract.image_to_string(area, lang='eng')
    captchafill=driver.find_element_by_id("txtEpicCaptcha")
    captchafill.send_keys(captchakey)
    time.sleep(1)
    search=driver.find_element_by_id("btnEpicSubmit")
    search.click()
    time.sleep(3)
    wrongcaptcha=driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div[2]/form/fieldset/div[3]/div/div[2]/div/span")
    if wrongcaptcha.text=="Wrong Captcha":
        captchafill.clear()
        captcha()
    else:
        pass

temppath=r"C:\Users\mishr\Desktop\JUPYTER DATA\temp"

csvcount=0
csvnamelist=[]
for file in os.listdir(temppath):
    if fnmatch.fnmatch(file, '*.csv'):
        print("CSV for execution : ",file)
        csvcount+=1
        csvnamelist.append(file)
print("Total files : ",csvcount)
time.sleep(1)
majorlist=[]
for i in csvnamelist:
    with open(temppath+"\\"+i, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            majorlist.append(row)
        csvFile.close()
    for j in range(len(majorlist)):
        majorlist[j]="".join(majorlist[j])
    print("Starting Main CSV creation")
    filename = temppath+"\\"+i+".csv"
    f = open(filename, "w")
    headers = "EPIC_No., Name, Age, Father's/Husband's Name,State, District, Polling Station, Assembly Constituency, Parliamentary Constituency\n"
    f.write(headers)
    f.close()
    for w in majorlist:
        driver = webdriver.Chrome(executable_path=temppath+"\\chromedriver.exe")
        driver.get("website") #enter website here
        continuel=driver.find_element_by_id("continue")
        continuel.click()
        epictabs=driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/ul/li[2]")
        epictabs.click()
        time.sleep(1)
        f = open(filename, "a")
        epicno=driver.find_element_by_xpath('//*[@id="name"]')
        epicno.clear()
        epicno.send_keys(w)
        select = Select(driver.find_element_by_id("epicStateList"))
        select.select_by_visible_text("Maharashtra")
        captcha()
        time.sleep(1)
        elements=driver.find_elements_by_class_name('ng-binding')
        Epic=elements[75].text
        temp=elements[76].text.replace("\n"," ")
        temp=temp.split()
        temp=temp[:3]
        Name="".join(temp)
        Age=elements[78].text
        v=elements[79].text.replace("\n"," ")
        v=v.split()
        v=v[:2]
        Father=" ".join(v)
        State=elements[81].text
        District=elements[82].text
        ps=elements[83].text
        ac=elements[84].text
        pc=elements[85].text
        f.write('"' + Epic + '","' + Name + '","' + Age + '","' + Father + '","' + State + '","' + District + '","' + ps + '","' + ac + '","' + pc + '"\n')
        print("Data extracted for : ", w)
        time.sleep(2)
        driver.close()
        f.close()

    

i