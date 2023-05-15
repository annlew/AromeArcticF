from datetime import datetime,timezone
import numpy as np
#from aaf_usersettings import *
#from aaf_plot_mod import *
#import netCDF4
#import fnmatch
import time as timer
import netrc
import ftplib

def todayAt (hr, min=0, sec=0, micros=0):
   now = datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)


def PointIdx(latPoint,lonPoint,latGrid,lonGrid):

   abslat = np.abs(latGrid-latPoint)
   abslon = np.abs(lonGrid-lonPoint)
   c = np.maximum(abslon,abslat)
   y_idx, x_idx = np.where(c == np.min(c))

   return y_idx,x_idx

def ReadLoc(filename):
   lon=[]
   lat=[]
   f = open(filename,'r')
   pos =f.readlines()
   f.close()
   print('printpos')
   print(pos)
   print(pos[0])
   if len(pos)>1:
      print ('long')
      for locs in pos:
         print (locs)
         #lon.append,lat.append=str.split(locs)
         lont,latt=str.split(locs)
         lon.append(lont)  
         lat.append(latt)  
   else:
      #lon,lat=str.split(pos)
      lont,latt=str.split(pos[0])
      lon.append(lont)  
      lat.append(latt)  
 
   print (filename)
   print (lon)
   print (lat)
   #return float(lat),float(lon)
   return lat,lon









def fetchOden():

   filename = "Odenloc.txt"
   nnetrc = netrc.netrc()
   remoteHostName = "bolftp.ecmwf.int"
   authTokens = nnetrc.authenticators(remoteHostName)
   # Print the access tokens
   #print("Remote Host Name:%s" % (remoteHostName))
   ftp_server = ftplib.FTP(remoteHostName, authTokens[0],authTokens[2])
   ftp_server.cwd('/artofmelt/') 
   # Write file in binary mode
   with open(filename, "wb") as file:
     # Command for Downloading the file "RETR filename"
     ftp_server.retrbinary(f"RETR {filename}", file.write)
   ftp_server.quit()


