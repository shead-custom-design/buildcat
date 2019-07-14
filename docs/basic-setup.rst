.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _basic-setup:

Basic Setup
===========

Follow these instructions to quickly setup a minimal-but-complete Buildcat
render farm on a single machine. Once you've gone through the process on a
single machine, the :ref:`advanced-setup` section will cover configuring a
full-fledged render farm spread across multiple machines.

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

For these examples, we'll assume that our BUILDCAT_ROOT is an external drive
on a Mac, and the path is `/Volumes/Buildcat`.

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

Next, install the Buildcat software using pip::

    $ pip install buildcat

Next, start the server::

    $ buildcat server

The server will print some startup information to the console and begin waiting
for connections::

    15455:C 05 Jul 2019 15:50:57.378 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
    15455:C 05 Jul 2019 15:50:57.378 # Redis version=5.0.3, bits=64, commit=00000000, modified=0, pid=15455, just started
    15455:C 05 Jul 2019 15:50:57.378 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
    15455:M 05 Jul 2019 15:50:57.379 * Increased maximum number of open files to 10032 (it was originally set to 256).
                    _._
               _.-``__ ''-._
          _.-``    `.  `_.  ''-._           Redis 5.0.3 (00000000/0) 64 bit
      .-`` .-```.  ```\/    _.,_ ''-._
     (    '      ,       .-`  | `,    )     Running in standalone mode
     |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
     |    `-._   `._    /     _.-'    |     PID: 15455
      `-._    `-._  `-./  _.-'    _.-'
     |`-._`-._    `-.__.-'    _.-'_.-'|
     |    `-._`-._        _.-'_.-'    |           http://redis.io
      `-._    `-._`-.__.-'_.-'    _.-'
     |`-._`-._    `-.__.-'    _.-'_.-'|
     |    `-._`-._        _.-'_.-'    |
      `-._    `-._`-.__.-'_.-'    _.-'
          `-._    `-.__.-'    _.-'
              `-._        _.-'
                  `-.__.-'

    15455:M 05 Jul 2019 15:50:57.380 # Server initialized
    15455:M 05 Jul 2019 15:50:57.380 * Ready to accept connections

Note that the server listens for connections on the loopback address -
`127.0.0.1` - by default, so we don't have to specify it explicitly.  Leave the
server running, and open another command line console to run the next set of
commands.

Worker
------

Now we're ready to run a worker.  Since we already installed Buildcat in the
previous step, there's nothing to do except fire it up::

    $ cd /Volumes/Buildcat
    $ buildcat worker

The worker will print a startup message, begin communicating with the server,
and wait for jobs to work on::

    16:11:42 RQ worker 'rq:worker:b9031b3c338b4307b9764fe36e7de13a' started, version 1.0
    16:11:42 *** Listening on default...

Note that we didn't have to specify the server address because the worker
defaults to `127.0.0.1` too.  Also, before starting the worker we changed the
working directory to BUILDCAT_ROOT.  This way, the worker knows where
BUILDCAT_ROOT is located, without having to configure it.  Like before, leave
the worker running and open another command line for the following steps.

Testing
-------

Now it's time to test the farm.  To keep things simple, we're going to send a
command to the server from the command line, as this is the easiest way to
ensure that everything's working::

    $ buildcat ping

This command submits a `buildcat.test.ping` job to the server, which hands it off to any
available worker.  If you check the console where we left our worker running, you'll see that it
accepted the job and ran it::

    21:52:49 default: buildcat.test.ping() (4b5c9b65-03ec-48f1-95b8-7c382604a0d3)
    21:52:49 default: Job OK (4b5c9b65-03ec-48f1-95b8-7c382604a0d3)
    21:52:49 Result is kept for 500 seconds

... and in the console where you sent the command, some information about the worker
is printed out::

    {'host': 'aurora.local', 'user': 'fred', 'root': '/Volumes/Buildcat', 'pid': 52928}

This confirms that the client, server, and worker are all communicating and
ready to render.

Summary
-------

That's it!  Your single-machine render farm is up-and-running.  Of course,
there are many details we've skipped in this section, such as how to submit
render jobs from your DCC client and how to start the farm automatically when
your machine boots.  In the :ref:`next section <advanced-setup>` we'll make
suggestions on how to setup a multi-machine farm and handle boot time startup,
and the section on :ref:`integrations <integrations>` will cover how to use
Buildcat with specific DCC tools.
