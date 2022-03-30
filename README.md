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
In order to obtain odbc connector for the database, please install microsoft access with the version (32/64bit) in coherence with your python version.

example:
32bit => https://www.microsoft.com/fr-fr/download/details.aspx?id=13255
64bit => https://www.microsoft.com/fr-FR/download/details.aspx?id=54920
