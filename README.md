# AromeArcticF

## Install 
```
git clone https://github.com/annlew/AromeArcticF.git

conda env create -f oden.yml

conda activate oden
```
For retrieving latest Oden location, access to Linus' fpt is required. Credentials need to be stored in  ~/.netrc

## Run at preset time
```
python arome_arctic_forecast.py
```
## Run now
```
python arome_arctic_forecast.py now
```

## Add extra point forecast locations

Create a file Extraloc.txt where a longitude and latitude pair separated by space is specified on each line.

Example:
```
-1.723 80.154
```
