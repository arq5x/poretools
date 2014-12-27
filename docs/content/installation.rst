############
Installation
############


====================
Basic Installation
====================
.. code-block:: bash

	git clone https://github.com/arq5x/poretools
	cd poretools

Install as root:

.. code-block:: bash

	python setup.py install

Install as a plain old user who has root access:

.. code-block:: bash

	sudo python setup.py install

Install as a plain old who lacks ``sudo`` priveleges:

.. code-block:: bash

	# details: https://docs.python.org/2/install/index.html#alternate-installation-the-user-scheme
	python setup.py install --user

	# now update your PATH such that it includes the directory to which poretools was just copied.
	# look for a line in the installation log like: Installing poretools script to /home/arq5x/.local/bin
        # in this case, I would either add that path to the PATH environment variable for the current session:
        export PATH=$PATH:/home/arq5x/.local/bin

        # or, better yet add it to your .bashrc file.
        # at this point you should be able to run the poretools executable from anywhere on your system.
        poretools --help
=================================
Installing on Windows with MinKNOW installed
=================================

MinKNOW installs the Anaconda distribution of Python, which means that h5py is already installed.

However, currently MinKNOW does not update the Windows registry to specify that Anaconda is the default version of Python, which makes installing packages tricky. To address this, some changes need to be made to the registry. This can be fixed by downloading the following file:

	<https://raw.githubusercontent.com/arq5x/poretools/master/dist/poretools.reg>

Ensure it is named 'poretools.reg' and then run it (by double-clicking). Windows will prompt you about making changes to the registry, which you should agree to.

The only additional dependency that is required is rpy2 and R.

Download rpy2 from the pre-built binary page at: <http://www.lfd.uci.edu/~gohlke/pythonlibs/>. You want the version for Python 2.7 on 64-bit Windows. Run the installer.

Then, to install poretools, simply download and run the Windows installer:

        <https://github.com/arq5x/poretools/blob/master/dist/poretools-0.3.1.win-amd64.exe?raw=true>

==================================
Plotting with R on Windows
==================================

If you wish to use the R plots (experimental, on Windows) you also need to:

Download R for Windows from: <http://cran.r-project.org/bin/windows/base/>

Run the installer, then start up R and install ggplot2:

.. code-block:: R

	install.packages("ggplot2")

You need to set two environment variables to run poretools currently:

.. code-block:: bash

	set R_HOME=c:\Program Files\R\R-3.1.1
	set R_USER=c:\Users\MY USER\Documents

You may also need to add the following directory to your PATH:

.. code-block:: bash

        C:\Program Files\R\R-3.1.1\bin\x64

Instructions for updating your PATH on Windows can be found here: http://geekswithblogs.net/renso/archive/2009/10/21/how-to-set-the-windows-path-in-windows-7.aspx

=================================
Installing on OS X
=================================

First, you should install a proper package manager for OS X. In our experience, `HomeBrew <http://brew.sh/>`_ works extremely well.

To install HomeBrew, you run the following command (lifted from the HomeBrew site):

.. code-block:: bash

	ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

Using HomeBrew, install HDF5 from the HomeBrew Science "tap";

.. code-block:: bash

	brew tap homebrew/science
	brew install hdf5

You will also need Cython and numpy packages (if they are not already installed):

.. code-block:: bash

	pip install cython
	pip install numpy
	
Now, you will need to install the R statistical analysis software (you may already have this...). The `CRAN <http://cran.r-project.org/bin/macosx/>`_ website houses automatic installation packages for different versions of OS X.  Here are links to such packages for `Snow Leopard and higher <http://cran.r-project.org/bin/macosx/R-3.1.1-snowleopard.pkg>`_ as well as `Mavericks <http://cran.r-project.org/bin/macosx/R-3.1.1-mavericks.pkg>`_.

At this point, you can install poretools.

.. code-block:: bash

	git clone https://github.com/arq5x/poretools
	cd poretools

Install as an administrator of your machine:

.. code-block:: bash

	sudo python setup.py install

Install as a plain old who lacks ``sudo`` priveleges:

.. code-block:: bash

	# details: https://docs.python.org/2/install/index.html#alternate-installation-the-user-scheme
	python setup.py install --user

=================================
Installing dependencies on Ubuntu
=================================

Package dependencies

.. code-block:: bash

	sudo apt-get install git python-setuptools python-dev cython libhdf5-serial-dev

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

Build the docker container yourself (preferred):

.. code-block:: bash
	git clone https://github.com/arq5x/poretools
	cd poretools
	docker build -t poretools .
	docker run poretools --help

Or use the pre-built `image from Docker Hub <https://registry.hub.docker.com/u/stephenturner/poretools/>`_:

.. code-block:: bash

	docker pull stephenturner/poretools
	docker run stephenturner/poretools --help

To run the poretools container on data residing on the host machine, run ``docker run -h`` and look at the help for the ``-v`` option.
