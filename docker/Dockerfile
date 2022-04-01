FROM continuumio/miniconda3
SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
apt-get install -y --no-install-recommends \
        openjdk-11-jre

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/openjdk-11-jre/
RUN export JAVA_HOME

ADD ./ /src/

# Install wheel of my project into container
RUN conda create -n myenv python=3.7
RUN source activate myenv && cd src && conda install --file requirements.txt

ENV UCANACESS_FILE_PATH /src/resources/
ENV HWSD_DATA /src/resources/