.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _installation:

Installation
============

Using a Package Manager
-----------------------------

A package manager (conda, apt, yum, MacPorts, etc) should generally be your
first stop for installing Buildcat - it will make it easy to install Buildcat and
its dependencies, keep them up-to-date, and even (gasp!) uninstall them
cleanly.  If your package manager doesn't support Buildcat yet, drop them a line
and let them know you'd like them to add it!

If you're new to Python or unsure where to start, we strongly recommend taking
a look at :ref:`Anaconda <anaconda-installation>`, which the Buildcat developers
use during their day-to-day work.

.. toctree::
  :maxdepth: 2

  anaconda-installation.rst

Using Pip / Easy Install
------------------------

If your package manager doesn't support Buildcat, or doesn't have the latest
version, your next option should be Python setup tools like `pip`.  You can
always install the latest stable version of Buildcat and its required
dependencies using::

    $ pip install buildcat

... following that, you'll be able to use all of Buildcat's features.

.. _From Source:

From Source
-----------

Finally, if you want to work with the latest, bleeding-edge Buildcat goodness,
you can install it using the source code::

    $ git clone https://github.com/shead-custom-design/buildcat
    $ cd buildcat
    $ sudo python setup.py install

The setup script installs Buildcat's required dependencies and copies Buildcat into
your Python site-packages directory, ready to go.

