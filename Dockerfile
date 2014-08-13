###############################################
# Dockerfile to build poretools container image
# Based on Ubuntu 14.04
# Build with:
#   sudo docker build -t poretools .
###############################################

# Use ubuntu 14.04 base image
FROM ubuntu:14.04

# set non-interactive mode
ENV DEBIAN_FRONTEND noninteractive

############# BEGIN INSTALLATION ##############

# Prepare to install R
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
RUN echo 'deb http://cran.rstudio.com/bin/linux/ubuntu trusty/' >> /etc/apt/sources.list
RUN apt-get update

# Install dependencies
RUN apt-get -y install git python-tables python-setuptools python-pip python-dev cython libhdf5-serial-dev r-base python-rpy2

# Upgrade numexpr
RUN pip install numexpr --upgrade

# Install R packages
RUN Rscript -e 'options("repos" = c(CRAN = "http://cran.rstudio.com/")); install.packages("codetools"); install.packages("MASS"); install.packages("ggplot2")'

# Install poretools
RUN git clone https://github.com/arq5x/poretools /tmp/poretools
RUN cd /tmp/poretools && python setup.py install

############## INSTALLATION END ##############

# Set entrypoint so container can be used as executable
ENTRYPOINT ["poretools"]

# File author/maintainer info
MAINTAINER Stephen Turner <lastname at virginia dot edu>
