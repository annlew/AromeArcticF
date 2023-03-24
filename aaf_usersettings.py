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


def VariableList():
   variables=['surface_air_pressure',
              'lwe_thickness_of_atmosphere_mass_content_of_water_vapor']

   return variables


def FetchTime():
    # provide fetch time interval in 24h format
    BeginHour=17
    BeginMin =0
    EndHour  =17
    EndMin   =2
  
    return BeginHour,BeginMin,EndHour,EndMin
