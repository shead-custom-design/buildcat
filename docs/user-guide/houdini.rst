.. image:: ../../artwork/buildcat.png
  :width: 200px
  :align: right

.. _houdini:

Houdini
=======

To integrate Buildcat with SideFX Houdini, we provide a pair of :ref:`integrations`
that can return information about a worker's local Houdini installation, and
render a range of frames from a Houdini .hip file.

Installation
------------

To use the Houdini integrations, each worker must be able to run the `hython`
executable provided by Houdini.  Typically, this means that you will have to
install Houdini on the worker host, locate the `hython` (or `hython.exe` on
Windows) executable, and add that location to the `PATH` environment variable
before starting the worker.  See https://www.sidefx.com/docs/houdini/hom/commandline.html#hython
for details on how to locate `hython`.

Production
----------

To query for information about a worker's Houdini installation from the command
line, use the :ref:`buildcat` command::

    $ buildcat houdini-info
    {'houdini': {'executable': 'hython', 'version': '18.5.408'}}

Note that `houdini-info` will block until the results are received, and that
the results could vary depending on which worker handled the request.

To submit a Houdini scene for rendering save the scene file and all of the
scene assets to BUILDCAT_ROOT, and ensure that all scene assets are accessed
with relative paths (for example, relative to $HIP).  Use Houdini's
`Render > Pre-Flight Scene ...` menu item to double check your asset locations.

Then you can use the :ref:`buildcat` command to start rendering::

    $ buildcat houdini-render path/to/scene.hip

Note that the path to the scene file must be *relative to BUILDCAT_ROOT* ... so if
your BUILDCAT_ROOT is on a network disk `//Aurora/Farm` and your scene is stored
as `//Aurora/Farm/ProjectFoo/Scene24/Take13.hip`, your buildcat command line would be::

    $ buildcat houdini-render ProjectFoo/Scene24/Take13.hip

By default, `houdini-render` will render frame 0 of your scene.  To render a
different frame, or multiple frames, you need to specify the start (first frame
to render) and stop (one past the last frame to render) of the desired range.
So, to render frame 8::

    $ buildcat houdini-render projectfoo/scene24/take13.hip --start 8 --stop 9

Or to render frames 1-100::

    $ buildcat houdini-render projectfoo/scene24/take13.hip --start 1 --stop 101

If you wanted to render every 3rd frame, you can do that too::

    $ buildcat houdini-render ProjectFoo/Scene24/Take13.hip --start 1 --stop 101 --step 3

Also by default, `houdini-render` assumes that you have a ROP named `/out/mantra_ipr` to control
the render.  If you want to render with some other ROP, you have to specify it too::

    $ buildcat houdini-render ProjectFoo/Scene24/Take13.hip --start 1 --stop 101 --rop /out/beauty_pass_ipr

After starting the render, keep an eye on the contents of BUILDCAT ROOT, and you will see rendered
frames begin to appear.
