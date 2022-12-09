.. image:: ../artwork/logo.png
  :width: 200px
  :align: right

.. _installation:

Installation
============

Buildcat
--------

To install the latest stable version of Buildcat and its dependencies, use `pip`::

    $ pip install buildcat

... once it completes, you'll be able to use all of Buildcat's core features.

Redis
-----

To run a buildcat server, you'll also need `Redis <https://redis.io>`_
which can't be installed via
pip.  If you use `Conda <https://docs.conda.io/en/latest/>`_ (which we strongly
recommend), you can install it as follows::

    $ conda install redis

Once you have Redis, you can install Buildcat and the rest of its dependencies::

    $ pip install buildcat

.. _documentation:

Documentation
-------------

We assume that you'll normally access this documentation online, but if you
want a local copy on your own computer, do the following:

Install Buildcat along with all of the dependencies needed to build the docs::

    $ pip install buildcat[doc]

Next, do the following to download a tarball to the current directory
containing all of the Buildcat source code, which includes this documentation::

    $ pip download buildcat --no-binary=:all: --no-deps

Now, you can extract the tarball contents and build the documentation (adjust the
following for the version you downloaded)::

    $ tar xzvf buildcat-0.6.1.tar.gz
    $ cd buildcat-0.6.1/docs
    $ make html
