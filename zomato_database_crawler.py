# -*- coding: cp1252 -*-
# 2014 ©Jayant Jaiswal. All rights reserved. 
#This is for the Zomato database and not the reviews

from selenium import webdriver
import signal
import time
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def main_program():
    global country,city,city_name,link,city_val,driver,chromedriver
    country=city=city_name=link=''
    city_val=0
    chromedriver = "F:\Tools\chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    #driver = webdriver.Firefox()

    f=open("toStartWith.txt","r")
    l=f.readlines()
    f.close()
    for i in xrange(len(l)):
        l[i]=l[i].strip()
    print l

    highlights=["Home Delivery","Takeaway","Seating","Dine-In","Non Veg","Alcohol","Air Conditioned","Wifi"]


    print "\nOpening Country's.txt file...\n"   #Opening File
    f=open("Country's.txt","r")
    countrys=f.readlines()
    f.close()
    z=0
    print "\nFile Closed ...\n"                 #File Closed
    for country in countrys:
        country=country.strip()
        if z==1:
            l[0]=country
        if country!=l[0]:
            continue
        else:
            z=1
        print "\n\nOpening",country," ...\n\n"      #Opening Country
        f=open(r"C:\Users\Jayant\Desktop\Tomato\Country's\\"+country+".txt","r")
        cities=f.readlines()
        f.close()
        if not os.path.exists(r"C:\Users\Jayant\Desktop\Tomato\Country's\\"+country):
            os.makedirs(r"C:\Users\Jayant\Desktop\Tomato\Country's\\"+country)
        print "\n\nCrawling",country," ................\n\n"    #Crawling Countries
        y=0
        for city in cities:
            city=city.strip()
            if y==1:
                l[1]=city
            if city!=l[1]:
                continue
            else:
                y=1
            print "**************Getting",city,"************"
            try:
                c=2
                driver.get(city)
                c=1
                element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"location_pretext")))
            except SystemExit:
                sys_exit()
            except:
                if c==2:
                    print "\n_______________Memory Eaten Up..... Closing the Driver______________\n"
                    driver.quit()
                    time.sleep(1)
                    print "\n_______________Starting Again_____________________\n"
                    chromedriver = "F:\Tools\chromedriver"
                    os.environ["webdriver.chrome.driver"] = chromedriver
                    driver = webdriver.Chrome(chromedriver)
                    #driver = webdriver.Firefox()
                    driver.get(city)
                elif c==1:
                    while c==1:
                        try:
                            driver.get(city)
                            element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"location_pretext")))
                            c=0
                            print "\n\nReconnected...\n\n"
                        except:
                            print "Network Error... Trying to Reconnect..."
            print "****************Got",city,"*********************"
            try:
                city_name=str(driver.find_element_by_xpath("//span[@class='location_input_sp']").text).strip()
            except:
                city_name="NA"
            
            print "\n\nFetching Links of Restaurants for",city_name," ......\n\n"   #Fetching Links
            c=1
            try:
                driver.find_element_by_id("search_button").click()                  #Thought of the changes
                print ">>>>>>>>>>>>Jayant Jaiswal<<<<<<<<<<<<<<<<"
                element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"search_button")))
                c=2
            except SystemExit:
                sys_exit()
            except:
                while c==1:
                    try:
                        driver.get(city)
                    except:
                        print "\n_______________Memory Eaten Up..... Closing the Driver______________\n"
                        driver.quit()
                        time.sleep(1)
                        print "\n_______________Starting Again_____________________\n"
                        chromedriver = "F:\Tools\chromedriver"
                        os.environ["webdriver.chrome.driver"] = chromedriver
                        driver = webdriver.Chrome(chromedriver)
                        #driver = webdriver.Firefox()
                    try:
                        element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"search_button")))
                        c=0
                    except:
                        print "***********Trying to click the SEARCH Button for",city_name,"*************"
            #driver.find_element_by_id("search_button").click()
            if c!=2:
                driver.find_element_by_id("search_button").click()
            print driver.current_url
            #print c
            print "******Search Button Clicked for",city_name,"*************"
            print driver.current_url
            time.sleep(5)
            #os.makedirs(r"C:\Users\Jayant\Desktop\Zomato\Country's\\"+country+"\\"+city_name)
            if not os.path.exists(r"C:\Users\Jayant\Desktop\Tomato\Country's\\"+country+"\\"+city_name+".txt"):
                l[4]='0'
            if l[4]=='0':
                city_val=0
                f=open(r"C:\Users\Jayant\Desktop\Tomato\Country's\\"+country+"\\"+city_name+".txt","w")
                try:
                    page=str(driver.find_element_by_xpath("//div[@class='col-l-3 mtop0 alpha tmargin pagination-number']/div").text).split()
                except:
                    print "***********Total Pages Cannot be Determined***********"
                    page="0"
                pg=int(page[-1])
                print pg
                url=str(driver.current_url)+'?page='
                for i in xrange(1,pg+1):
                    c=1
                    try:
                        c=2
                        driver.get(url+str(i))
                        c=1
                        element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"location_pretext")))
                    except SystemExit:
                        sys_exit()
                    except:
                        if c==2:
                            print "\n_______________Memory Eaten Up..... Closing the Driver______________\n"
                            driver.quit()
                            time.sleep(1)
                            print "\n_______________Starting Again_____________________\n"
                            chromedriver = "F:\Tools\chromedriver"
                            os.environ["webdriver.chrome.driver"] = chromedriver
                            driver = webdriver.Chrome(chromedriver)
                            #driver = webdriver.Firefox()
                            driver.get(url+str(i))
                        elif c==1:
                            while c==1:
                                try:
                                    driver.get(url+str(i))
                                    element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"location_pretext")))
                                    c=0
                                    print "\n\nReconnected...\n\n"
                                except:
                                    print "Network Error... Trying to Reconnect..."
                    try:
                        elem = driver.find_elements_by_class_name("result-title")
                    except:
                        print "*********Restaurant Title Not Found**********"
                    try:
                        addr = driver.find_elements_by_class_name("search-result-address")
                    except:
                        print "*********Restaurant Address Not Found**********"
                    print "Crawling Page...........",i,"of",city
                    for j in xrange(len(elem)):
                        print elem[j].text
                        print >>f,elem[j].get_attribute("href")
                        print addr[j].text
                    print '\n\n'
                f.close()
            city_val=1
            print "\n\nLinks Fetched for Restaurants of",city_name,"...... Files Closed\n\n"      #Files Closed
            print "Crawling of restaurants of",city_name,"begins....\n\n"
            f=open(r"C:\Users\Jayant\Desktop\Tomato\Country's\\"+country+"\\"+city_name+".txt","r")
            links=f.readlines()
            f.close()
            for i in xrange(len(links)):
                links[i]=links[i].strip()
                link=links[i]
                c=1
                try:
                    c=2
                    driver.get(links[i])
                    c=1
                    element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"location_pretext")))
                except SystemExit:
                    sys_exit()
                except:
                    if c==2:
                        print "\n_______________Memory Eaten Up..... Closing the Driver______________\n"
                        driver.quit()
                        time.sleep(1)
                        print "\n_______________Starting Again_____________________\n"
                        chromedriver = "F:\Tools\chromedriver"
                        os.environ["webdriver.chrome.driver"] = chromedriver
                        driver = webdriver.Chrome(chromedriver)
                        #driver = webdriver.Firefox()
                        driver.get(links[i])
                    elif c==1:
                        while c==1:
                            try:
                                driver.get(links[i])
                                element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"location_pretext")))
                                c=0
                                print "\n\nReconnected...\n\n"
                            except:
                                print "Network Error... Trying to Reconnect..."
                try:
                    res_name=str(driver.find_element_by_xpath("//span[@itemprop='name']").text).strip()
                except:
                    res_name="NA"
                print "\nCrawling Restaurant",res_name,"of City",city_name,"in",country,".......\n"     #Crawling Restaurants
                try:
                    res_rate = str(driver.find_element_by_xpath("//div[@itemprop='ratingValue']").text)
                except:
                    res_rate="NA"
                try:
                    res_id=str(driver.find_element_by_xpath("//div[@itemprop='ratingValue']").get_attribute("data-res-id"))
                except:
                    res_id="NA"
                try:
                    res_add=str(driver.find_element_by_xpath("//div[@class='res-main-address-text']").text)
                except:
                    res_add="NA"
                try:
                    res_location = str(driver.find_element_by_class_name("resmap-img").get_attribute("style").split('|')[2])
                    lat=res_location.split(',')[0]
                    lon=res_location.split(',')[1]
                except:
                    lat="NA"
                    lon="NA"
                try:
                    res_pop_rev=driver.find_elements_by_xpath("//span[@class='grey-text']")
                    if len(res_pop_rev)==2:
                        res_pop_rev=str(res_pop_rev[0].text.strip())
                        res_all_rev=str(driver.find_elements_by_xpath("//span[@class='grey-text']")[1].text.strip())
                    else:
                        res_all_rev=str(res_pop_rev[0].text.strip())
                        res_pop_rev="0"
                except:
                    res_pop_rev="0"
                    res_all_rev="0"
                try:
                    res_votes=str(driver.find_elements_by_xpath("//span[@itemprop='ratingCount']")[0].text.strip())                         #Just Print
                except:
                    res_votes="0"
                try:
                    res_feat=str(driver.find_element_by_xpath("//*[@id='mainframe']/div[1]/div/div[1]/div[2]/div/span[2]").text).strip()
                    if res_feat.split()[-1]=="Collections":
                        res_feat=res_feat[12:-12]
                    else:
                        res_feat=res_feat[12:-11]
                except:
                    res_feat="NA"
                try:
                    res_cost=str(dr.find_element_by_xpath("//*[@id='mainframe']/div[1]/div/div[1]/div[3]/div[8]/div[2]/span[2]").text).strip()
                except:
                    res_cost="NA"
                try:
                    res_estb_type=str(driver.find_element_by_xpath("//*[@id='mainframe']/div[1]/div/div[1]/div[3]/div[2]/div/div/a").text).strip()
                except:
                    res_estb_type="NA"
                try:
                    res_known=str(driver.find_element_by_xpath("//*[@id='mainframe']/div[1]/div/div[1]/div[3]/div[3]/div/div[2]").text).strip()
                except:
                    res_known="NA"
                try:
                    res_shud_order=str(driver.find_element_by_xpath('//*[@id="mainframe"]/div[1]/div/div[1]/div[3]/div[4]/div/div[2]').text).strip()
                except:
                    res_shud_order="NA"
                try:
                    res_cuisines=driver.find_elements_by_xpath("//a[@itemprop='servesCuisine']")                                        #List
                except:
                    res_cuisines="NA"
                try:
                    res_highlights=driver.find_elements_by_class_name("res-info-feature-text")                                          #List
                except:
                    res_highlights="NA"
                try:
                    res_cost=driver.find_elements_by_xpath("//span[@itemprop='priceRange']")[0].text.partition("for")[0].strip()        #Just Print
                except:
                    res_cost="NA"
                res_high=['No']*7
                for i in res_highlights:
                    i=str(i.text)
                    if ("Home Delivery" in i) and (('No' not in i) and ('Not' not in i)):
                        res_high[0]='Yes'
                    elif ("Takeaway" in i) and (('No' not in i) and ('Not' not in i)):
                        res_high[1]='Yes'
                    elif (("Seating" in i) or ("Dine-In" in i)) and (('No' not in i) and ('Not' not in i)):
                        res_high[2]='Yes'
                    elif ("Non Veg" in i) and (('No ' not in i) and ('Not' not in i)):
                        res_high[3]='Yes'
                    elif (("Alcohol" in i) or ("Bar" in i)) and (('No' not in i) and ('Not' not in i)):
                        res_high[4]='Yes'
                    elif ("Air Conditioned" in i) and (('No' not in i) and ('Not' not in i)):
                        res_high[5]='Yes'
                    elif ("Wifi" in i) and (('No' not in i) and ('Not' not in i)):
                        res_high[6]='Yes'

                cuis=''

                for i in res_cuisines:
                    cuis=cuis+str(i.text.strip())+", "
                cuis=cuis[:-2]
                with open("Tomato_db.csv","ab") as c:
                    f=csv.writer(c)
                    a=[res_name,res_id,res_add,res_rate,str(city_name.strip()),str(country.strip()),lat,lon,res_votes,res_feat,res_cost,res_estb_type,res_known,res_shud_order,res_pop_rev,res_all_rev]+res_high+[cuis]
                    f.writerow(a)
                f=open("Cuisines.txt","a")
                print >>f,cuis
                f.close()

                print "\nSaved the database for",res_name," ......\n"
    driver.quit()
            




def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            f=open("toStartWith.txt","w")
            print >>f,country
            print >>f,city
            print >>f,city_name
            print >>f,link
            print >>f,city_val
            f.close()
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        f=open("toStartWith.txt","w")
        print >>f,country
        print >>f,city
        print >>f,city_name
        print >>f,link
        print >>f,city_val
        f.close()
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)

def sys_exit():
    driver.quit()
    sys.exit(1)


# store the original SIGINT handler
original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)
main_program()
