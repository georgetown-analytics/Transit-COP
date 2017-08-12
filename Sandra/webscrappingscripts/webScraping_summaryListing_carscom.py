from bs4 import BeautifulSoup
import requests
import re
import time
import random


def extractValue(car_property):
	return car_property.split(':')[1].strip("\"")

file_header="site,car_id,car_descrip,car_make,car_model,car_trim,car_year,car_category,car_mileage,car_price,car_extColor,car_transmission,car_driveTrain,car_vendor,car_location,car_detail_link,car_img_link"

carscomFileName = "carsdotcom_06272017_02_20001_Used"
site = "carsDotCom"
baseUrl ="https://www.cars.com"
carsFile = open("./"+carscomFileName+".csv",'w')
carsFile.write(file_header+"\n")

for pageNum in range(18,51):
	htmlSource="https://www.cars.com/for-sale/searchresults.action/?page="+str(pageNum)+"&perPage=100&rd=150&searchSource=UTILITY&sort=distance-nearest&stkTypId=28881&zc=20001"
	r = requests.get(htmlSource)
	data = r.text
	soup = BeautifulSoup(data,'html.parser')

	for listing in soup.find_all('div',class_ ="shop-srp-listings__listing"):
		car_id = str(listing['id'].split('-')[1])
		car_detail_link = str(baseUrl+listing.a['href'])
		car_img_link = str(listing.img['src'])
		car_descrip = str(listing.img['alt'])
		
		car_price = str(-1)
		price_line_entry = listing.find('span',class_='listing-row__price')
		if price_line_entry is not None :
			price_line = price_line_entry.contents
			if (len(price_line) >= 2) :
				car_price = str(price_line[1].replace(',',''))


		car_mileage = str(-1)
		mileage_line_entry = listing.find('span',class_='listing-row__mileage')
		if mileage_line_entry is not None :
			mileage_line = mileage_line_entry.contents
			mileage_list = mileage_line[0].split(':')
			if (len(mileage_list) == 2) :
				car_mileage = str(mileage_list[1].strip().replace(',',''))

		
		metainfo_items = listing.find_all('span',class_='listing-row__meta-item')
		#print(metainfo_items[0].strong.string.split(':')[0])

		car_extColor = ""
		car_transmission = ""
		car_driveTrain = ""
		if len(metainfo_items) == 3: 
			car_extColor = str(metainfo_items[0].contents[1].strip())
			car_transmission = str(metainfo_items[1].contents[1].strip())
			car_driveTrain = str(metainfo_items[2].contents[1].strip())

		car_vendor = str((listing.find('a',class_='listing-row__dealer-name').contents)[0].strip())
		car_location = str(listing.find_all('span',class_="listing-row__distance")[1].contents[0].strip())

		det_list = listing.find('div',class_='listing-row__save').a['vehicle'].split(',')

		car_make = str(extractValue(det_list[2]))
		car_model = str(extractValue(det_list[4]))
		car_trim = str(extractValue(det_list[6]))
		car_year = str(extractValue(det_list[8]))
		car_category = str(extractValue(det_list[9]))

		carsFile.write(site+","+car_id+","+car_descrip+","+car_make+","+car_model+","+car_trim+","+car_year+","+car_category+","+car_mileage+","+car_price+","+car_extColor+","+car_transmission+","+car_driveTrain+","+car_vendor+","+car_location+","+car_detail_link+","+car_img_link+"\n")

	time.sleep(random.randint(45,70))	

carsFile.close()
