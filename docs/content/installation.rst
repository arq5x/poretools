############
Installation
############


====================
Basic Installation
====================
.. code-block:: bash

	git clone https://github.com/arq5x/poretools
	cd poretools
	python setup.py install
	# or
	sudo python setup.py install


=================================
Installing on Windows
=================================
To do.


=================================
Installing dependencies on Ubuntu
=================================

Package dependencies

.. code-block:: bash

	sudo apt-get install git python-tables python-setuptools python-pip python-dev cython libhdf5-serial-dev

Then install R 3.0, this requires a bit of hacking. You need to replace 'precise' with the appropriate version if you are on a different Ubuntu version, see <http://cran.r-project.org/bin/linux/ubuntu/README> for more details.

.. code-block:: bash

	sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9

Open in a text editor (as sudo) the file ``/etc/apt/sources.list`` and add the following line to the bottom, for Ubuntu 12.04:

.. code-block:: bash

	deb http://www.stats.bris.ac.uk/R/bin/linux/ubuntu precise/

Or, for Ubuntu 14.04:

.. code-block:: bash

	deb http://www.stats.bris.ac.uk/R/bin/linux/ubuntu trusty/ 

Then, run the following commands to install R 3.0:

.. code-block:: bash

	sudo apt-get update
	sudo apt-get install r-base python-rpy2

Start R

.. code-block:: bash

	R

Then run the following commands within the R programme, and follow any prompts:

.. code-block:: R

	options("repos" = c(CRAN = "http://cran.rstudio.com/"))
	install.packages("codetools")
	install.packages("MASS")
	install.packages("ggplot2")

Then install poretools, finally:

.. code-block:: bash

	sudo pip install numexpr --upgrade
	git clone https://github.com/arq5x/poretools
	cd poretools
	sudo python setup.py install
	poretools

============
In the cloud
============

Amazon Web Services machine image ID: ami-4c0ec424

==========
Via docker
==========

Using the [docker image](https://registry.hub.docker.com/u/stephenturner/poretools/)

.. code-block:: bash

	docker pull stephenturner/poretools
	docker run stephenturner/poretools poretools --help
