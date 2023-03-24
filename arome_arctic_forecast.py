import xml.etree.ElementTree as ET
import requests
import numpy as np
import netCDF4
import matplotlib.pylab as plt
from datetime import datetime,timezone
from aaf_plot_mod import *
from aaf_xml_mod import *
from aaf_func import *
from aaf_usersettings import *
import fnmatch
import os
import time

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
   
#   print('my root')
#   print(root)
#   print( len(root))
#   
#   print('root tag')
#   print(root.tag)
#   
#   print('root tags')
#   print(root.tag[:])
#   
#   print('root[0] and [1]')
#   print (root[0])
#   print (root[1])
#   
#   print('child tags')
#   # You can iterate over an element's children.
#   for child in root:
#       print('child.tag')
#       print(child.tag)
#       print('child.attrib')
#       print(child.attrib)
#   
#   for child in root:
#       print('child.text')
#       print(child.text)
#   
#   print ('root attributes')
#   print(root.attrib)
   



   return file_f,update_time




def plot_surface_pressure(dods_file,forecasts,forecast_length):

   filename = "https://thredds.met.no/thredds/dodsC/"+dods_file
   #filename = "https://thredds.met.no/thredds/dodsC/metpparchive/2021/08/01/met_analysis_1_0km_nordic_20210801T12Z.nc"
   #filename = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/archive/arome_arctic_det_2_5km_20230301T09Z.nc"
   filename = "../arome_arctic_det_2_5km_20230301T09Z.nc"

   ncfile   = netCDF4.Dataset(filename)
   
   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]
   x = ncfile.variables["x" ][:]
   y = ncfile.variables["y"][:]
   timestep  = ncfile.variables["time"][0:(forecasts+1)*forecast_length:forecast_length]

   # Fetch variables
   var_list=variable_list()
   
   var = np.empty((len(var_list),forecasts+1,len(y),len(x)))
   unit={} 
   long_name={} 
   print (var.shape)

   print(len(x))
   print(len(y))
   print(len(longitudes))
   print(len(longitudes))

   for i in range(len(var_list)):
      print (var_list[i])

      var[i,:,:,:] = ncfile.variables[var_list[i]][0:(forecasts+1)*forecast_length:forecast_length,0,:,:]
      unit[i] =  ncfile.variables[var_list[i]].units
      long_name[i] =  ncfile.variables[var_list[i]].long_name
      print (unit)


   ncfile.close()  

   print(len(latitudes))
   print(len(longitudes))
   #print(slp.shape)
   print (len(timestep))
 
   #fig, ax = define_figure(1,forecasts+1)
   #print(len(ax))
   #plot2(fig,ax,longitudes, latitudes, slp, timestep)


   plot_pw_rotated_grid_separate(longitudes,latitudes,var[0,:,:,:], timestep,forecasts+1,unit[0],long_name[0])
   plot_pw_rotated_grid_separate(longitudes,latitudes,var[1,:,:,:], timestep,forecasts+1,unit[1],long_name[1])
   #plot_pw_rotated_grid_separate(longitudes,latitudes,var[2,:,:,:], timestep,forecasts+1,unit[2],long_name[2])
      






def main():

   # Fetch user settings 
   forecasts, forecast_length = user_settings()
   i=0

   old_time='2023-03-03T10:06:33Z'
   old_time=''
   update=True
 
   try:
      #while True:
      while update:
        print('Hello',i)
        time.sleep(10)

    
        interval_start='10:00:00'
        interval_stop='10:30:00'
        FMT = '%H:%M:%S'

        now=datetime.now()
        
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        
        if now > datetime.strptime(interval_start,FMT) and now<datetime.strptime(interval_stop,FMT):
           print ('not late')
        else:
           print ('late')


#   except KeyboardInterrupt:
#    print('interrupted!')

   # Load the latest catalogue 
        load_catalog()


   # Parse xml file and fetch filename for OPeNDAP
        forecast_file,update_time = parseXML('catalog.xml')

        print ('update_time')
        print ('update_time')
        print ('update_time')
        print (update_time)

        print (old_time)

        if not fnmatch.fnmatch(update_time, old_time):
            print ('no match!')
            update=False

        old_time=update_time
        
        i=i+1
   except KeyboardInterrupt:
      print('interrupted!')

   # Plot field
   plot_surface_pressure(forecast_file,forecasts,forecast_length)


def main_test():

   # Fetch user settings 
   forecasts, forecast_length = user_settings()
   i=0


   old_time='2023-03-03T10:06:33Z'
   old_time=''
   interval_start=todayAt(13,min=18)
   interval_stop='18:50:00'


   FMT = '%H:%M:%S'
 
   try:
      while True:

         update=True
         now=datetime.now()
         current_time = now.strftime("%H:%M:%S")
         print("Current Time =", current_time)
         start_time = interval_start.strftime("%H:%M:%S")  
         print("Start Time =", start_time)

     
         if now > interval_start:
            print ('not late')


            while update:
               print('Hello',i)
               time.sleep(10)


               # Load the latest catalogue 
               load_catalog()


               # Parse xml file and fetch filename for OPeNDAP
               forecast_file,update_time = parseXML('catalog.xml')

               print ('update_time')
               print ('update_time')
               print ('update_time')
               print (update_time)

               print ('old time: ',old_time)

               if not fnmatch.fnmatch(update_time, old_time):
                   print ('no match!')
                   update=False

               old_time=update_time
        
               i=i+1

            plot_surface_pressure(forecast_file,forecasts,forecast_length)

         else:

            time.sleep(10)
   except KeyboardInterrupt:
      print('interrupted!')

   # Plot field
   #plot_surface_pressure(forecast_file,forecasts,forecast_length)




def main_dev_plot_test():

   # Fetch user settings 
   forecasts, forecast_length = user_settings()

   # Load the latest catalogue 
   #load_catalog()

   # Parse xml file and fetch filename for OPeNDAP
   forecast_file,update_time = parseXML('catalog.xml')

   # Plot field
   plot_surface_pressure(forecast_file,forecasts,forecast_length)


if __name__ == "__main__":
  
   # calling main function
   main_test()
   #main_dev_plot_test()



