import xml.etree.ElementTree as ET
import requests
import numpy as np
from datetime import datetime,timezone,timedelta
from aaf_xml_mod import *
from aaf_func import *
from aaf_usersettings import *
from aaf_plotInterface import *
import fnmatch
import time
import os
import sys

def load_catalog():
   #os.rename('catalog.xml','catalog_old.xml')
   url = 'https://thredds.met.no/thredds/catalog/aromearcticlatest/archive/catalog.xml'
   resp = requests.get(url)
   with open('catalog.xml', 'wb') as f:
      f.write(resp.content)


   
def parseXML(xmlfile):

   # To check contents of xml file
   #parsetest(xmlfile)

   file_f,update_time = parse_archive(xmlfile)

   tree=ET.parse(xmlfile)
   root= tree.getroot()
   
   return file_f,update_time




def plotPrep(dods_file):#,forecasts,forecast_length):

   # Fetch Oden location from Linus' ftp  
   fetchOden()  

   filename = "https://thredds.met.no/thredds/dodsC/"+dods_file
   #filename = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/archive/arome_arctic_det_2_5km_20230301T09Z.nc"
   #filename = "../arome_arctic_det_2_5km_20230301T09Z.nc"

   # Prepare forecast maps 
   #MapPrep(filename)

   # Prepare point forecast
   PointPrepZ(filename)
 
   # Prepare forecast maps 
   #Plot T850hPa and Z500hPa with ice edge
   TZPrep(filename,Tpl=850,Zpl=500)
   #Plot T lowest model level and MSLP with ice edge
   print('ml')
   TZPrep(filename,Tml=65,Psl=1)
   #Plot precipitable water and MSLP with ice edge
   print('lw')
   TZPrep(filename,lwe=1,Psl=1)
   #Plot accumulated precipitation and MSLP with ice edge
   print('prec')
   TZPrep(filename,prec=1,Psl=1)
 
      




def main(when='later'):

   # Fetch user settings 
   BeginHour,BeginMin,EndHour,EndMin = FetchTime()


   old_time='2023-03-03T10:06:33Z'
   old_time=''
 
   try:
      while True:

         update=True
         now=datetime.now()

         if when=='now':
            interval_start=datetime.now()-timedelta(minutes = 10)
            interval_stop=datetime.now()+timedelta(minutes = 10)
         else:
            interval_start=todayAt(BeginHour,min=BeginMin)
            interval_stop =todayAt(EndHour,min=EndMin)


         # just for printing
         current_time = now.strftime("%H:%M:%S")
         print("Current Time =", current_time)
         start_time = interval_start.strftime("%H:%M:%S")  
         print("Start Time =", start_time)
     
         if now > interval_start and now < interval_stop:

            while update and now < interval_stop:

               # Load the latest catalogue 
               load_catalog()

               # Parse xml file and fetch filename for OPeNDAP
               forecast_file,update_time = parseXML('catalog.xml')

               print ('update time',update_time)
               print ('old time: ',old_time)

               # If there is a new file, break loop and plot. Return to main loop         
               if not fnmatch.fnmatch(update_time, old_time):
                   print ('no match!')
                   update=False
                   
                   # Send plot request when new data is available 
                   plotPrep(forecast_file)#,forecasts,forecast_length)

               old_time=update_time
               now=datetime.now()
               time.sleep(300)

         else:
            time.sleep(1800)  #30min
            #time.sleep(5)  #30min
   except KeyboardInterrupt:
      print('interrupted!')






if __name__ == "__main__":
  
   # calling main function
   if len(sys.argv)>1:
      print ((sys.argv[1]))
      if sys.argv[1]=='now':
         main(sys.argv[1])
      else: 
         print('not recognised argument, try "now"')
   else:
      print ('Run later')
      main()



