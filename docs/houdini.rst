.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _houdini:

Houdini
=======

To integrate Buildcat with SideFX Houdini, we provide a special "Buildcat" ROP
node that can communicate with the Buildcat server.  To use the Buildcat ROP,
you'll need to run Houdini on a machine that has network access to the Buildcat
server and access to the Buildcat networkshared storage directory, just like
a worker.  Furthermore, you'll need to perform the following one-time installation.

Installation
------------

First, you'll need to make the `redis` and `rq` Python libraries accessible to
Houdini.  This is slightly complicated by the fact that Houdini uses Python 2.7.
If you're using Anaconda (strongly recommended), you can create a special Python 2.7
environment with both libraries, for use in Houdini::

    $ conda create -n python27 python=2

Now that you've created an environment named `python27`, activate it and
install the libraries just as you did on your workers::

    $ conda activate python27
    $ pip install redis-py
    $ pip install rq

Then, you'll need to configure Houdini so it can find the newly-installed
libraries.  To locate the directory where they were installed, run Python
with the `python27` environment still active, and print out the Python search
paths::

    $ python
    >>> import pprint, sys
    >>> pprint.pprint(sys.path)
    ['',
     '/Users/fred/miniconda3/envs/python27/lib/python27.zip',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7/plat-darwin',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7/plat-mac',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7/plat-mac/lib-scriptpackages',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7/lib-tk',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7/lib-old',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7/lib-dynload',
     '/Users/fred/miniconda3/envs/python27/lib/python2.7/site-packages']

Look for the path that ends with `/site-packages`, which in this case is
`/Users/fred/miniconda3/envs/python27/lib/python2.7/site-packages`.  This is
where the `redis` and `rq` packages were just installed.  To configure Houdini
to find them, you'll have to edit your `houdini.env` file, setting the
environment variable PYTHONPATH to the site-packages directory (see
https://www.sidefx.com/docs/houdini/basics/config_env.html for details on
setting environment variables for various platforms).  Following the above
example you might put the following in your `houdini.env`::

    PYTHONPATH = /Users/fred/miniconda3/envs/python27/lib/python2.7/site-packages

While you're editing `houdini.env`, it is also a good idea to configure your
BUILDCAT_ROOT, by setting an environment variable of the same name, pointing
to your shared storage directory::

    BUILDCAT_ROOT = /Volumes/Buildcat

Finally, you'll need to install the digital asset file containing the Buildcat
ROP. You can put it in any empty directory you like, using a command-line console::

    $ mkdir ~/integrations
    $ cd ~/integrations
    $ buildcat-install
    INFO:buildcat-install:Copying files from /Users/tshead/src/buildcat/buildcat/integrations
    INFO:buildcat-install:Copying houdini/demo.hiplc
    INFO:buildcat-install:Copying houdini/scd__buildcat.hdalc
    INFO:buildcat-install:Installation complete.

Now, the next time you start Houdini, you'll be ready to use Buildcat!

Production
----------

To submit a Houdini scene to Buildcat for rendering, save the scene file in
BUILDCAT_ROOT, and ensure that all of the scene assets are stored in
BUILDCAT_ROOT, and accessed with relative paths (for example, relative to
$HIP).  Use Houdini's `Render > Pre-Flight Scene ...` menu item to check your
asset locations.

Next, you'll need to load the Buildcat digital asset into your scene.  Use the
`Assets > Install Digital Asset Library` menu to select the
`scd__buildcat.hdalc` file you installed above.

Now create an instance of the `Buildcat Render` ROP in an output context, and
connect an output ROP to the input of the Buildcat ROP node.  Set the `Server
URI` parameter to point to your Buildcat server.  The `Buildcat Root` parameter
defaults to the $BUILDCAT_ROOT environment variable that we set earlier (or you
can point it elsewhere if you opted not to set $BUILDCAT_ROOT).  Set the
`Start / End / Inc` parameters to define the range of frames to render, and
press `Submit Job` and your job will start!  Keep an eye on the contents of
BUILDCAT ROOT, and you should see rendered frames begin to appear.
