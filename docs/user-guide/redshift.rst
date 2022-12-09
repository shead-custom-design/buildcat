.. image:: ../../artwork/logo.png
  :width: 200px
  :align: right

Redshift
========

To integrate Buildcat with `Redshift <https://redshift3d.com>`_, we provide a
pair of :ref:`integrations` that can return information about a worker's local
Redshift installation, and render an image from a Redshift .rs file.

Installation
------------

To use the Redshift integrations, each worker must be able to run the `redshiftCmdLine`
executable provided by Redshift.  Typically, this means that you will have to
install Redshift on the worker host, locate the `redshiftCmdLine` (or `redshiftCmdLine.exe` on
Windows) executable, and add that location to the `PATH` environment variable
before starting the worker.  See the `Redshift Documentation <https://docs.redshift3d.com>`_
for details on where the `redshiftCmdLine` executable is located on specific platforms.

Production
----------

To query for information about a worker's Redshift installation from the command
line, use the :ref:`buildcat` command::

    $ buildcat redshift-info
    {'os': {'host': 'tim-aurora',
            'machine': 'x86_64',
            'processor': 'x86_64',
            'release': '4.4.0-19041-Microsoft',
            'system': 'Linux',
            'version': '#488-Microsoft Mon Sep 01 13:43:00 PST 2020'},
     'python': {'prefix': '/home/tshead/miniconda3',
                'version': '3.8.5 (default, Sep  4 2020, 07:30:14) \n[GCC 7.3.0]'},
     'redshift': {'executable': 'redshiftCmdLine.exe',
                  'version': b'Redshift Command-Line Renderer (version 3.0.45 - API'
                             b': 3027) Copyright 2021 Redshift Rendering Technologi'
                             b'es '},
     'worker': {'pid': 302,
                'root': '/home/tshead',
                'user': 'tshead',
                'version': '0.4.0-dev'}}

Note that `redshift-info` will block until the results are received, and that
the results could vary depending on which worker handled the request.

To submit a Redshift scene for rendering save the scene file and all of the
scene assets to BUILDCAT_ROOT, and ensure that all scene assets can be accessed
with relative paths.

Then you can use the :ref:`buildcat` command to render an image::

    $ buildcat redshift-render path/to/scene.rs

Note that the path to the scene file must be *relative to BUILDCAT_ROOT* ... so if
your BUILDCAT_ROOT is on a network disk `//Aurora/Farm` and your scene is stored
as `//Aurora/Farm/ProjectFoo/Scene24/Take13.rs`, your buildcat command line would be::

    $ buildcat redshift-render ProjectFoo/Scene24/Take13.rs

After starting the render, keep an eye on the contents of BUILDCAT ROOT, and
you should see the rendered frame appear.
