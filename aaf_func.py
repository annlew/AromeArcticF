from datetime import datetime,timezone



def todayAt (hr, min=0, sec=0, micros=0):
   now = datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)
