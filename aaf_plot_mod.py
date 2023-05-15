import numpy as np
import matplotlib.pylab as plt
from datetime import datetime,timezone
import cartopy.crs as ccrs
import matplotlib.dates as mdates
#import pyproj
import os
import subprocess

def get_variable():
   print ('hello')   

def cLevs(field,lev):

   if field=='lwe': # precipitable water
     pstart=0.
     pstop=30.
     pstep=2.
   if field=='prec':  # precipitation
     pstart=0.1
     pstop=10
     pstep=1

   if field=='Tp' or field=='Tml':   # temperature
      if lev==850 or lev ==65:
         pstart=-34.
         pstop=30.
         pstep=2.
      else:
         pstart=-34. #np.nanmin(var[0]-T0)
         pstop=30. #np.nanmax(var[0]-T0)
         pstep=2#(pstop-pstart)/20.
      if pstop==pstart:
         pstop=10.
         pstep=(pstop-pstart)/20.

   if field=='Zp' or field=='Psl':
      if lev==500:
         pstart=480.
         pstop=600.
         pstep=2.
      elif lev ==1:
         pstart=800.
         pstop=1040.
         pstep=2.
      else:
         pstart=800. #np.nanmin(var[1]/g)
         pstop=500. #np.nanmax(var[1]/g)
         pstep=(pstop-pstart)/20.
      if pstop==pstart:
         pstop=10.
         pstep=(pstop-pstart)/20.

   if field=='prec':
      steps=int((pstop-0)/pstep)
      levels= np.linspace(0,pstop,num=steps+1, endpoint=True)
      levels[0]=pstart
   else:
      steps=int((pstop-pstart)/pstep)
      levels= np.linspace(pstart,pstop,num=steps+1, endpoint=True)

   return levels




def plot_TZ(x,y,var,time,nfigs,Tp,Zp,Tml,Psl,lwe,prec):

   # Define contour levels depending on variable   
   if Tp:
      print('tp',Tp)
      levsT= cLevs('Tp',Tp)
   if Tml:
      print('tml',Tml)
      levsT= cLevs('Tml',Tml)
   if lwe:
      print('lwe',lwe)
      levsT= cLevs('lwe',lwe)
   if prec:
      print('prec',prec)
      levsT= cLevs('prec',prec)
   if Zp:
      print('Zp',Zp)
      levsZ= cLevs('Zp',Zp)
   if Psl:
      print('Psl',Psl)
      levsZ= cLevs('Psl',Psl)

   # constants
   g =98.0665
   T0=273.15

   cmap='viridis'
   cmap='nipy_spectral'
   if prec:
      cmap='Blues'
  
   ax={}
   cf={}
   cp={}
   ci={}
   cb={}
   fig={}
   date={}   
   datet={}   
   datef={}   

   for i in range(nfigs):
      fig[i],ax[i]=plt.subplots(1,1,subplot_kw=dict(projection=ccrs.RotatedPole(pole_longitude=155.0, pole_latitude=15.0)))
      ax[i].set_extent([-20, 74, 68, 90],crs=ccrs.PlateCarree())
      ax[i].gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
      ax[i].coastlines()

      date[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
      datet[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y%m%d_%H")
      datef[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y%m%d_00")

      # plot field
      if Tp or Tml:
         cf[i]=ax[i].contourf(x, y, var[0,i,:,:]-T0, levels=levsT,transform=ccrs.PlateCarree())
      elif prec:
         if i==0:
            cf[i]=ax[i].contourf(x, y, var[0,i,:,:], levels=levsT,transform=ccrs.PlateCarree())
         else:
            cf[i]=ax[i].contourf(x, y, var[0,i,:,:]-var[0,i-1,:,:] , levels=levsT,transform=ccrs.PlateCarree())
      else:
         cf[i]=ax[i].contourf(x, y, var[0,i,:,:], levels=levsT,transform=ccrs.PlateCarree())

      # plot ice edge 
      ci[i]=ax[i].contour(x, y, var[2,i,:,:], levels=0,colors='w',linewidths=2,transform=ccrs.PlateCarree())

      # plot mslp/geop
      if Zp:
         cp[i]=ax[i].contour(x, y, var[1,i,:,:]/g, levels=levsZ,colors='k',linewidths=.5,transform=ccrs.PlateCarree())
      elif Psl:
         cp[i]=ax[i].contour(x, y, var[1,i,:,:]/100., levels=levsZ,colors='k',linewidths=.5,transform=ccrs.PlateCarree())
      ax[i].clabel(cp[i], fontsize=10 )
      cf[i].set_cmap(cmap)

      cb[i] = fig[i].colorbar(cf[i],orientation='horizontal', shrink=0.6)

      if (Tp!=None and Zp!=None):
         cb[i].ax.set_title('Geopotential height [dam] '+str(Zp)+'hPa\n Temperature [$^{\circ}$C] '+str(Tp)+'hPa')
      if (Tml != None and Psl != None):
         cb[i].ax.set_title('MSLP [hPa] '+str(Zp)+'hPa\n Temperature [$^{\circ}$C] lowest model level')

      if i==0: 
         ax[i].set_title('Analysis '+date[i])
      else:
         ax[i].set_title('Production time '+date[0]+' Valid '+date[i])

      fig[i].set_size_inches(10,10, forward=True)
      fig[i].tight_layout()


      dirName='../../artofmelt/AromeArctic/'+datef[0]
      if not os.path.exists(dirName):
         os.makedirs(dirName)

      if (Tp and Zp):
         cb[i].ax.set_title('Geopotential height [dam] '+str(Zp)+'hPa\n Temperature [$^{\circ}$C] '+str(Tp)+'hPa')
         fig[i].savefig(dirName+'/Arome_Arctic_T'+str(Tp)+'Z'+str(Zp)+'_'+datet[0]+'_'+datet[i]+'.png')
         fig[i].clf()
         plt.close(fig[i])
      if (Tml and Psl):
         cb[i].ax.set_title('MSLP [hPa] \n Temperature [$^{\circ}$C] lowest model level')
         fig[i].savefig(dirName+'/Arome_Arctic_Tml'+str(Tml)+'MSLP_'+datet[0]+'_'+datet[i]+'.png')
         fig[i].clf()
         plt.close(fig[i])
      if (lwe and Psl):
         cb[i].ax.set_title('MSLP [hPa] \n Precipitable water [m]')
         fig[i].savefig(dirName+'/Arome_Arctic_Precipitablewater_MSLP_'+datet[0]+'_'+datet[i]+'.png')
         fig[i].clf()
         plt.close(fig[i])
      if (prec and Psl):
         cb[i].ax.set_title('MSLP [hPa] \n Accumulated precipitation [kg/m^2]')
         fig[i].savefig(dirName+'/Arome_Arctic_Precip_MSLP_'+datet[0]+'_'+datet[i]+'.png')
         fig[i].clf()
         plt.close(fig[i])

      subprocess.call(['rclone', 'copy', '--ignore-existing', dirName ,  'remote_box:artofmelt/'+datef[0]+'/Arome'])


def plot2(figin,axin,x,y,var,time):

   print('hello2')
   cmap='viridis'

   pstart=75000.
   pstop=104000.
   pstep=500.
   steps=int((pstop-pstart)/pstep)   
   levs= np.linspace(pstart,pstop,num=steps+1, endpoint=True)


   for i in range(len(axin)):

      date=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
      cf=axin[i].contourf(x, y, var[i,:,:], levels=levs)
      cp=axin[i].contour(x, y, var[i,:,:], levels=levs,colors='k',linewidths=.5)
      axin[i].clabel(cp, fontsize=10 )
      axin[i].set_title(date)
      cf.set_cmap(cmap)

   cbar_ax = figin.add_axes([0.3, 0.035, 0.4, 0.02])
   figin.colorbar(cf, cax=cbar_ax,orientation='horizontal')


   plt.show()

def plot_point(t,z,var,lat,lon,nfigs,units,long_name):


   date=datetime.fromtimestamp(t[0],tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
   datet=datetime.fromtimestamp(t[0],tz=timezone.utc).strftime("%Y-%m-%d_%H:%M")

   func = np.vectorize(datetime.utcfromtimestamp)
   t_ax=func(t)

   ax={}
   cf={}
   cp={}
   cb={}
   fig={}
   for i in range(nfigs):
   
      fig[i],ax[i]=plt.subplots(1,1)
      cf[i]=ax[i].contourf(t_ax,z, var[:,:,i,i].T)
      plt.gca().invert_yaxis()
   
      fig[i].set_size_inches(12,6, forward=True)
   
      fig[i].tight_layout(rect=[0.02,0.05 ,1.06 ,0.95])
   
      cb[i] = fig[i].colorbar(cf[i],orientation='vertical')#, shrink=0.6)
      cb[i].ax.set_title(units)


      Day_Locator= mdates.DayLocator() 
      Hour_Locator= mdates.HourLocator(interval=3) 
      formatter = mdates.ConciseDateFormatter(Day_Locator)
      minformatter = mdates.ConciseDateFormatter(Day_Locator)
      ax[i].xaxis.set_minor_locator(Hour_Locator) 
      ax[i].xaxis.set_major_locator(Day_Locator) 
      ax[i].xaxis.set_major_formatter(formatter)
      ax[i].xaxis.set_minor_formatter(formatter)
   
      ax[i].set_ylabel('pressure [hPa]')
      ax[i].set_xlabel('time')
    
      ax[i].set_title(long_name+' Production time '+date+' lat '+str('%.2f'%lat)+' lon '+str('%.2f'%lon))
   
      fig[i].savefig('Arome_Arctic_'+str('%.2f'%lat)+'_'+str('%.2f'%lon)+'_'+long_name.replace(" ", "")+'_'+datet+'.png')


def plot_pointZ(t,z,var,var_aux,var_aux2,lat,lon,nfigs,**kwargs):
   field    = kwargs.get('field',    None)
   var_aux3 = kwargs.get('var_aux3', None)

   # contour levels
   if field=='q':
      pstart=0.
      pstop=5.
      pstep=0.2
      steps=int((pstop-pstart)/pstep)
      levs= np.linspace(pstart,pstop,num=steps+1, endpoint=True)
   if field=='t':
      levs= cLevs('Tml',1)
   if field=='wind':
      levs= cLevs('lwe',1)

   # various time definitions
   date=datetime.fromtimestamp(t[0],tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
   datet=datetime.fromtimestamp(t[0],tz=timezone.utc).strftime("%Y-%m-%d_%H:%M")
   datef=datetime.fromtimestamp(t[0],tz=timezone.utc).strftime("%Y%m%d_%H")
   dateo=datetime.fromtimestamp(t[0],tz=timezone.utc).strftime("%Y%m%d_00")

   func = np.vectorize(datetime.utcfromtimestamp)
   t_ax=func(t)

   Day_Locator= mdates.DayLocator() 
   Hour_Locator= mdates.HourLocator(interval=6) 
   formatter = mdates.ConciseDateFormatter(Day_Locator)
   minformatter = mdates.ConciseDateFormatter(Day_Locator)

   ax={}
   ax2={}
   cf={}
   cp={}
   cb={}
   fig={}
   for i in range(nfigs):

      fig[i],ax=plt.subplots(2,2,gridspec_kw={'width_ratios': [4, 1], 'height_ratios': [3,1]},constrained_layout=True)
      fig[i].set_size_inches(12,8, forward=True)

      # FIRST AXES
      cf[0,0]=ax[0,0].contourf(t_ax,z, var[:,:,i].T,levels=levs)
      cb[0,0] = plt.colorbar(cf[0,0],ax=ax[0,0],orientation='vertical',pad=-0.01)#, shrink=0.6)
             
      if field=='q':
         cb[0,0].ax.set_title('g/kg')
         ax[0,0].set_title('Specific humidity Production time '+date+' lat '+str('%.2f'%lat[i])+' lon '+str('%.2f'%lon[i]))
      if field=='t':
         cb[0,0].ax.set_title('[$^{\circ}$C]')
         ax[0,0].set_title('Temperature Production time '+date+' lat '+str('%.2f'%lat[i])+' lon '+str('%.2f'%lon[i]))
      if field=='wind':
         cb[0,0].ax.set_title('[m/s]')
         ax[0,0].set_title('Wind speed Production time '+date+' lat '+str('%.2f'%lat[i])+' lon '+str('%.2f'%lon[i]))

      # invariant decorations
      cmap='nipy_spectral'
      cf[0,0].set_cmap(cmap)
      ax[0,0].xaxis.set_minor_locator(Hour_Locator) 
      ax[0,0].xaxis.set_major_locator(Day_Locator) 
      ax[0,0].set_xticklabels([])
      ax[0,0].set_ylabel('height [m]')
      ax[0,0].grid(axis='x', color='dimgrey',which='minor', linestyle='--') 
      ax[0,0].grid(axis='y', color='dimgrey', linestyle='--') 

   
      # SECOND AXES
      if field=='q' or field=='t':
         q1,=ax[0,1].plot( var[0,:,i],z,label='00')
         q2,=ax[0,1].plot( var[24,:,i],z,'r',label='24')
         q3,=ax[0,1].plot( var[48,:,i],z,'y',label='48')
         q4,=ax[0,1].plot( var[-1,:,i],z,'k',label='66')

      if field=='wind':
         q1,=ax[0,1].plot( var_aux3[0,:,i],z,label='00')
         q2,=ax[0,1].plot( var_aux3[24,:,i],z,'r',label='24')
         q3,=ax[0,1].plot( var_aux3[48,:,i],z,'y',label='48')
         q4,=ax[0,1].plot( var_aux3[-1,:,i],z,'k',label='66')

         ax[0,1].set_xlim(0,360)
         ax[0,1].set_xlabel('WD')
         ax[0,1].set_xticks([0,90,180,270,360])
         ax[0,1].set_xticklabels(['N','E','S','W','N'])      

      if field=='q':
         ax[0,1].set_xlim(0,5)
         ax[0,1].set_xlabel('q [g/kg]')
      if field=='t':
         ax[0,1].set_xlabel('T [$^{\circ}$C]')

      # invariant decorations
      ax[0,1].legend(handles=[q1,q2,q3,q4],loc='lower right', bbox_to_anchor=(1, 1),ncol=2)
      ax[0,1].set_ylim(0,z[-1])
      ax[0,1].grid(axis='y', color='dimgrey', linestyle='--') 
      ax[0,1].grid(axis='x', color='dimgrey', linestyle='--') 
      ax[0,1].set_yticklabels([])

      # THIRD AXES
      p1,=ax[1,0].plot(t_ax, var_aux[:,i,i],'k')

      if field=='q':
         ax[1,0].set_ylabel('precipitation [mm]')
         ax[1,0].set_ylim(0,max(var_aux[:,i,i]))
      if field=='t':
         ax[1,0].set_ylim(min( np.min(var_aux[:,i,i]), np.min(var_aux2[:,i,i]))-0.5,max(np.max(var_aux[:,i,i]),np.max(var_aux2[:,i,i]))+0.5)
         ax[1,0].set_ylabel('T 0m [$^{\circ}$C]')
      if field=='wind':
         ax[1,0].set_ylim(0,np.max(var_aux[:,i,i]))
         ax[1,0].set_ylabel('wind speed 10m [m/s]')

      # invariant decorations
      ax[1,0].set_xlabel('time')
      ax[1,0].grid(axis='x', color='dimgrey',which='minor', linestyle='--') 
      ax[1,0].grid(axis='y', color='dimgrey', linestyle='--') 

      # double axes
      ax2 = ax[1,0].twinx()
      if field=='q':
         p2,=ax2.plot(t_ax, var_aux2[:,i],'darkblue')
         ax2.set_ylabel('cloud water [kg/m2]',color='darkblue')
         ax2.set_ylim(0,np.max(var_aux2[:,i]))
      if field=='t':
         p2,=ax2.plot(t_ax, var_aux2[:,i,i],'darkblue')
         ax2.set_ylabel('T 2m [$^{\circ}$C]',color='darkblue')
         ax2.set_ylim(min( np.min(var_aux[:,i,i]), np.min(var_aux2[:,i,i]))-0.5,max(np.max(var_aux[:,i,i]), np.max(var_aux2[:,i,i]))+0.5)
      if field=='wind':
         p2,=ax2.plot(t_ax, var_aux2[:,i,i],'darkblue',label='cloud water')
         ax2.set_ylabel('WD 10m',color='darkblue')
         ax2.set_ylim(0,360)
         ax2.set_yticks([0,90,180,270,360])
         ax2.set_yticklabels(['N','E','S','W','N'])      

      # invariant decorations
      ax2.set_xlim(t_ax[0],t_ax[-1])
      ax2.grid(axis='y', color='cornflowerblue', linestyle='--') 
      ax2.tick_params(axis='y', colors='darkblue')
      ax2.xaxis.set_minor_locator(Hour_Locator) 
      ax2.xaxis.set_major_locator(Day_Locator) 
      ax2.xaxis.set_major_formatter(formatter)
      ax2.xaxis.set_minor_formatter(formatter)

      # FORTH AXES: empty
      ax[-1, -1].axis('off')

      dirName='../../artofmelt/AromeArctic/'+dateo
      if not os.path.exists(dirName):
         os.makedirs(dirName)
   
      if field=='q':
         fig[i].savefig(dirName+'/Arome_Arctic_ZQ_'+datef+'_'+str('%.2f'%lat[i])+'_'+str('%.2f'%lon[i])+'.png')
      if field=='t':
         fig[i].savefig(dirName+'/Arome_Arctic_ZT_'+datef+'_'+str('%.2f'%lat[i])+'_'+str('%.2f'%lon[i])+'.png')
      if field=='wind':
         fig[i].savefig(dirName+'/Arome_Arctic_Zwind_'+datef+'_'+str('%.2f'%lat[i])+'_'+str('%.2f'%lon[i])+'.png')

      fig[i].clf()
      plt.close(fig[i])

      subprocess.call(['rclone', 'copy', '--ignore-existing', dirName ,  'remote_box:artofmelt/'+dateo+'/Arome'])


def plot_pw_rotated_grid_separate(x,y,var,time,nfigs,units,long_name):

   if units=='m':
      pstart=0.
      pstop=20.
      pstep=2.
   elif units =='Pa':
      pstart=75000.
      pstop=104000.
      pstep=500.
   elif units =='':
      pstart=0.
      pstop=1.
      pstep=0.1
   else:
      pstart=np.nanmin(var)
      pstop=np.nanmax(var)
      if pstop==pstart:
         pstop=10.
   pstep=(pstop-pstart)/20.
   print(pstart) 
   print(pstop) 

   cmap='viridis'
   #pstart=0.
   #pstop=20.
   #pstep=2.
   steps=int((pstop-pstart)/pstep)
   levs= np.linspace(pstart,pstop,num=steps+1, endpoint=True)
   ax={}
   cf={}
   cp={}
   cb={}
   fig={}
   date={}   
   datet={}   

   for i in range(nfigs):
      fig[i],ax[i]=plt.subplots(1,1,subplot_kw=dict(projection=ccrs.RotatedPole(pole_longitude=155.0, pole_latitude=15.0)))
      ax[i].set_extent([-20, 74, 68, 90],crs=ccrs.PlateCarree())
      ax[i].gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
      ax[i].coastlines()

      date[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
      datet[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d_%H:%M")

      cf[i]=ax[i].contourf(x, y, var[i,:,:], levels=levs,transform=ccrs.PlateCarree())
      #cp[i]=ax[i].contour(x, y, var[i,:,:], levels=levs,colors='k',linewidths=.5,transform=ccrs.PlateCarree())
      cp[i]=ax[i].contour(x, y, var[i,:,:], levels=0,colors='k',linewidths=1.5,transform=ccrs.PlateCarree())
      ax[i].clabel(cp[i], fontsize=10 )
      cf[i].set_cmap(cmap)

      cb[i] = fig[i].colorbar(cf[i],orientation='horizontal', shrink=0.6)
      cb[i].ax.set_title(long_name+' ['+units+']')


      if i==0: 
         ax[i].set_title('Analysis '+date[i])
      else:
         ax[i].set_title('Production time '+date[0]+' Valid '+date[i])

      fig[i].set_size_inches(10,10, forward=True)
      fig[i].tight_layout()
      fig[i].savefig('Arome_Arctic_'+long_name.replace(" ", "")+'_'+datet[0]+'_'+datet[i]+'.png')

def plot_slp_rotated_grid_separate(x,y,var,time,nfigs):

   cmap='viridis'
   pstart=75000.
   pstop=104000.
   pstep=500.
   steps=int((pstop-pstart)/pstep)
   levs= np.linspace(pstart,pstop,num=steps+1, endpoint=True)
   ax={}
   cf={}
   cp={}
   fig={}
   date={}   
   datet={}   

   for i in range(nfigs):
      fig[i],ax[i]=plt.subplots(1,1,subplot_kw=dict(projection=ccrs.RotatedPole(pole_longitude=155.0, pole_latitude=15.0)))
      ax[i].set_extent([-20, 74, 68, 90],crs=ccrs.PlateCarree())
      ax[i].gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
      ax[i].coastlines()

      date[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
      datet[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d_ %H:%M")

      cf[i]=ax[i].contourf(x, y, var[i,:,:], levels=levs,transform=ccrs.PlateCarree())
      cp[i]=ax[i].contour(x, y, var[i,:,:], levels=levs,colors='k',linewidths=.5,transform=ccrs.PlateCarree())
      ax[i].clabel(cp[i], fontsize=10 )
      cf[i].set_cmap(cmap)

      fig[i].colorbar(cf[i], orientation='horizontal', shrink=0.6)

      if i==0: 
         ax[i].set_title('Analysis '+date[i])
      else:
         ax[i].set_title('Production time '+date[0]+' Valid '+date[i])

      fig[i].set_size_inches(10,10, forward=True)
      fig[i].tight_layout()
      fig[i].savefig('Arome_Arctic_'+datet[0]+'_'+datet[i]+'.png')



def plot3(x,y, var, time,nfigs):




   cmap='viridis'

   pstart=75000.
   pstop=104000.
   pstep=500.
   steps=int((pstop-pstart)/pstep)
   levs= np.linspace(pstart,pstop,num=steps+1, endpoint=True)
   ax={}
   cf={}
   cp={}
   #date={}   
   fig={}

   for i in range(nfigs):
      fig[i],ax[i]=plt.subplots(1,1,subplot_kw=dict(projection=ccrs.RotatedPole(pole_longitude=155.0, pole_latitude=15.0)))
      #ax[i] = plt.axes(projection=ccrs.RotatedPole(pole_longitude=155.0, pole_latitude=15.0))
      #fig[i] = plt.axes(projection=ccrs.RotatedPole(pole_longitude=155.0, pole_latitude=15.0))
      #fig[i].axes(projection=ccrs.RotatedPole(pole_longitude=155.0, pole_latitude=15.0))
      ax[i].set_extent([-20, 74, 68, 90],crs=ccrs.PlateCarree())
      ax[i].gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
      ax[i].coastlines()

      print ('hej')

  # for i in range(nfigs):
   #fig=plt.figure()
   #ax= fig.add_axes([0,0,1,1])
      date=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

      cf[i]=ax[i].contourf(x, y, var[i,:,:], levels=levs)
      #cf=ax.contourf(x, y, var[i,:,:], levels=levs,transform=ccrs.PlateCarree())
      cp[i]=ax[i].contour(x, y, var[i,:,:], levels=levs,colors='k',linewidths=.5)
      #cp=ax.contour(x, y, var[i,:,:], levels=levs,colors='k',linewidths=.5,transform=ccrs.PlateCarree())
      ax[i].clabel(cp[i], fontsize=10 )
      ax[i].set_title(date)
      cf[i].set_cmap(cmap)

      fig[i].colorbar(cf[i], orientation='horizontal', shrink=0.6)

      #ax[i].figure.set_size_inches(10,12, forward=True)
      fig[i].set_size_inches(10,10, forward=True)

      #plt.show( )
      #plt.show( block=False)
      #ax[i].figure.savefig("plot_%s.png" %i)
      fig[i].tight_layout()
      fig[i].savefig("plot_%s.png" %i)
      #plt.clf()






def define_figure(pan_row,pan_col):

   print('hello3')
   fig, ax = plt.subplots(pan_row,pan_col)
   
   x_size=pan_col*8.
   y_size=pan_row*8.
   fig.set_size_inches(x_size,y_size, forward=True)
   fig.tight_layout(rect=[0,0.05,1,0.98])

   # if each forecast is plotted in separate figure
   

   return fig, ax










