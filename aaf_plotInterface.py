from datetime import datetime,timezone
import numpy as np
from aaf_usersettings import *
from aaf_plot_mod import *
from aaf_func import *
import netCDF4
import fnmatch
import time as timer



# Plot prep functions
#####################################################################

def TZPrep(ncfileName,**kwargs):
   Tpl = kwargs.get('Tpl', None)
   Zpl = kwargs.get('Zpl', None)
   Tml = kwargs.get('Tml', None)
   Psl = kwargs.get('Psl', None)
   lwe = kwargs.get('lwe', None)
   prec= kwargs.get('prec', None)

   # Fetch variables from user definitions for map plot

   if (Tpl and Zpl):
      var_list=VariableListTZMap()
   if (Tml and Psl):
      var_list=VariableListTPMap()
   if (lwe and Psl):
      var_list=VariableListPWMap()
   if (prec and Psl):
      var_list=VariableListPrecMap()

   #print (var_list)

   forecasts, forecast_length =ForecastSettings()
   print(ncfileName)
   ncfile   = netCDF4.Dataset(ncfileName)

   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]
   timestep  = ncfile.variables["time"][0:(forecasts+1)*forecast_length:forecast_length]

   v_idx=[]
   if Tml:
      modellev  = ncfile.variables["hybrid"][:]
      #v_idx.append(np.where(modellev==Tml)[0])
      v_idx.append(Tml-1)
   if Tpl or Zpl:
      pressure  = ncfile.variables["pressure"][:]
      if Tpl:
         v_idx.append(np.where(pressure==Tpl)[0])
      if Zpl:
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



def PointPrepZ(ncfileName):

   # Fetch point forecast loaction from user definition
   [lon,lat],posd = ForecastPointPosition()

   # constants
   maxIdx=35#60
   e=0.622
   R=287.052874 
   g=9.82

   ncfile   = netCDF4.Dataset(ncfileName)

   time      = ncfile.variables['time'][:]
   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]
   ap        = ncfile.variables["ap"][maxIdx:]
   b         = ncfile.variables["b"][maxIdx:]
   cap       = ncfile.variables["ap"][:]
   cb        = ncfile.variables["b"][:]


   #print (len(posd))

   ytest = np.empty(len(posd),dtype=int)
   xtest = np.empty(len(posd),dtype=int)
   i=0
   for key in posd.keys():
       print('Location', key)

       #print( posd[key]['lat'])
       ytest[i],xtest[i] = PointIdx(posd[key]['lat'],posd[key]['lon'],latitudes,longitudes)

       print (ytest[i],xtest[i] )
       print('lat: ',latitudes[ytest[i],xtest[i]], ' lon: ',longitudes[ytest[i],xtest[i]])
       i=i+1   
   #print (sorted(posd.keys()))
 
   #print('latitudes')
   #print(latitudes[ytest,xtest])
   #print('longitudes')
   #print(longitudes[ytest,xtest])
 
   # vertical coordinate conversion

   print ('Read variables for vertical interpolation')
   print ('pressure')
   ps = np.squeeze(ncfile.variables['surface_air_pressure'][:,:,ytest,xtest])
   print ('temperature')
   T = ncfile.variables['air_temperature_ml'][:,maxIdx:,ytest,xtest]
   print ('humidity')
   q = 1000.*ncfile.variables['specific_humidity_ml'][:,maxIdx:,ytest,xtest]

   print ('Read variables for plotting')
   # temperature
   print ('surface temperature')
   T0 =  np.squeeze(ncfile.variables['air_temperature_0m'][:,:,ytest,xtest])-273.15
   T2 =  np.squeeze(ncfile.variables['air_temperature_2m'][:,:,ytest,xtest])-273.15

   # wind
   print ('wind')
   U = ncfile.variables['x_wind_ml'][:,maxIdx:,ytest,xtest]
   V = ncfile.variables['y_wind_ml'][:,maxIdx:,ytest,xtest]
   print ('surface wind')
   ws10 =  np.squeeze(ncfile.variables['wind_speed'][:,:,ytest,xtest])
   wd10 =  np.squeeze(ncfile.variables['wind_direction'][:,:,ytest,xtest])

   print ('precipitation')
   prec = np.squeeze(ncfile.variables['precipitation_amount_acc'][:,:,ytest,xtest])

   print ('cloud water and ice (full atmosphere)')
   clm=  ncfile.variables['mass_fraction_of_cloud_condensed_water_in_air_ml'][:,:,ytest,xtest]
   cim=  ncfile.variables['mass_fraction_of_cloud_ice_in_air_ml'][:,:,ytest,xtest]
   
   # Close file
   ncfile.close()


   # 2D variables

   print ('calculate wind speed and direction')
   ws=np.zeros((len(time),len(ap),len(posd))) 
   wd=np.zeros((len(time),len(ap),len(posd))) 
   for loc in range(len(posd)):
      ws[:,:,loc]= np.sqrt(U[:,:,loc,loc]*U[:,:,loc,loc] + V[:,:,loc,loc]*V[:,:,loc,loc]  )
      wd[:,:,loc]=270.-np.arctan2(V[:,:,loc,loc],U[:,:,loc,loc])*(180./np.pi)
      if np.max(wd[:,:,loc])>360.:
         wd[:,:,loc]=np.where(wd[:,:,loc]>360.,wd[:,:,loc]-360., wd[:,:,loc])

#   tic = timer.perf_counter()
#   toc = timer.perf_counter()
#   tac = timer.perf_counter()
#
#   print(f"First {toc - tic:0.4f} seconds")
#   print(f"Second {tac - toc:0.4f} seconds")


   # Vertical integration of cloud variables
   print ('vertical integration of cloud water and ice')
   cpl=np.zeros((len(cap),len(time),len(posd),len(posd))) 
   for k in range(len(cap)):
      cpl[k,:,:,:]=  cap[k] + cb[k]*ps[:,:,:]

   clm_v=np.zeros((len(time),len(posd))) 
   cim_v=np.zeros((len(time),len(posd))) 
   for i in range(len(time)):
      for loc in range(len(posd)):
         clm_v[i,loc]= np.sum(clm[i,1:,loc,loc]*np.diff(cpl[:,i,loc,loc])/g)
         cim_v[i,loc]= np.sum(cim[i,1:,loc,loc]*np.diff(cpl[:,i,loc,loc])/g)
   cwm=clm_v+cim_v


   print('virtual temperature')
   Tv=T*(q+e)/(e*(1.+q))


   print('model levels to pressure to height')
   plevs=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   z    =np.zeros((len(ap),len(time),len(posd),len(posd))) 
   dz   =np.zeros((len(ap),len(time),len(posd),len(posd))) 
   for k in range(len(ap)):
      plevs[k,:,:,:]=  ap[k] + b[k]*ps[:,:,:]
      if k>0:
        dz[k,:,:,:]=(R*Tv[:,k,:,:]/g)*np.log(plevs[k,:,:,:]/plevs[k-1,:,:,:])
        #print (dz[k,0,1,1])
        #z[:k,:,:,:] = z[:k,:,:,:]+dz
        #print (z[k-1,0,1,1])
        z[0:k,:,:,:] =z[0:k,:,:,:]+ dz[k,:,:,:] 


   zv=np.linspace(0, 3000, num=31, endpoint=True)
   #zv=np.linspace(0, 200, num=6, endpoint=True)

   # Vertical interpolation to geometric height
   print ('vertical interpolation')
   qv=np.zeros((len(time),len(zv),len(posd))) 
   tv=np.zeros((len(time),len(zv),len(posd))) 
   wsv=np.zeros((len(time),len(zv),len(posd))) 
   wdv=np.zeros((len(time),len(zv),len(posd))) 
   for i in range(len(time)):
      for loc in range(len(posd)):
         qv[i,:,loc] = np.interp(zv,np.flip(z[:,i,loc,loc]),np.flip(q[i,:,loc,loc]))
         tv[i,:,loc] = np.interp(zv,np.flip(z[:,i,loc,loc]),np.flip(T[i,:,loc,loc]))
         wsv[i,:,loc]= np.interp(zv,np.flip(z[:,i,loc,loc]),np.flip(ws[i,:,loc]))
         wdv[i,:,loc]= np.interp(zv,np.flip(z[:,i,loc,loc]),np.flip(wd[i,:,loc]))


   print ('plot')
   # Call plot function
   plot_pointZ(time,zv,qv[:,:,:],       prec,cwm,      latitudes[ytest,xtest],longitudes[ytest,xtest],len(posd),field='q' )
   plot_pointZ(time,zv,tv[:,:,:]-273.15,T0,  T2,       latitudes[ytest,xtest],longitudes[ytest,xtest],len(posd),field='t' )
   plot_pointZ(time,zv,wsv[:,:,:],ws10,wd10,latitudes[ytest,xtest],longitudes[ytest,xtest],len(posd),field='wind',var_aux3=wdv)

   # detele variables
   del qv,tv,wsv,wdv 
   del q,T,ws,wd,Tv,clm,cim,U,V
   #del q,T,ws,wd,Tv,U,V



def PointPrep(ncfileName):


   # Fetch point forecast loaction from user definition
   #lon,lat = ForecastPointPosition()
   [lon,lat],posd = ForecastPointPosition()
   print(ForecastPointPosition())


   # Fetch variables from user definitiona for point forecast 
   var_list=VariableListPoint()

   print ( var_list)

   # extra variables needed
   # p(n,k,j,i) = ap(k) + b(k)*ps(n,j,i)
   #aux_var= 'surface_air_pressure'
   #aux_var= 'hybrid'
   #         'ap'
   #         'b'

   print(ncfileName)
   ncfile   = netCDF4.Dataset(ncfileName)

   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]
   #ps= ncfile.variables["surface_air_pressure"][:]
   ap= ncfile.variables["ap"][60:]
   b= ncfile.variables["b"][60:]



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
 
   print('ytest')
   print(ytest)
   print('xtest')
   print(xtest)
 


   time       = ncfile.variables['time'][:]
   height     = ncfile.variables['pressure'][:]

   p_lat=latitudes[y_idx,x_idx]
   p_lon=longitudes[y_idx,x_idx]

   # vertical coordinate conversion

   e=0.622

   print ('hej1')
   ps = np.squeeze(ncfile.variables['surface_air_pressure'][:,:,ytest,xtest])
   prec = np.squeeze(ncfile.variables['precipitation_amount_acc'][:,:,ytest,xtest])
   print ('hej2')
   clm=  ncfile.variables['mass_fraction_of_cloud_condensed_water_in_air_ml'][:,60:,ytest,xtest]
   cim=  ncfile.variables['mass_fraction_of_cloud_ice_in_air_ml'][:,60:,ytest,xtest]
   T = ncfile.variables['air_temperature_ml'][:,60:,ytest,xtest]
   print ('hej3')
   q = 1000.*ncfile.variables['specific_humidity_ml'][:,60:,ytest,xtest]
   print ('hej4')
   Tv=T*(q+e)/(e*(1.+q))
   #Tv2=np.multiply(T,np.divide((q+e),(e*(1.+q))))
   print ('ps shape')
   print (ps.shape)
   print (ap.shape)
   print (Tv.shape)
   R=287.052874 
   g=9.82

   #print(T[0,:,0,0])
   #print(Tv[0,:,0,0])






   plevs=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   z=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   dz=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   #Tv=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   for k in range(len(ap)):
   #for k in range(len(posd)):
      plevs[k,:,:,:]=  ap[k] + b[k]*ps[:,:,:]
      if k>0:
        dz[k,:,:,:]=(R*Tv[:,k,:,:]/g)*np.log(plevs[k,:,:,:]/plevs[k-1,:,:,:])
        #print (dz[k,0,1,1])
        #z[:k,:,:,:] = z[:k,:,:,:]+dz
        #print (z[k-1,0,1,1])
        z[0:k,:,:,:] =z[0:k,:,:,:]+ dz[k,:,:,:] 

        #print (z[k-1,0,1,1])
        #print (z[0:k-1,0,1,1])
        #print (z[0:0,0,1,1])
        #print (z[0:1,0,1,1])

   # Vertical integration of cloud variables
   #for k in range(0, len(ap)):
   #   clm_v[:,:,:] = clm_v[:,:,:] + clm[i,k,:,:]*np.diff(plevs[:,0,0])/9.81
   #   #cim_v[:,:,:] = cim_v[:,:,:] + cim[i,k,:,:]*dp[k,:,:]/9.81

   #atm = atm + dp[k,:,:]/9.81
   clm_v=np.zeros(len(time)) 
   cim_v=np.zeros(len(time)) 
   for i in range(len(time)):
      clm_v[i]= np.sum(clm[i,1:,0,0]*np.diff(plevs[:,i,0,0])/g)
      cim_v[i]= np.sum(cim[i,1:,0,0]*np.diff(plevs[:,i,0,0])/g)
   cwm=clm_v+cim_v
   print('clm')
   print(clm[0,1:,0,0])
   print(cim[0,1:,0,0])
   print(clm_v)
   print(cim_v)
   dp = np.diff(plevs[:,0,0,0])
   atm = np.sum(np.diff(plevs[:,0,0,0]))/g
   print(dp)
   print('atm')
   print(atm)

   #print (dz[:,0,1,1])
   print ('z')
   print (z[:,0,0,0])
   #print (z[:,0,1,1])
   print (plevs[:,0,1,1])
   print (plevs.shape)
   zv=np.linspace(0, 200, num=6, endpoint=True)
   print ('zv')
   print (zv)
   #z = dz

   # User variables
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

   print (q.shape)

   qv=np.zeros((len(time),len(zv),len(posd),len(posd))) 
   qv[0,:,0,0]= np.interp(zv,np.flip(z[:,0,0,0]),np.flip(q[0,:,0,0]))

   print(qv[0,:,0,0])
   print(q[0,:,0,0])


   for i in range(len(time)):
     qv[i,:,0,0]= np.interp(zv,np.flip(z[:,i,0,0]),np.flip(q[i,:,0,0]))




   plot_pointZ(time,zv,qv[:,:,:,:],prec,cwm,p_lat,p_lon,len(posd),unit[0],long_name[0] )

   #plot_point(time,height,var[0,:,:,:,:],p_lat,p_lon,len(posd),unit[0],long_name[0] )
   #plot_point(time,height,var[1,:,:,:,:],p_lat,p_lon,len(posd),unit[1],long_name[1] )










def PointPrepPL(ncfileName):


   # Fetch point forecast loaction from user definition
   #lon,lat = ForecastPointPosition()
   [lon,lat],posd = ForecastPointPosition()
   print(ForecastPointPosition())


   # Fetch variables from user definitiona for point forecast 
   var_list=VariableListPoint()

   print ( var_list)

   # extra variables needed
   # p(n,k,j,i) = ap(k) + b(k)*ps(n,j,i)
   #aux_var= 'surface_air_pressure'
   #aux_var= 'hybrid'
   #         'ap'
   #         'b'


   ncfile   = netCDF4.Dataset(ncfileName)

   latitudes = ncfile.variables["latitude" ][:]
   longitudes= ncfile.variables["longitude"][:]
   #ps= ncfile.variables["surface_air_pressure"][:]
   ap= ncfile.variables["ap"][60:]
   b= ncfile.variables["b"][60:]



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
 
   print('ytest')
   print(ytest)
   print('xtest')
   print(xtest)
 


   time       = ncfile.variables['time'][:]
   height     = ncfile.variables['pressure'][:]

   p_lat=latitudes[y_idx,x_idx]
   p_lon=longitudes[y_idx,x_idx]

   # vertical coordinate conversion

   e=0.622

   print ('hej1')
   ps = np.squeeze(ncfile.variables['surface_air_pressure'][:,:,ytest,xtest])
   print ('hej2')
   T = ncfile.variables['air_temperature_ml'][:,60:,ytest,xtest]
   print ('hej3')
   q = 1000.*ncfile.variables['specific_humidity_ml'][:,60:,ytest,xtest]
   print ('hej4')
   Tv=T*(q+e)/(e*(1.+q))
   #Tv2=np.multiply(T,np.divide((q+e),(e*(1.+q))))
   print ('ps shape')
   print (ps.shape)
   print (ap.shape)
   print (Tv.shape)
   R=287.052874 
   g=9.82

   #print(T[0,:,0,0])
   #print(Tv[0,:,0,0])


   plevs=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   z=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   dz=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   #Tv=np.zeros((len(ap),len(time),len(posd),len(posd))) 
   for k in range(len(ap)):
   #for k in range(len(posd)):
      plevs[k,:,:,:]=  ap[k] + b[k]*ps[:,:,:]
      if k>0:
        dz[k,:,:,:]=(R*Tv[:,k,:,:]/g)*np.log(plevs[k,:,:,:]/plevs[k-1,:,:,:])
        #print (dz[k,0,1,1])
        #z[:k,:,:,:] = z[:k,:,:,:]+dz
        #print (z[k-1,0,1,1])
        z[0:k,:,:,:] =z[0:k,:,:,:]+ dz[k,:,:,:] 

        #print (z[k-1,0,1,1])
        #print (z[0:k-1,0,1,1])
        #print (z[0:0,0,1,1])
        #print (z[0:1,0,1,1])


   #print (dz[:,0,1,1])
   print ('z')
   print (z[:,0,0,0])
   #print (z[:,0,1,1])
   print (plevs[:,0,1,1])
   print (plevs.shape)
   zv=np.linspace(0, 200, num=6, endpoint=True)
   print ('zv')
   print (zv)
   #z = dz

   # User variables
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

   print (q.shape)

   qv=np.zeros((len(time),len(zv),len(posd),len(posd))) 
   qv[0,:,0,0]= np.interp(zv,np.flip(z[:,0,0,0]),np.flip(q[0,:,0,0]))

   print(qv[0,:,0,0])
   print(q[0,:,0,0])


   for i in range(len(time)):
     qv[i,:,0,0]= np.interp(zv,np.flip(z[:,i,0,0]),np.flip(q[i,:,0,0]))




   plot_pointZ(time,zv,qv[:,:,:,:],p_lat,p_lon,len(posd),unit[0],long_name[0] )

   plot_point(time,height,var[0,:,:,:,:],p_lat,p_lon,len(posd),unit[0],long_name[0] )
   plot_point(time,height,var[1,:,:,:,:],p_lat,p_lon,len(posd),unit[1],long_name[1] )

