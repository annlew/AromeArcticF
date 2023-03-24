import numpy as np
import matplotlib.pylab as plt
from datetime import datetime,timezone
import cartopy.crs as ccrs
import pyproj

#def user_settings():
#
#   # XML source
#   url='https://thredds.met.no/thredds/catalog/aromearcticlatest/archive/catalog.xml'
#
#   # Number of forecast to display in addition to anlaysis
#   forecasts=2
#
#   # forecast interval length in hours
#   forecast_length=3
#
#   #-----------------------------------------
#
#   forecast_length_s=forecast_length*60*60
#
#   return forecasts,forecast_length 
#
#
#def variable_list():
#   variables=['surface_air_pressure',
#              'lwe_thickness_of_atmosphere_mass_content_of_water_vapor']
#
#   return variables
#
#
def get_variable():
   print ('hello')   





def plot1(x,y,var,date):
   print('hello1')

   ax=plt.pcolormesh(x, y, var)
   plt.title('PS '+date)
   plt.show()



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


def plot_pw_rotated_grid_separate(x,y,var,time,nfigs,units,long_name):

   if units=='m':
      pstart=0.
      pstop=20.
      pstep=2.
   elif units =='Pa':
      pstart=75000.
      pstop=104000.
      pstep=500.
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
      datet[i]=datetime.fromtimestamp(time[i],tz=timezone.utc).strftime("%Y-%m-%d_ %H:%M")

      cf[i]=ax[i].contourf(x, y, var[i,:,:], levels=levs,transform=ccrs.PlateCarree())
      cp[i]=ax[i].contour(x, y, var[i,:,:], levels=levs,colors='k',linewidths=.5,transform=ccrs.PlateCarree())
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










