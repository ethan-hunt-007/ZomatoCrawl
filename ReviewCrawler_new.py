from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import csv



def script():
    #Get the chromedriver for chrome
    chromedriver = "C:\Chrome Driver\chromedriver"
    driver = webdriver.Chrome(chromedriver)

    #Describes an variable 'wait' which is used to wait for elements to load on a webpage
    wait = WebDriverWait(driver, 30)

    #Get all the links to crawl
    f = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato\Country's\India\Kolkata.txt","r")
    l = f.readlines()
    f.close()

    #Get our starting point
    f2 = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\BeginFrom.txt","r")
    m = f2.readline()
    b = m.split()
    f2.close()

    #Which link to start crawling from
    k = int(b[0])
    #Which review to start crawling from
    z = int(b[1])+1

    f2 = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\Not yet crawled.txt","r")
    v = f2.readlines()
    f2.close()

    #Store the current link and review being crawled
    storei=0
    storej=0

    i=0

    #Run a loop for each link to crawl
    #for i in range(c, len(l)):
    while k<11:
        i = int(v[k])

        if i==2592:
            print("\n\n\nALL REVIEWS DONE !!!!!\n\n\n")
            return
        
        l[i]=l[i].strip()

        storei = k
        storej = -1

        #Store the current link being crawled. Reviews is yet to be crawled
        f2 = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\BeginFrom.txt","w")
        f2.write(str(storei)+" "+str(storej))
        f2.close()
                

        #Get the url
        url = l[i]
        driver.get(url)

        time.sleep(3)

        #Restaurant Name
        restaurantName = wait.until(EC.presence_of_element_located((By.XPATH,"//h1[@class='res-name left']/a/span[@itemprop='name']")))
        rn = restaurantName.text.encode("utf8")

        time.sleep(3)

        try:
            m = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='no-review-section']/div")))
            with open("Kolkata_Reviews_DB_Edit.csv","ab") as c:
                f1=csv.writer(c)
                f1.writerow(("None", "None", "None", "None", rn, "None", "None"))
            print("\n\nNo Reviews yet  for  "+rn+"\n\n")
            k+=1
            continue
        except:
            time.sleep(3)
        
        #Get the 'All Reviews' Button and click on it
        pr = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-sort='reviews-dd']")))
        time.sleep(3)
        pr.click()
        
        #Get the 'Load More' Button
        try:
            elem = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='load-more']")))
        except:
            elem = 0

        #Get the total count of posts to load
        origCount = int(driver.find_element_by_xpath("//a[@data-sort='reviews-dd']/span[@class='grey-text']").text)

        #Temp Counter pertaining to the number of posts left to load
        count = origCount
        if elem > 0:
            #Load all Posts
            while elem.is_displayed():
                elem.click()
                #Get remaining count
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH,"//span[@class='zs-load-more-count']")))
                    count=int(driver.find_element_by_xpath("//span[@class='zs-load-more-count']").text)
                except:
                    break
                

        #Reviews Counter
        j=0
            

        #Run a loop from 0 to the total number of reviews
        for j in range(z, origCount):

            storej = j
    
            #User ID
            #When chrome crashes due to excessive data load, TimeOutException() first occurs here
            try:
                userId = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/a")))
                uid = userId.get_attribute("data-entity_id").encode('utf8')
                #userId = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/a")))
                #uid = userId.get_attribute("data-entity_id").encode('utf8')
            except:
                #userId = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/a")))
                #uid = userId.get_attribute("data-entity_id").encode('utf8')
                f10 = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\Not yet Crawled Revised.txt","a")
                f10.write("\n"+str(i))
                f10.close()
                break
                '''driver.close()
                print("\n\nTimeOut Exception has occured.....Control is now being handed to the main module")
                time.sleep(1)
                return'''
                '''print("\n\n\n"+str(i)+"NOT REVIEWED !!!!!!\n\n\n")
                f10 = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\Not yet crawled.txt","a")
                f10.write("\n"+str(i))
                f10.close()
                i+=1
                break'''

            try:
                #User Name    
                #userNm = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/a")))
                #unm = userNm.text.encode('utf8')
                userNm = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/a")))
                unm = userNm.text.encode('utf8')
            except:
                userNm = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[1]/a")))
                unm = userNm.text.encode('utf8')
                #print("Error -> User Name")

            try:
                #User Rating
                rate = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div/div/div")))
                #rate = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div/div/div")))
                rating = ((int(rate.get_attribute("class")[-1:])+1)/2.0)
            except:
                #print("Error -> Rating")
                rate = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div/div/div")))
                rating = ((int(rate.get_attribute("class")[-1:])+1)/2.0)

            #Date
            try:
                dateTime = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[2]/a/time")))
                #dateTime = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div[1]/div["+str(j+1)+"]/div[2]/div[2]/a/time")))
                d = str(dateTime.get_attribute("datetime")).replace(" ", "")[:-8]
            except:
                dateTime = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[2]/a/time")))
                d = str(dateTime.get_attribute("datetime")).replace(" ", "")[:-8]

            #Followers
            try:
                followers = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[2]")))
                #followers = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[2]")))
                f = str(followers.text)
            except:
                '''try:
                    followers = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[2]")))
                    f = str(followers.text)
                except:'''
                f = '0'

            #Restaurant reviews + Hidden Reviews
            try:
                reviews = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div")))
                #reviews = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div["+str(j+1)+"]/div[3]/div/div[1]/div")))
                rev = str(reviews.text.encode('utf8')).replace('Rated', '')
            except:
                reviews = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div")))
                rev = str(reviews.text.encode('utf8')).replace('Rated', '')

            if rev=="":
                try:
                    reviews = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div[1]")))
                    #reviews = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div[1]")))
                    rev = reviews.get_attribute('textContent').encode('utf8')
                    j = rev.replace('Rated', '')
                except:
                    reviews = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='reviews-container']/div[1]/div[3]/div/div/div[1]/div["+str(j+1)+"]/div[3]/div/div[1]/div[1]")))
                    rev = reviews.get_attribute('textContent').encode('utf8')
                    j = rev.replace('Rated', '')
                #Print the collected data out into a csv file(for hidden reviews)
                with open("Kolkata_Reviews_DB_Edit.csv","ab") as c:
                    f1=csv.writer(c)
                    f1.writerow((uid, unm, d, f, rn, rating, j.decode('utf8').encode('utf8')))

                f2 = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\BeginFrom.txt","w")
                f2.write(str(storei)+" "+str(storej))
                f2.close()
            else:
                #Print the collected data out into a csv file(for normal reviews)
                with open("Kolkata_Reviews_DB_Edit.csv","ab") as c:
                    f1=csv.writer(c)
                    f1.writerow((uid, unm, d, f, rn, rating, rev.decode('utf8').encode('utf8')))
            
            
            #Print the collected data out into a csv file(for normal reviews)
            with open("Kolkata_Reviews_DB_Edit.csv","ab") as c:
                f1=csv.writer(c)
                f1.writerow((uid, unm, d, f, rn, rating, rev.decode('utf8').encode('utf8')))

                f2 = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\BeginFrom.txt","w")
                f2.write(str(storei)+" "+str(storej))
                f2.close()

        #Reset review counter starting point
        z=0

        print "Reviews for "+rn+" is done....."+str(i)

        k+=1
            
        
    driver.close()



def main():
    #Keep looping the script module until all links have been crawled
    while True:
        '''f = open(r"C:\Users\user\Desktop\My Programs\Python Projects\Tomato - Kolkata Reviews\Not yet crawled.txt","r")
        m = f.readlines()
        k = len(m)
        c = int(m[k-1])

        if c<2592:
            break
        else:'''
        #Pausing for the computer to catch some breath
        print("\n\nThe Script will restart after one minute......")
        time.sleep(3)
        print("Script is now restarting....\n\n")
        time.sleep(1)
        script()
        '''try:
            script()
        except:
            print("\n\nUnable to restart script......Will try again after 2 minutes")
            time.sleep(3)
            print("Script is now restarting....\n\n")
            time.sleep(1)
            script()'''
            

main()
