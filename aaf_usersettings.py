import numpy as np
from datetime import datetime,timezone


def ForecastSettings():

   # XML source
   url='https://thredds.met.no/thredds/catalog/aromearcticlatest/archive/catalog.xml'

   # Number of forecast to display in addition to anlaysis
   forecasts=2

   # forecast interval length in hours
   forecast_length=3

   #-----------------------------------------

   forecast_length_s=forecast_length*60*60

   return forecasts,forecast_length


def ForecastPointPosition():

           # lon  lat
   position= [15, 78]
   positiond= {("point1","lat"):15,("point2","lat"): 11.53,
               ("point1","lon"):78,("point2","lon"): 78.54  }

   positiond2 = { 'point1':   {'lat': 78,    'lon':15    },
                  'zeppelin': {'lat': 78.54, 'lon': 11.53}}


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
    BeginHour=18
    BeginMin =1
    EndHour  =18
    EndMin   =20
  
    return BeginHour,BeginMin,EndHour,EndMin
