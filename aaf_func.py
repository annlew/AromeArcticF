from datetime import datetime,timezone
import numpy as np
from aaf_usersettings import *
from aaf_plot_mod import *
import netCDF4
import fnmatch

# Short functions

def todayAt (hr, min=0, sec=0, micros=0):
   now = datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)


def PointIdx(latPoint,lonPoint,latGrid,lonGrid):

   abslat = np.abs(latGrid-latPoint)
   abslon = np.abs(lonGrid-lonPoint)
   c = np.maximum(abslon,abslat)
   y_idx, x_idx = np.where(c == np.min(c))

   return y_idx,x_idx   



# Plot prep functions

def TZPrep(ncfileName,**kwargs):
   Tpl = kwargs.get('Tpl', None)
   Zpl = kwargs.get('Zpl', None)
   Tml = kwargs.get('Tml', None)
   Psl = kwargs.get('Psl', None)
   lwe = kwargs.get('lwe', None)
   prec= kwargs.get('prec', None)

   # Fetch variables from user definitions for map plot

   if (Tpl!=None and Zpl!=None):
      var_list=VariableListTZMap()
   if (Tml != None and Psl != None):
      var_list=VariableListTPMap()
   if (lwe != None and Psl != None):
      var_list=VariableListPWMap()
   if (prec != None and Psl != None):
      var_list=VariableListPrecMap()

   #print (var_list)

   forecasts, forecast_length =ForecastSettings()

   ncfile   = netCDF4.Dataset(ncfileName)

   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]
   timestep  = ncfile.variables["time"][0:(forecasts+1)*forecast_length:forecast_length]

   v_idx=[]
   if Tml!=None:
      modellev  = ncfile.variables["hybrid"][:]
      #v_idx.append(np.where(modellev==Tml)[0])
      v_idx.append(Tml-1)
   if Tpl!=None or Zpl!=None:
      pressure  = ncfile.variables["pressure"][:]
      if Tpl!=None:
         v_idx.append(np.where(pressure==Tpl)[0])
      if Zpl!=None:
         v_idx.append(np.where(pressure==Zpl)[0])

   var = np.empty((len(var_list),forecasts+1,len(latitudes),len(latitudes[0])))
   unit={}
   long_name={}


   for i in range(len(var_list)):
      long_name[i] =  ncfile.variables[var_list[i]].long_name
      #print(long_name[i])
      if not fnmatch.fnmatch(long_name[i],'Sea_ice_fraction'):
         if not fnmatch.fnmatch(long_name[i],'Mean Sea Level Pressure (MSLP)') and v_idx:
            #print('nooo')
            var[i,:,:,:] = np.squeeze(ncfile.variables[var_list[i]][0:(forecasts+1)*forecast_length:forecast_length,v_idx[i],:,:])
            unit[i] =  ncfile.variables[var_list[i]].units
         else:
            #print('yees')
            var[i,:,:,:] = np.squeeze(ncfile.variables[var_list[i]][0:(forecasts+1)*forecast_length:forecast_length,:,:])
            unit[i] =  ncfile.variables[var_list[i]].units
      else:
         var[i,:,:,:] = np.squeeze(ncfile.variables[var_list[i]][0:(forecasts+1)*forecast_length:forecast_length,:,:])
         unit[i]=""
   ncfile.close()

   # Plot maps
   plot_TZ(longitudes,latitudes,var[:,:,:,:], timestep,forecasts+1,Tpl,Zpl,Tml,Psl,lwe,prec)


def MapPrep(ncfileName):

   # Fetch variables from user definitiona for map plot
   var_list=VariableListMap()
   forecasts, forecast_length =ForecastSettings()


   ncfile   = netCDF4.Dataset(ncfileName)

   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]
   timestep  = ncfile.variables["time"][0:(forecasts+1)*forecast_length:forecast_length]

   var = np.empty((len(var_list),forecasts+1,len(latitudes),len(latitudes[0])))
   unit={}
   long_name={}

   for i in range(len(var_list)):
      print (var_list[i])

      var[i,:,:,:] = ncfile.variables[var_list[i]][0:(forecasts+1)*forecast_length:forecast_length,0,:,:]
      long_name[i] =  ncfile.variables[var_list[i]].long_name
      if not fnmatch.fnmatch(long_name[i],'Sea_ice_fraction'):

         print (long_name[i])
         unit[i] =  ncfile.variables[var_list[i]].units
         print (unit)
      else:
         unit[i]=""
   ncfile.close()

   print (var.shape)

   # Plot maps
   #plot_pw_rotated_grid_separate(longitudes,latitudes,var[0,:,:,:], timestep,forecasts+1,unit[0],long_name[0])
   #plot_pw_rotated_grid_separate(longitudes,latitudes,var[1,:,:,:], timestep,forecasts+1,unit[1],long_name[1])
   plot_pw_rotated_grid_separate(longitudes,latitudes,var[2,:,:,:], timestep,forecasts+1,unit[2],long_name[2])



def PointPrep(ncfileName):


   # Fetch point forecast loaction from user definition
   #lon,lat = ForecastPointPosition()
   [lon,lat],posd = ForecastPointPosition()
   print(ForecastPointPosition())


   # Fetch variables from user definitiona for point forecast 
   var_list=VariableListPoint()

   print ( var_list)

   ncfile   = netCDF4.Dataset(ncfileName)

   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]

   y_idx, x_idx= PointIdx(lat,lon,latitudes,longitudes)


   print( posd['point1']['lat'])
   print( posd['point1']['lon'])

   print (y_idx,x_idx )

   print (len(posd))

   ytest = np.empty(len(posd),dtype=int)
   xtest = np.empty(len(posd),dtype=int)
   #ytest=[]
   #xtest=[]
   i=0
   for key in posd.keys():
       print('key')
       print(key)

       print( posd[key]['lat'])
       ytest[i],xtest[i] = PointIdx(posd[key]['lat'],posd[key]['lon'],latitudes,longitudes)

       print (ytest,xtest )
       i=i+1   
   print (sorted(posd.keys()))
 
   print(ytest)
   print(xtest)
 


   time       = ncfile.variables['time'][:]
   height     = ncfile.variables['pressure'][:]

   p_lat=latitudes[y_idx,x_idx]
   p_lon=longitudes[y_idx,x_idx]

   var = np.empty((len(var_list),len(time),len(height),len(posd),len(posd)))
   unit={}
   long_name={}

   for i in range(len(var_list)):
      print (var_list[i])
      #p_var = np.squeeze(ncfile.variables['specific_humidity_pl'][:,:,y_idx,x_idx])
      #var[i,:,:] = np.squeeze(ncfile.variables[var_list[i]][:,:,y_idx,x_idx])
      #var[i,:,:] = np.squeeze(ncfile.variables[var_list[i]][:,:,ytest,xtest])
      var[i,:,:,:,:] = np.squeeze(ncfile.variables[var_list[i]][:,:,ytest,xtest])
      unit[i] =  ncfile.variables[var_list[i]].units
      long_name[i] =  ncfile.variables[var_list[i]].long_name

   ncfile.close()

   



   plot_point(time,height,var[0,:,:,:,:],p_lat,p_lon,len(posd),unit[0],long_name[0] )
   plot_point(time,height,var[1,:,:,:,:],p_lat,p_lon,len(posd),unit[1],long_name[1] )










