import sys
site="carsoupdotcom"

lines = open('carsoupcom_07012017_20001_temp.csv', 'r').readlines()

lines_set = set(lines)

out  = open('carsoupcom_07012017_20001_draft2XX.csv', 'w')

oldkey=-1
newkey=0

linekey={}


for line in lines_set:
    newkey=int(line.split(',')[0])

    if newkey not in linekey.keys():
    	out.write(site+","+line)
    	linekey[newkey]=line
    else:
        print(line)
        print(linekey[newkey])
        if line==linekey[newkey]:
            print("yes")

out.close()
