from bs4 import BeautifulSoup
import requests
import re
import time
import random

file_header="car_id,car_descrip,car_make,car_model,car_trim,car_year,car_category,car_mileage,car_price,car_extColor,car_transmission,car_driveTrain,car_vendor,car_location,car_detail_link,car_img_link,car_engine"


carscomFileName = "carsoupcom_07012017_20001_11_Used"
htmlSource = "./CarSoup.com.html"



baseUrl="https://www.carsoup.com/"
carsFile = open("./"+carscomFileName+".csv",'w')
carsFile.write(file_header+"\n")

for pageNum in range(1305,1325):
	htmlSource="http://www.carsoup.com/for-sale/used/?radius=150&dosort=stdslr_asc%2Cdistance_asc&form_type=4%3ASummaryZip&maxprice=1000000&pagenum="+str(pageNum)
	r = requests.get(htmlSource)
	data = r.text
	soup = BeautifulSoup(data,'html.parser')

	for listing in soup.find_all('div',class_ ="grid srp-vehicle"):
		car_vehiMakeModel_line = listing.find('h2',class_="vehicleMakeModel")
		#print(car_vehiMakeModel_line)
		
		car_detail_link = baseUrl+str(car_vehiMakeModel_line.a['href'])
		#print(car_detail_link)
		car_details_link_list = car_detail_link.split('/')
		
		car_year = str(-1)
		car_make = str(-1)
		car_model = str(-1)
		car_id = str(-1)
		if len(car_details_link_list) >= 9 :
			car_year = str(car_details_link_list[6])
			car_make = str(car_details_link_list[7])
			car_model = str(car_details_link_list[8])
			car_id = str(car_details_link_list[9])
		
		#print("y",car_year)
		#print("ma",car_make)
		#print("mo",car_model)
		#print("id",car_id)

		car_img_link = str(-1)
		car_img_link_line = listing.find('a')
		if car_img_link_line is not None:
			car_img_link = car_img_link_line.img['data-src']
		#print(car_img_link)

		car_descrip = ""
	#	car_descrip_line = listing.find('div',itemprop='description')
	#	if car_descrip_line is not None:
	#		car_descrip = car_descrip_line.string.replace(',','')
		#print(car_descrip)
		
		car_price = str(-1)
		price_line = str(listing.find('span',class_='price').string)
		
		if (len(price_line) > 0):
			car_price = price_line.replace(',','').replace('$','')
		#print(car_price)


		car_mileage = str(-1)
		mileage_line_tag = listing.find('span',class_='mileage')
		if mileage_line_tag is not None:
			mileage_line = str(mileage_line_tag.string)
			if (len(mileage_line) > 2) :
				car_mileage = str(mileage_line.split()[0].strip().replace(',',''))
		#print(car_mileage)

		
		metainfo_items = listing.find_all('li')
		#print(metainfo_items[2])
		#print(metainfo_items[0].strong.string.split(':')[0])

		car_extColor = ""
		car_transmission = ""
		car_driveTrain = ""
		car_engine = ""
		if len(metainfo_items) > 4: 
			car_extColor = str(metainfo_items[0].string.strip())
			car_transmission = str(metainfo_items[2].string.strip())
			car_driveTrain = str(metainfo_items[1].string.strip())
			car_engine = str(metainfo_items[3].string.strip())

		#print('ext',car_extColor)
		#print('tr',car_transmission)
		#print('dt',car_driveTrain)
		#print('eng',car_engine)

		car_vendor = ""
		car_location = str(listing.find('span',itemprop="address").string.strip())
		#print(car_location)

		car_trim = str(-1)
		car_category = ""
		car_category_line = listing.find('span',class_='bold').contents
		if len(car_category_line) > 1:
			car_category = car_category_line[1].replace('\'','')
		#print(car_category)

		carsFile.write(car_id+","+car_descrip+","+car_make+","+car_model+","+car_trim+","+car_year+","+car_category+","+car_mileage+","+car_price+","+car_extColor+","+car_transmission+","+car_driveTrain+","+car_vendor+","+car_location+","+car_detail_link+","+car_img_link+","+car_engine+"\n")

	time.sleep(random.randint(60,150))
	print(pageNum,"...")
carsFile.close()
