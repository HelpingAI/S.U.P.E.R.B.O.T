# Import necessary packages
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import warnings
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import re

warnings.simplefilter("ignore")
url = "https://chat-app-b8c333.zapier.app/zapchat"
chrome_driver_path = 'C:\\Users\\hp\\Desktop\\DEVELOPER\\Projects\\Project 1\\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--log-level=3')
service = Service(chrome_driver_path)
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.get(url)
sleep(5)


File = open("C:\\Users\\hp\\Desktop\\DEVELOPER\\Projects\\Project 1\\Study.txt","w")
File.write("2")
File.close()

while True:
    Inputtttt = input("AI: ")
    try:
        driver.find_element(by=By.XPATH,value="/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/form/fieldset/textarea").send_keys(Inputtttt)
    except:
        driver.find_element(by=By.XPATH,value="/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/form/fieldset/textarea").send_keys(Inputtttt)

    sleep(1)
    try:
        driver.find_element(by=By.XPATH,value="/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/form/fieldset/button").click()
    except:
        driver.find_element(by=By.XPATH,value="/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/form/fieldset/button").click()

    sleep(10)
    File = open("C:\\Users\\hp\\Desktop\\DEVELOPER\\Projects\\Project 1\\Study.txt","r")
    Data = File.read()
    Data = str(Data)
    File.close()
    try:
        XpathValue = f'/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/div/div/div[{Data}]/div[2]/p'
        Text = driver.find_element(by=By.XPATH,value=XpathValue).text
        NewText = re.sub(r'\d+\s*','',Text)
        print(NewText)
        File = open("C:\\Users\\hp\\Desktop\\DEVELOPER\\Projects\\Project 1\\Study.txt","w")
        NewData = int(Data) + 1
        File.write(str(NewData))
        File.close()
    except Exception as e:
        print(e)
