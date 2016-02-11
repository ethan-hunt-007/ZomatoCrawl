from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pythonds.basic.queue import Queue
import idlelib.PyShell as pyshel
import time,os,csv,sys,time,re

#Global variables
global url_q,path,wait,start_url,users_crawled

chromedriver = r'F:\Tools\chromedriver'

#Starting Url of a person in Kolkata
f=open('url_queue.txt','r')
start_url = f.readlines()
f.close()
#start_url = 'https://www.zomato.com/users/rajdeep-biswas-4638621'

#Path to the Directory for the data to be dumped
path = 'C:\Users\Jayant\Desktop\Tomato\Maps.Google.Com\Trajectory Mining\TryingNew\dust_bin'

'''#Declaring Driver
driver = webdriver.Chrome(chromedriver)

#Defining Wait time over driver
wait = WebDriverWait(driver,30)'''

#Declaring the URL Queue
url_q = Queue()
users_crawled = []



def define_driver():
	#Declaring Driver
	driver = webdriver.Chrome(chromedriver)
	#Defining Wait time over driver
	wait = WebDriverWait(driver,30)
	return driver,wait


def driver_get(driver,url):
	try:
		driver.get(url)
	except MemoryError,e:
		print "__________________Memory Eaten Up... Closing the driver__________________"
		driver.quit()
		time.sleep(2)
		driver = webdriver.Chrome(chromedriver)
		driver.get(url)
	except SystemExit:
		driver.quit()
		sys.exit(1)
	return driver


def crawl():
	global lis,bis,data1,data2,url,ratings,reviews,driver
	for uri in start_url:
		url_q.enqueue(uri.strip())
	driver,wait=define_driver()
	print "\n*****************Starting the CRAWL*********************************\n"
	while not url_q.isEmpty():
		url=url_q.dequeue()
		##Going to the Reviews Part of the page
		driver=driver_get(driver,url+'#reviews')

		print "\n************Waiting for the reviews page to load***********\n"
		while True:
			try:
				wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#reviews > div.s-title.mbot0.borderless')))
				break
			except:
				print "......Network Error....."
		print "\n************Reviews Page LOADED********************\n"


		##getting the user_id
		print "\n***************Fetching the user_ID********************\n"
		try:
			user_id=driver.find_element_by_xpath('//div[contains(@class,"follow")]').get_attribute('data-user-id')
		except:
			user_id=-1

		try:
			no_of_reviews=driver.find_element_by_xpath('//a[@data-tab="reviews"]').text
			no_of_reviews = re.findall('\d+',no_of_reviews)
			no_of_reviews = int(no_of_reviews[0])
		except:
			no_of_reviews=0

		if user_id in users_crawled or user_id==-1:
			print "\n__________User already CRAWLED________________\n"
			continue

		try:
			if driver.find_element_by_xpath('//div[contains(@class,"usr-location")]').text.strip()!='Kolkata':
				continue
		except:
			pass
		if no_of_reviews!=0:
			print "\n__________________New USER... Starting the crawl__________________\n"

			#Getting and Clicking the LOAD MORE button
			print "\n**********Clicking the LOAD_MORE button***********\n"
			try:
				load_more = driver.find_element_by_class_name('load-more')
				while True:
					try:
						s=wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'load-more')))
						load_more.click()
						time.sleep(2)
					except Exception,e:
						print "E1: ",str(e)
						break
			except Exception,e:
				print "E2 :",str(e)

			print "\n************ALL data LOADED****************\n"

			##Getting the reviews DIV block
			print "\n********Wait while we fetch Reviews and other data**********\n"
			try:
				elem=driver.find_elements_by_xpath('//*[@id="reviewFeed"]/div')
			except Exception,e:
				print str(e)

			##Getting the total review blocks
			g=elem[0].find_elements_by_xpath("//div[contains(@class,'rev-text')]")

			##Getting the reviews and ratings
			ratings = []
			reviews = []
			for block in g:
				rating = block.find_element_by_tag_name('div').get_attribute('aria-label')
				review = block.text
				if rating!=None:
					rating = rating.strip()
					if review not in reviews and review!='' and review!=' ':
						reviews.append(review)
						ratings.append(rating)

			##Getting ReviewId,RestaurantId,RestaurantName
			##RestaurantAddress and datetime
			lis = []
			bis = []
			for block in elem:
				rev_id = block.get_attribute('data-review_id')
				res_id = block.find_element_by_class_name('snippet__name').find_element_by_class_name('snippet__link').get_attribute('data-entity_id')
				res_name = block.find_element_by_class_name('snippet__name').text
				res_addr = block.find_element_by_class_name('snippet__location').text
				datetime = block.find_element_by_tag_name('time').get_attribute('datetime')
				if (rev_id,res_id) not in lis:
					lis.append([rev_id,res_id])
					bis.append([res_name,res_addr,datetime])
			data1=[]
			data2=[]
			for i in xrange(len(lis)):
				if lis[i] not in data1:
					data1.append(lis[i])
					data2.append(bis[i])

			##Getting other necessary details
			# no_of_reviews=driver.find_element_by_xpath('//a[@data-tab="reviews"]').text
			# no_of_reviews = re.findall('\d+',no_of_reviews)
			# no_of_reviews = int(no_of_reviews[0])
			# user_id=driver.find_element_by_xpath('//div[contains(@class,"follow")]').get_attribute('data-user-id')
			user_link = url
			user_name = driver.find_element_by_class_name('full-name').text
			print no_of_reviews,len(data1),len(ratings),len(reviews)
			print "\n********ALL data for %s fetched**************\n"%user_name

			## Pause for user intervention if the no. of reviews does not equal the list length
			if no_of_reviews!=len(data1) or no_of_reviews!=len(ratings) or no_of_reviews!=len(reviews):
				pyshel.main()



			print "\n**********Writing %s's data to the file************\n"%user_name
			with open(r'..\dust_bin\user_data.csv','ab') as c:
				f=csv.writer(c)
				f.writerow([user_id,user_name,user_link,no_of_reviews])
			with open(r'..\dust_bin\review_data.csv','ab') as c:
				f=csv.writer(c)
				for i in xrange(len(data1)):
					f.writerow([user_id]+data1[i]+map(lambda x:x.encode('utf-8'),data2[i])+[reviews[i].encode('utf-8')]+[ratings[i]])
			print "\n**********Data Written to file************\n"
			##Addding the crawled user
			users_crawled.append(user_id)
			print "\n************ User %s crawled **************\n"%user_name

		##Process to move to the user network
		driver.back()
		driver.back()


		print "\n************Fetching the Followers and Followings of %s************\n"%user_name
		try:
			driver_get(driver,url+'#network')
			s=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#network > div > div.s-title.mbot0.borderless')))
		except Exception,e:
			print str(e)

		#Getting and Clicking the LOAD MORE button
		try:
			load_more = driver.find_element_by_class_name('load-more')
			while True:
				try:
					s=wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'load-more')))
					load_more.click()
					time.sleep(2)
				except Exception,e:
					print "E1: ",str(e)
					break
		except Exception,e:
			print "E2 :",str(e)

		try:
			elem=driver.find_elements_by_class_name('snippet__link')
		except:
			print "\n_______NO Followers of %s__________\n"%user_name
			elem=[]
		for i in elem:
			url_q.enqueue(str(i.get_attribute('href')))
		print "\n*******Network Fetched... Beginning the next crawl************\n"
	driver.quit()
try:
	crawl()
except Exception,e:
	print str(e)
	f=open('url_queue.txt','w')
	print >>f,url
	while not url_q.isEmpty():
		print >>f,url_q.dequeue()
	f.close()
	driver.quit()

'''Clicking the LOAD MORE button
		c=1
		d=0
		a=0
		elem=driver.find_element_by_xpath('//*[@id="foodjourney"]/div[2]')
		while c==1:
			try:
				s=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="foodjourney"]/div[2]')))
				elem=driver.find_element_by_xpath('//*[@id="foodjourney"]/div[2]')
				if str(elem.text)=="":
					break
				elem.click()
			except Exception,e:
				if str(elem.text)=="":
					break
				print str(e)

			try:
				s=driver.find_element_by_xpath('//*[@id="nFeed"]/div[9]/div/div[2]/p[1]')
				c=0
			except:
				c=1
				if len(driver.find_elements_by_class_name('snippet__link'))==a:
					d+=1
					time.sleep(3)
				else:
					d=0
					a=len(driver.find_elements_by_class_name('snippet__link'))
				print d,
				if d>40:
					driver.refresh()
					d=0
					time.sleep(3)
		'''
