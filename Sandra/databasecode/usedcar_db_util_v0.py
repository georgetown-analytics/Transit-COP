import psycopg2

# TODO data is entered as a flat table; no normalization has been performed on this version

#accessing database
# TODO when ported to AWS connect statement should be updated


#databaseName and creadentials
dbName = 'usedcarsflat'
dbhost = 'localhost'
dbuser = 'stinta'
dbpass = 'georgetown'

originalcsv="/home/stinta/Development/python/projects/gwdatasciencecapstone/usedCars/utils/finaldatatowranggle/cleanfile_negativemileage_fromDavid.csv"



def createAndPopulateUseCarTable():
	try:
		print("Connecting to database")
		connect_str = "dbname='"+ dbName +"' user='" + dbuser +"' host='"+ dbhost +\
			"' password='"+ dbpass + "'"
		
		print(connect_str)
		conn = psycopg2.connect(connect_str)
		cursor = conn.cursor()

		CREATE_USEDCARTABLE_QUERY="""CREATE TABLE carsoupdata (
			localid			integer,
			site			varchar(40) NOT NULL,
			car_id			integer CONSTRAINT firstkey PRIMARY KEY,
			car_description		varchar(40) ,
			car_make		varchar(40) NOT NULL,
			car_model		varchar(40) ,
			car_trim		varchar(40) ,
			car_year		integer NOT NULL,
			car_category		varchar(40),
			car_mileage		integer NOT NULL,
			car_price		integer NOT NULL,
			car_extColor		varchar(40),
			car_transmission	varchar(40),
			car_driveTrain   	varchar(10),
			car_vendor_city		varchar(40),
			car_vendor_state	varchar(40) NOT NULL,
			car_vendor_zip		integer,
			car_detail_link		varchar(300),
			car_img_link		varchar(300),
			car_engine		varchar(40) NOT NULL
		);"""
			
		print("Creating carsoupusedcar table")
		cursor.execute(CREATE_USEDCARTABLE_QUERY)
		print("... created!")

		print("populating from csv file")
		f = open(originalcsv,'r',encoding='utf-8')
		cursor.copy_from(f,'"carsoupdata"',sep=",")
		print("... finished copying data") 

		conn.commit()
		conn.close()

	except Exception as e:
		print("Error on connecting and creating table")
		print(e)
	

if __name__== "__main__":
		createAndPopulateUseCarTable()	
