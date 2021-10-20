import csv
import datetime
import time

import pandas as pd
from selenium import webdriver

import json


#initializing the webdriver
driver = webdriver.Chrome(executable_path='C://Users//rmkmu//chromedriver//chromedriver.exe')
#Getting the website page
driver.get("https://covidtelangana.com")
driver.maximize_window()
time.sleep(2)
#clicking on the plasma tab webelement
plasma=driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[3]/div/button[2]').click()
time.sleep(2)
#xpath for the full page (eg: hosp name, ph#,direction, plasma count...etc)
Details=driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[2]/div[2]/div/div/div')
#length or count of the details variable
l=len(Details)
print(l)
#UT=Updated Time
#the below code from line 27 to 46 is to convert from updated time to linux timestamp
time_detail = {"time" : [], "T" : []}
def getUpdatedTimeStamp(UT):
    values = UT.split(" ")
    for val in  values:
        if (val.isdigit()):
            time_detail['time']=val
        elif (val == 'minutes'):
            time_detail['T'] = 0
        elif (val == 'hours'):
            time_detail['T'] = 1
        elif (val == 'months'):
            time_detail['T'] = 2

def convertedTimeStamp():
  if (time_detail['T']==0):
      return time.time()*1000 - float(time_detail['time'])*60*1000
  elif (time_detail['T']==1):
      return time.time()*1000- float(time_detail['time']) *60*60*1000
  else:
      return time.time()*1000 - float(time_detail['time']) *2629743*100

#from line 49 to 51 is to print df data with full rows and columns in the output console
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#outer list is for declaring the headers
# outer_list = [['Hospital_List','phoneNumber_list','Description_List', 'updated_time_list', 'Plasma_count']]
outer_list = []
time.sleep(2)
l=5
#for loop is used to get the details iteration
for i in range(l):
    Details_1=Details[i].text
    # print(Details_1)
    #line 62 for converting text data into list hence using str.splitlines
    a = str.splitlines(Details_1)
    # print(a)
    #line 65 - to create a empty inner list
    inner_list =[]
    #HN=hospital name
    #a[0] index is zero
    HN=a[0]
    #apppending is adding data to the list
    inner_list.append(HN)
    #PH=Phone number
    PH=a[1]
    inner_list.append(PH)
    #DS=Description(email & address)
    DS=a[2]+", "+a[3]
    inner_list.append(DS)
    #UT=updated time
    #line 80 & 81 calling above functions converting updated time to linux timestamp
    UT=a[5]
    getUpdatedTimeStamp(UT)
    lastTime = convertedTimeStamp()
    inner_list.append(lastTime)
    #PS=PlasmaCount
    # PS=a[6]+" "+a[7]+","+a[8]+" "+a[9]
    time.sleep(2)
    if len(a)==10:
        PS=a[6]+" "+a[7]+","+a[8]+" "+a[9]
    else:
        PS="No Plasma Details"
    inner_list.append(PS)
    outer_list.append(inner_list)
    # print(outer_list)
#creating a dataframe & declaring the headers
df = pd.DataFrame(outer_list, columns=['Hospital_List','phoneNumber_list','Description_List', 'updated_time_list', 'Plasma_count'])
# df=pd.DataFrame(outer_list)
# print(df)
#converting df to dictonary
dictionary = df.to_dict(orient="index")
# print(dictionary)
#converting dictonary to json string
jsonString = json.dumps(dictionary, indent=4)
print(jsonString)
driver.close()












