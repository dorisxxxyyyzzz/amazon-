from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time 
import csv
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


df=pd.read_csv('smartwatch (有標題的).csv')
a=df['Website'][0:10]
print(a)
for i in a:
    url=i
    
# url='https://www.amazon.co.uk/Sekonda-Monitor-Activity-Functions-1909/dp/B09FY4459M/ref=zg_bs_14284664031_sccl_2/258-3481884-2475716?psc=1'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    webpage=requests.get(url,headers=headers)
    soup=BeautifulSoup(webpage.text,'html.parser')
    driver = webdriver.Chrome()
    driver.get(url)
    
    
    cookie_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sp-cc-accept"))
    )
    cookie_button.click()
    driver.find_element(By.XPATH, '//*[@id="nav-global-location-slot"]').click()
    time.sleep(2)
    city = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdateInput"]')
    city.send_keys("E1 0AA")
    city.send_keys(Keys.ENTER)
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    
    # 滑動到下方評論區
    y = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="customer-reviews_feature_div"]'))
    )
     
    y = y.location["y"]
    driver.execute_script("window.scrollTo(0, {});".format(y))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="reviewsMedley"]/div/div[1]'))
    )
    
    
    # # 商品總分:
    商品總分=[]
    a=soup.find('span',{'class':'cr-widget-TitleRatingsAndHistogram'})
    try:
        Customer_reviews=a.find('span',class_='a-icon-alt').text
        商品總分.append(Customer_reviews)
    except:
        商品總分.append('No Customer reviews')
    
    
    
    # # 每級別評分占比: 
    每級別評分占比=[]  
    
    c=a.find_all('span',class_='a-declarative')
    starbox=[]   
    for i in c:
        ans=i.find_all('span',class_='a-size-base')
    for j in ans: 
        try:
            r=j.find('a').get('title')
            r=str(r)       
        except:
            r='0'
        starbox.append(r)    
    每級別評分占比.append(starbox[0::2])
    
    
                                  
    # # By feature
    # # 要判斷是否有see more
    
    By_feature=[]
    try:
        WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="cr-dp-summarization-attributes"]'))
            )

        try:
            driver.find_element(By.XPATH,'//*[@id="reviewsMedley"]/div/div[1]/span[2]')
            try: 
                driver.find_element(By.XPATH,'//*[@id="cr-summarization-attributes-list"]/div[4]/a/i').click()
            except:
                pass
            By_feature.append(driver.find_element(By.XPATH,'//*[@id="cr-dp-summarization-attributes"]').text)
        except:
            pass
            By_feature.append('No element')
    except:   
        pass
        By_feature.append('No By feature')
    
    
    # # Read reviews that mention
    
    tag_box=[]
    try:
        driver.find_element(By.XPATH,'//*[@id="cr-lighthut-1-"]/div')
        for i in range(1,16):
            y=str(i)
            x='//*[@id="cr-lighthut-1-"]/div/span['+ y +']'     
            tag_box.append(driver.find_element(By.XPATH,x).text)
        # print(tag_box)     
    except:
        pass 
        tag_box.append('No tag')
    
    
    
    
    # next page
    review_2023=[]     
    try:       
        see_all_reviews = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="reviews-medley-footer"]/div[2]/a'))
        )   
        see_all_reviews.click()    
        y = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="cm_cr-view_opt_sort_filter"]/div[1]/div[1]'))
        )
        
        y = y.location["y"]
        driver.execute_script("window.scrollTo(0, {});".format(y))
        
        sort_by = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="a-autoid-3-announce"]'))
        )
        sort_by.click()
        #選擇 Most recent 
        most_recent = driver.find_element(By.XPATH,'//*[@id="sort-order-dropdown_1"]')
        most_recent.click()
        
        filtera = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="a-autoid-4-announce"]'))
        )
        filtera.click()
        purchase = driver.find_element(By.XPATH,'//*[@id="reviewer-type-dropdown_1"]')
        purchase.click()
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="reviews-filter-info-segment"]'))
        )
        current_url = driver.current_url
        
            
        box1=[]
        box2=[] 
        box3=[]
        
        webpage=requests.get(current_url,headers=headers)
        soup=BeautifulSoup(webpage.text,'html.parser')
        # y = WebDriverWait(driver, 10).until(
        # EC.presence_of_element_located((By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]'))
        # ) 
        # y = y.location["y"]
        # driver.execute_script("window.scrollTo(0, {});".format(y))
        review_section = soup.find_all('div',{'class':'a-section review aok-relative'})
        while True:
            for k in review_section:
                date = k.find_all('span',{'class':'a-size-base a-color-secondary review-date'})
                for l in date:
                    box1.append(l.text)
            for i in review_section:
                review = i.find_all('span',{'class':'a-size-base review-text review-text-content'})
                for j in review:
                    box2.append(j.text)         
            zipped = zip(box1, box2)
            for item in zipped:
                for i in item:
                    ans = re.findall('.*(?=2023).*',i)
                    # print(ans)
                    box3.append(ans)
                    if ans != [] :
                        review_2023.append(item)
                        last_item=item
                        # print(item)
            # print(box3[-2][0])
            # print(last_item[0])
            if box3[-2][0] != last_item[0]:
                break
            y = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]'))
            )
            y = y.location["y"]
            driver.execute_script("window.scrollTo(0, {});".format(y))
            
            second_page = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]'))
            )  
            second_page.click()    
    except:
        pass
    
    
    a=每級別評分占比
    b=商品總分 
    c=By_feature
    s=' '
    d=tag_box
    st=' '

    # with open(r'C:\Users\Admin\Desktop\amazon\smartwatchall.csv','at',newline='') as file:
    
    with open(r'C:\Users\Admin\Desktop\amazon\smartwatchall.csv','at',newline='',encoding='UTF-8') as file:
      
        writer=csv.writer(file)        
        # writer.writerow([])
        try:
            for i in d:
                s=s+str(i)+','      
        except UnicodeEncodeError:
            pass 
            # writer.writerow([s])
        try:
            for j in review_2023:
                st=st+str(j)+',' 
        except :
            pass    
        writer.writerow([a,b,c,s,st])    

    














  


