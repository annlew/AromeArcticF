import numpy as np
from datetime import datetime,timezone
from aaf_func import *
import os

def ForecastSettings():

   # XML source
   url='https://thredds.met.no/thredds/catalog/aromearcticlatest/archive/catalog.xml'

   # Number of forecast to display in addition to anlaysis
   forecasts=11

   # forecast interval length in hours
   forecast_length=6

   #-----------------------------------------

   forecast_length_s=forecast_length*60*60

   return forecasts,forecast_length


def ForecastPointPosition():

           # lon  lat
   position= [15, 78]
   positiond2 = { 'Oden':         {'lat': 79.72, 'lon':1.98  }, # deafault position, overwritten if Odenloc.txt exists
                  'Longyearbyen': {'lat': 78.13, 'lon': 15.38}}

   # Read position for point forecast from files if files exist
   if os.path.isfile('Odenloc.txt'):
      print ('Oden location exists')
      lat,lon=ReadLoc('Odenloc.txt')
      positiond2['Oden']['lat']=float(lat[0])
      positiond2['Oden']['lon']=float(lon[0])
   if os.path.isfile('Extraloc.txt'):
      print ('Extra locations exist')
      lat,lon=ReadLoc('Extraloc.txt')
      for loc in range(len(lat)):
         newpos= {str(loc+1): {'lat': float(lat[loc]), 'lon':float(lon[loc])  }}
         print(newpos)
         positiond2.update(newpos)

   return position,positiond2


# Variable lists for plots

def VariableListPoint():
   # Variable for point forecast
   variables=['specific_humidity_pl',
              'air_temperature_pl']
   return variables

def VariableListMap():
   # Variables for map plots
   variables=['lwe_thickness_of_atmosphere_mass_content_of_water_vapor',
              'air_pressure_at_sea_level',
              'SFX_SIC']
   return variables

def VariableListTZMap():
   # Variables for temperature geopotential height map plots
   variables=['air_temperature_pl', 
              'geopotential_pl',
              'SFX_SIC']
   return variables

def VariableListTPMap():
   # Variables for temperature mslp map plots
   variables=['air_temperature_ml', 
              'air_pressure_at_sea_level',
              'SFX_SIC']
   return variables

def VariableListPWMap():
   # Variables for map plots
   variables=['lwe_thickness_of_atmosphere_mass_content_of_water_vapor',
              'air_pressure_at_sea_level',
              'SFX_SIC']
   return variables

def VariableListPrecMap():
   # Variables for map plots
   variables=['precipitation_amount_acc',
              'air_pressure_at_sea_level',
              'SFX_SIC']
   return variables

def FetchTime():
    # provide fetch time interval in 24h format
    BeginHour=9
    BeginMin =5
    EndHour  =BeginHour+1
    EndMin   =BeginMin
  
    return BeginHour,BeginMin,EndHour,EndMin
