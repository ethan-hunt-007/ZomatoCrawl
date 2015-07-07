# -*- coding: cp1252 -*-
# 2014 ©Jayant Jaiswal. All rights reserved. 
#This is for crawling Zomato Reviews


from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



f=open(r"C:\Users\Jayant\Desktop\Tomato\Country's\India\Delhi NCR.txt","r")
l=f.readlines()
f.close()
for i in xrange(len(l)):
    l[i]=l[i].strip()


#driver = webdriver.Firefox()
chromedriver = "F:\Tools\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
for j in xrange(12,len(l)):
    driver.get(l[j])
    try:
        name = str(driver.find_element_by_xpath("//span[@itemprop='name']").text).strip()
    except:
        continue
    try:
        elem = driver.find_element_by_xpath("//div[@class='load-more']")
    except:
        continue
    try:
        rate = driver.find_element_by_xpath("//div[@itemprop='ratingValue']")
        rate=rate.text
        #print "Rate =",rate.text
    except:
        continue
        #print "Rate = NA"
    try:
        location = driver.find_element_by_class_name("resmap-img")
        loc=location.get_attribute("style")
        loc=loc.split('|')
        loc=loc[2]
        #print "Location is",loc[2]
    except:
        continue
        #print "Location is NA"
    try:
        rev_type=driver.find_elements_by_xpath("//span[@class='grey-text']")
        #print "Popular",rev_type[0].text
        #print "All",rev_type[1].text
    except:
        continue
        #print "NA"
    #cuisine=driver.find_element_by_class_name("pb2 res-info-cuisines clearfix").text
    #print "Cuisines",cuisine
    t=int(str(elem.text.split()[-1]))
    w=t
    while elem.is_displayed:
        elem.click()
        #time.sleep(2.5)
        print "Loaded",w
        try:
            elem = driver.find_element_by_xpath("//div[@class='load-more']")
        except:
            break
        w=w-5
    '''f=open(name+".txt","w")
    print >>f,"Location is",loc[2]
    print >>f,"Rate =",rate.text
    print >>f,"\n\n*********************The reviews are :- ****************************\n"'''
    for i in xrange(t+5):
        try:
            usr_id=driver.find_element_by_xpath("//*[@id="reviews-container"]/div[1]/div[3]/div[1]/div["+str(i+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/a")
            with open(usr_id+".csv","ab") as c:
                f=csv.writer(c)
                jay = driver.find_element_by_xpath("//div[@class='zs-following-list']/div["+str(i+1)+"]")
                rate = driver.find_element_by_xpath("//div[@class='zs-following-list']/div["+str(i+1)+"]/div[3]/div/div/div/div/div")
        print >>f,"Review",i
        print "Review",i
        print >>f,'\n'
        print >>f,"Rate = ",((int(rate.get_attribute("class")[-1:])+1)/2.0)
        print >>f,jay.text.encode('utf-8')
        print >>f,'\n'
    f.close()

driver.close()
