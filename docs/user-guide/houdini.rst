.. image:: ../../artwork/logo.png
  :width: 200px
  :align: right

.. _houdini:

Houdini
=======

To integrate Buildcat with SideFX Houdini, we provide :ref:`integrations` to
return information about a worker's local Houdini installation, render a range
of frames from a Houdini .hip file, and render an .ifd file.

Installation
------------

To use the Houdini integrations, each worker must be able to run the `hython`
and `mantra` executables provided by Houdini.  Typically, this means that you
will have to install Houdini on the worker host, locate the `hython` and
`mantra` (or `hython.exe` and `mantra.exe` on Windows) executables, and add
that location to the `PATH` environment variable before starting the worker.
See the `Houdini Documentation <https://www.sidefx.com/docs/>`_ for details on
where `hython` and `mantra` are located for specific platforms.

To submit a Houdini scene for rendering, save the scene file and all of the
scene assets to BUILDCAT_ROOT, and ensure that all scene assets are accessed
using relative paths (for example, relative to $HIP), *including output files*.
Use Houdini's `Render > Pre-Flight Scene ...` menu item to double check your
asset locations.  It's important that *every* input or output for your project
is contained within BUILDCAT_ROOT.

Command Line Integration
------------------------

To query for information about a worker's Houdini installation from the command
line, use the :ref:`buildcat` command::

    $ buildcat houdini-info
    {'houdini': {'executable': 'hython.exe', 'version': '18.5.408'},
     'os': {'host': 'tim-aurora',
        'machine': 'x86_64',
        'processor': 'x86_64',
        'release': '4.4.0-19041-Microsoft',
        'system': 'Linux',
        'version': '#488-Microsoft Mon Sep 01 13:43:00 PST 2020'},
     'python': {'prefix': '/home/tshead/miniconda3',
                'version': '3.8.5 (default, Sep  4 2020, 07:30:14) \n[GCC 7.3.0]'},
     'worker': {'pid': 225,
                'root': '/home/tshead',
                'user': 'tshead',
                'version': '0.4.0-dev'}}


Keep in mind that `houdini-info` will block until a worker handles the request, and that the results will vary depending on which worker does so.

Next, you can use the :ref:`buildcat` command to render a .hip file::

    $ buildcat houdini-render-hip path/to/scene.hip

Note that the path to the .hip file must be *relative to BUILDCAT_ROOT* ... so if
your BUILDCAT_ROOT is on a network disk `//aurora/farm` and your scene is stored
as `//aurora/farm/projectfoo/scene24/take13.hip`, your buildcat command line would be::

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip

By default, the `houdini-render-hip` subcommand will render frame 1 of your
scene.  To render a different frame, just specify it after the hip file::

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 8

Or to render all of the frames between 1-100 (inclusive)::

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 1-100

If you want to render every 3rd frame, you can do that too::

    $ buildcat houdini-render-hip projectfoo/scene24/Take13.hip --frames 1-100:3

You can combine as many individual frames and ranges as you like, using commas::

    $ buildcat houdini-render-hip projectfoo/scene24/Take13.hip --frames 1,7,9,10-25,75-100:2

Be aware that `houdini-render` assumes that your .hip file has a ROP node named `/out/mantra_ipr` that it
will use for the render. If you want to render with some other ROP, you'll need to specify that too::

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 1-100 --rop /out/mantra1

After starting the render, keep an eye on the contents of BUILDCAT_ROOT, and you will see rendered
frames begin to appear.

Parallelism
~~~~~~~~~~~

A limitation of `houdini-render-hip` is that it renders frames one-after-the-other
as a single job. This is what you want if you're caching the results of a
simulation or other geometry to a disk, but won't help speed up rendering if
you want to render frames simultaneously on multiple machines.  To do that,
there are several possible alternatives:

On one hand, you could submit multiple jobs with `houdini-render-hip` that each
render a subset of frames.  For example, if you had two machines with similar
resources, you might split your job into two::

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 1-50 --rop /out/mantra1
    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 51-100 --rop /out/mantra1

As long as you have a worker waiting on each machine, both jobs will run simultaneously, and the render should complete in roughly half the time.  Note
that this can be an efficient approach because the `hython` processes that do
the work only have to be started and stopped once.

On the other hand, the above approach can be suboptimal if your machines have
mismatched capabilities - if you split the job into equal halves, but one
machine is faster than the other, it will quickly complete its half and sit
idle until the slower machine eventually finishes its half; in this case, it would be
better if the render is *load balanced*, so both machines can work at their full
capacity, and finish at roughly the same time.  To accomplish this, you can submit
one job per frame::

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 1 --rop /out/mantra1
    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 2 --rop /out/mantra1
    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 3 --rop /out/mantra1

    ...

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 100 --rop /out/mantra1

Because this approach creates many small jobs, there is more overhead from
`hython` processes starting and stopping, but both machines can complete
as many jobs as their resources allow.

The downside to either approach is that every worker that's rendering a .hip
file consumes a full Houdini license while it runs.  Depending on how many
workers you have, you may be prevented from using Houdini during rendering, or
you may run out of licenses altogether, and overcoming this requires a more complicated approach:

First, create a Mantra ROP in your .hip file that writes .ifd files to disk, instead of rendering.  As always, make sure the .ifd files and temp storage directories are located within $BUILDCAT_ROOT.

Second, start a job that renders the .ifd-generating ROP in your scene::

    $ buildcat houdini-render-hip projectfoo/scene24/take13.hip --frames 1-100 --rop /out/generate_ifds

Finally, submit jobs to render each of the .ifd files::

    $ buildcat houdini-render-ifd projectfoo/scene24/ifds/take13-0001.ifd
    $ buildcat houdini-render-ifd projectfoo/scene24/ifds/take13-0002.ifd
    $ buildcat houdini-render-ifd projectfoo/scene24/ifds/take13-0003.ifd

    ...

    $ buildcat houdini-render-ifd projectfoo/scene24/ifds/take13-0100.ifd

Now, a Houdini license is only consumed while the .ifd files are generated by
the first job.  The remaining jobs render a single .ifd file apiece and each consume
a single `mantra` license while rendering, allowing you to render with as many workers as you
have render licenses, and continue using Houdini while they work.

Scripted Integration
--------------------

Instead of using the command line, you might want Houdini to automatically
submit Buildcat jobs for you.  For example, if you have a ROP that generates
.ifd files as described above, it's useful to have the ROP submit a job for
each .ifd file as soon as it's written to disk, so rendering can begin
immediately, instead of idling workers while .ifd generation completes.  To do so, add a Python Post-Frame Script to your .ifd-generating
ROP, with contents along the lines of the following::

    import os

    import hou
    import redis
    import rq

    filename = os.path.relpath(hou.ch("soho_diskfile"), hou.getenv("HIP"))

    queue = rq.Queue(connection=redis.Redis())
    queue.enqueue("buildcat.hou.render_ifd", filename)

Now when you generate the .ifd files, render jobs will be automatically created.
Note that this script assumes that you use the $HIP environment variable to
anchor the .ifd and temporary storage paths, and that $HIP refers to the same
location as BUILDCAT_ROOT.  It also assumes that you've configured Houdini to
load the `redis` and `rq` Python modules from an external location (these modules
are not provided by Houdini).


