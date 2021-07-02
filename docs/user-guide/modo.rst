.. image:: ../../artwork/buildcat.png
  :width: 200px
  :align: right

.. _modo:

Modo
====

To integrate Buildcat with Foundry Modo, we provide a pair of :ref:`integrations`
that can return information about a worker's local Modo installation, and
render a range of frames from a Modo .lxo file.

Installation
------------

To use the Modo integrations, each worker must be able to run the `modo_cl`
executable provided by Modo.  Typically, this means that you will have to
install Modo on the worker host, locate the `modo_cl` (or `modo_cl.exe` on
Windows) executable, and add that location to the `PATH` environment variable
before starting the worker.  See the `Modo Documentation <https://learn.foundry.com/modo/>`_
for details on where `modo_cl` is located for specific platforms.

Production
----------

To query for information about a worker's Modo installation from the command
line, use the :ref:`buildcat` command::

    $ buildcat modo-info
    {'modo': {'executable': 'modo_cl.exe', 'version': '1321'},
     'os': {'host': 'tim-aurora',
            'machine': 'x86_64',
            'processor': 'x86_64',
            'release': '4.4.0-19041-Microsoft',
            'system': 'Linux',
            'version': '#488-Microsoft Mon Sep 01 13:43:00 PST 2020'},
     'python': {'prefix': '/home/tshead/miniconda3',
                'version': '3.8.5 (default, Sep  4 2020, 07:30:14) \n[GCC 7.3.0]'},
     'worker': {'pid': 237,
                'root': '/home/tshead',
                'user': 'tshead',
                'version': '0.4.0-dev'}}

Note that `modo-info` will block until the results are received, and that
the results could vary depending on which worker handled the request.

To submit a Modo scene for rendering save the scene file and all of the
scene assets to BUILDCAT_ROOT, and ensure that all scene assets are accessed
with relative paths.

Then you can use the :ref:`buildcat` command to start rendering::

    $ buildcat modo-render path/to/scene.lxo

Note that the path to the scene file must be *relative to BUILDCAT_ROOT* ... so if
your BUILDCAT_ROOT is on a network disk `//Aurora/Farm` and your scene is stored
as `//Aurora/Farm/ProjectFoo/Scene24/Take13.lxo`, your buildcat command line would be::

    $ buildcat modo-render ProjectFoo/Scene24/Take13.lxo

By default, `modo-render` will render frame 0 of your scene.  To render a
different frame, or multiple frames, you need to specify the start (first frame
to render) and stop (one past the last frame to render) of the desired range.
So, to render frame 8::

    $ buildcat modo-render projectfoo/scene24/take13.lxo --start 8 --stop 9

Or to render frames 1-100::

    $ buildcat modo-render projectfoo/scene24/take13.lxo --start 1 --stop 101

If you wanted to render every 3rd frame, you can do that too::

    $ buildcat modo-render ProjectFoo/Scene24/Take13.lxo --start 1 --stop 101 --step 3

After starting the render, keep an eye on the contents of BUILDCAT ROOT, and you will see rendered
frames begin to appear.
