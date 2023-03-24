import numpy as np
from datetime import datetime,timezone


def user_settings():

   # XML source
   url='https://thredds.met.no/thredds/catalog/aromearcticlatest/archive/catalog.xml'

   # Number of forecast to display in addition to anlaysis
   forecasts=2

   # forecast interval length in hours
   forecast_length=3

   #-----------------------------------------

   forecast_length_s=forecast_length*60*60

   return forecasts,forecast_length


def variable_list():
   variables=['surface_air_pressure',
              'lwe_thickness_of_atmosphere_mass_content_of_water_vapor']

   return variables
