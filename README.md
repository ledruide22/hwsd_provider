HWSD_ PROVIDER
==============

By using this code you are able to retrieve soil composition for all point over the world.
For more information see https://data.isric.org/geonetwork/srv/api/records/bda461b1-2f35-4d0c-bb16-44297068e10d

1. Requirements

Create conda environement: 
> conda create -n hwsd_provider python=3.8

> conda activate hwsd_provider

> conda install --file requirements.txt

Download:

- HWSD database at http://www.fao.org/fileadmin/user_upload/soils/HWSD%20Viewer/HWSD.zip
- HWSD raster at http://www.fao.org/fileadmin/user_upload/soils/HWSD%20Viewer/HWSD_RASTER.zip

Put all unzip foder in a single folder, and create a system env variable call 'HWSD_DATA' to point to this folder.


NOTE:
=====

WINDOWS:
========
In order to obtain odbc connector for the database, please install microsoft access with the version (32/64bit) in coherence with your python version.

example:
32bit => https://www.microsoft.com/fr-fr/download/details.aspx?id=13255
64bit => https://www.microsoft.com/fr-FR/download/details.aspx?id=54920

LINUX:
======
For linux users please download UcanAcess from http://ucanaccess.sourceforge.net/site.html
Unzip file in a directory and create an environement variable
UCANACESS_FILE_PATH to point to the folder UCanAccess-5.0.1.bin


DOCKER:
=======

step 1. Build docker image from dockerfile
-------------------------------------------
docker build . -t hwsd_linux_docker:0.0.1 -f .\docker\Dockerfile

step2. Execute docker image/container
-------------------------------------
docker run -p 8180:8180 hwsd_linux_docker:0.0.1

step3. Check if service is started
----------------------------------
goes at http://localhost:8180=> 'READY TO RETURN HWSD DATA' should be display

send GET request by specifying the lat long wanted => http://localhost:8180//soil_data?lat=10.2878&long=20.1234
