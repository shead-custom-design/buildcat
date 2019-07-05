.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _installation:

Installation
============

.. note::
     This section covers installing the Buildcat software on a computer;
     setting-up your Buildcat render farm requires additional work described in
     in :ref:`Design <design>` and :ref:`Setup <setup>`.

Anaconda
--------

Whether you’re new to Python or an old hand, we strongly recommend installing
`Anaconda <https://www.continuum.io/downloads>`_. Anaconda can conveniently install
Python and many of Buildcat's dependencies in your home directory, making Buildcat
setup very easy and leaving your system Python pristine.

Using Pip / Easy Install
------------------------

The best way to get the most recent stable release of Buildcat and its dependencies
is using `pip`::

    $ pip install buildcat

From Source
-----------

Finally, if you want to work with the latest, bleeding-edge Buildcat goodness,
you can install it using the source code::

    $ git clone https://github.com/shead-custom-design/buildcat
    $ cd buildcat
    $ sudo python setup.py install

The setup script installs Buildcat's required dependencies and copies Buildcat into
your Python site-packages directory, ready to go.

