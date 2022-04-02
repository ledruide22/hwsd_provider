FROM continuumio/miniconda3
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y unzip

RUN mkdir resources

RUN cd resources && wget http://www.fao.org/fileadmin/user_upload/soils/HWSD%20Viewer/HWSD.zip \
&& unzip HWSD.zip -d HWSD && rm HWSD.zip
RUN cd resources && wget http://www.fao.org/fileadmin/user_upload/soils/HWSD%20Viewer/HWSD_RASTER.zip \
&& unzip HWSD_RASTER.zip -d HWSD_RASTER && rm HWSD_RASTER.zip
RUN cd resources && wget https://sourceforge.net/projects/ucanaccess/files/latest/download/UCanAccess-5.0.1.bin.zip \
&& unzip UCanAccess-5.0.1.bin.zip && rm UCanAccess-5.0.1.bin.zip

FROM continuumio/miniconda3
ENV LANG C.UTF-8

ADD ./ /src/

SHELL ["/bin/bash", "-c"]


# Create a wheel of my project
RUN conda create -n myenv python=3.7 wheel
RUN source activate myenv && cd /src && python setup.py bdist_wheel

FROM continuumio/miniconda3
SHELL ["/bin/bash", "-c"]

COPY --from=0 /resources/ /src/resources/
ENV UCANACESS_FILE_PATH /src/resources/
RUN export UCANACESS_FILE_PATH

COPY --from=1 /src/dist/*.whl /opt/hwsd_provider/
ENV HWSD_DATA /src/resources/
RUN export HWSD_DATA


# Install wheel of my project into container
RUN conda create -n myenv python=3.7
#RUN source activate myenv && conda install 'gdal>=3.0,<3.1' 'pyodbc>=4.0,<4.1' 'rasterio>=1.1,<1.2' 'jaydebeapi>=1.2,<1.3'
RUN source activate myenv && conda install gdal pyodbc rasterio jaydebeapi
RUN source activate myenv &&  pip install --no-cache-dir /opt/hwsd_provider/hwsd_provider-0.0.1-py3-none-any.whl

## Install Java to use ms db connector
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-11-jre

## Setup JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/openjdk-11-jre/
RUN export JAVA_HOME