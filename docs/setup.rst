.. _setup:

.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

Setup
=====

Follow these instructions to quickly setup a minimal-but-complete Buildcat
render farm on a single machine. Once you've gone through the process on a
single machine, you'll be ready to setup a full-fledged render farm spread
across multiple machines.

.. tip::
    Make sure you read :ref:`design` and understand how the parts of a Buildcat
    farm work together before you start!

Shared Storage
--------------

The first step in setting-up your render farm will be to create or choose a
filesystem location for the shared storage space.  Throughout this
documentation we will refer to this location as BUILDCAT_ROOT.  Keep in mind
that BUILDCAT_ROOT must have enough storage for your projects, their assets
(geometry, textures, simulations, etc), and all of their rendered outputs, so
you'll want to pick a location on a disk with as much free space as possible.

For these examples, we'll assume that our BUILDCAT_ROOT is `/Volumes/Buildcat`.

Network Communication
---------------------

The next step in setting-up a render farm is identifying how your server, workers,
and clients will communicate with one another.  In particular, you need to know
the network address of the machine running your server.

Since our sample render farm will be running on one machine, we'll use the
loopback address - `127.0.0.1` as our server address throughout the rest of
this section.

Anaconda
--------

Now that we've selected BUILDCAT_ROOT and our network address, it's time to start
installing software.  We'll need Python and all of Buildcat's other dependencies.
Getting all of the pieces in place (and dealing with different platforms) is one of
the things that makes installing render farm software difficult.

Instead, whether you’re new to Python or an old hand, we strongly recommend
installing `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_, a
minimalist subset of Anaconda.  Anaconda is a portable (OSX, Linux, and
Windows) Python distribution that you can use to conveniently install Python in
your home directory.  This is incredibly useful because installing the rest of
Buildcat's dependencies is easy and consistent across platforms, and you will
be leaving your system-provided Python in pristine condition.

The remainder of this documentation will assume that you have Anaconda
installed.  You can still obtain Buildcat's dependencies using other methods,
but you'll need to handle those details on your own.

Server
------

Now we're ready to install the Buildcat (Redis) server from a command line,
using Anaconda::

    $ conda install redis

Next, start Redis::

    $ redis-server

The Redis server will print some startup information to the console and wait
for connections.  Note that Redis listens for connections on the loopback
address - `127.0.0.1` - by default, so we don't have to specify the network
address we choose earlier.  Leave Redis running, and open another command line
console to run the next set of commands.

Worker
------

Now we're ready to setup a worker.  First, we need to install the Python
client software for Redis, so our worker can communicate with the server.
Again, we'll use Anaconda to get it::

    $ conda install redis-py

Second, we'll install the RQ software that actually provides the worker process::

    $ pip install rq

(`pip` is a tool for installing Python software that's provided by Anaconda).

Next, we need to install the Buildcat software, which adds render-farm-specific
functionality to the vanilla RQ workers.  The following will install the most
recent stable release of Buildcat::

    $ pip install buildcat

Alternatively, if you're feeling lucky and want to use the latest,
bleeding-edge Buildcat goodness, you can install from source code::

    $ git clone https://github.com/shead-custom-design/buildcat
    $ cd buildcat
    $ python setup.py install

Finally, we're ready to run a worker::

    $ cd /Volumes/Buildcat
    $ rq worker -w buildcat.worker.Worker

The worker will print a startup message, begin communicating with the server,
and wait for jobs to work on.  Once again, leave the worker running and open
another command line console for the following steps.  Note that, before
starting the worker, we changed the working directory to BUILDCAT_ROOT.  This
way, the worker knows where BUILDCAT_ROOT is located, without having to
configure it, mess with registry entries, etc.

