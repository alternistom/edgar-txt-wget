from urllib.request import urlopen
import wget
import re
import os

fileDate = input("► Which day? Please input it YYYYMMDD format! ")

fileType = '13F-HR'

base_url = "https://www.sec.gov/Archives/edgar/daily-index/"
txtLink = 'https://www.sec.gov/Archives/'

yearUrl = fileDate[:4]
monthUrl = fileDate[4:-2]
dayUrl = fileDate[-2:]

if 1 <= int(monthUrl) <= 3:
    QTR = "QTR1"

if 4 <= int(monthUrl) <= 6:
    QTR = "QTR2"

if 7 <= int(monthUrl) <= 9:
    QTR = "QTR3"

if 10 <= int(monthUrl) <= 12:
    QTR = "QTR4"

lines = urlopen(str(base_url) + str(yearUrl) + "/" + str(QTR) + "/" + "company." + fileDate + ".idx", timeout = 4).read().decode('ascii').split("\n")

filingCounter = 0

fileTypeForDir = fileType.replace("/","-")

dirName = fileTypeForDir + "/" + str(yearUrl) + "/" + str(monthUrl) + "/" + str(dayUrl) + "/"

if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists") 

for line in lines:
    if " " + fileType + " " in line:

        edgarName = re.sub(r" " + str(fileType) + ".*","",line).replace(",","").replace("/","").strip()
        print(edgarName)
        edgarLink = line.strip().rsplit(" ", 1)[1]
        print(edgarLink)
        CIK = " ".join(line.split()).rsplit(" ", 4)[2]
        print(CIK)
        print("Now Downloading File!")
        print("")
        wget.download(txtLink + edgarLink, dirName + edgarName + ".txt")
        #CIKLink = CIK_search_url + str(CIK)
        #row = (edgarName + "," + CIK + "," + CIKLink + "," + fileType + "," + str(fileDate) + "," + edgarLink).split(",")
        #dailyfilings.append(row)
        print("")
        filingCounter += 1

if filingCounter != 0:
    print("I have downloaded " + str(filingCounter) + " filings for this date: " + str(fileDate))
else:
       print("No filings for this day!")

