import requests
from bs4 import BeautifulSoup
import time 
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.amazon.co.uk/Best-Sellers-Electronics-Photo-Headphones-Earphones/zgbs/electronics/4085731/ref=zg_bs_pg_2?_encoding=UTF8&pg=1')
#按下cookie_button
cookie_button=driver.find_element(By.ID,"sp-cc-accept")
cookie_button.click()
time.sleep(3)
 

list1=[]           
for j in range(1,3):
    driver.get('https://www.amazon.co.uk/Best-Sellers-Fashion-Mens-Fashion-Smartwatches/zgbs/fashion/14284664031/ref=zg_bs_pg_1?_encoding=UTF8&pg='+str(j)) 
    # scroll_step決定每次滾動的大小
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        scroll_step = 800
        for i in range(int(last_height/scroll_step)):
            driver.execute_script("window.scrollTo(0, {});".format(i * scroll_step))
            time.sleep(0.8)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(1)
    last_height = driver.execute_script("return document.body.scrollHeight")        
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    soup=BeautifulSoup(driver.page_source,'html.parser')
    item = soup.find('div',{'class':'p13n-gridRow _cDEzb_grid-row_3Cywl'})
    goods = item.find_all('div',{'id':'gridItemRoot'})
    for k in goods:
        a='https://www.amazon.co.uk/'+k.a.get("href")
        list1.append(a)
        


with open(r'/Users/wen-linchang/Desktop/amazon/smartwatch.csv','wt',newline='') as file:
    writer=csv.writer(file)
    for l in range(len(list1)):
        writer.writerow([str(l+1),list1[l]])
        
        

