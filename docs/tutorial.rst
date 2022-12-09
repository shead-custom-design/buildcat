.. image:: ../artwork/logo.png
  :width: 200px
  :align: right

.. _tutorial:

Tutorial
========

We created Buildcat because we were frustrated with the complexity and builtin
assumptions of other render farms.  Buildcat is written in Python for
portability, simplicity, and flexibility.  It runs on MacOS, Linux, and Windows
(using WSL), requires little-to-no configuration, and uses existing open source
software wherever possible instead of reinventing wheels.

We strongly recommend you follow this tutorial to quickly setup a
minimal-but-complete Buildcat render farm on a single machine. It's quick and
easy, and once you've done it on one machine, you'll have a good feel for the
process.  Then, individual articles in the :ref:`user_guide` will
discuss how to setup a full-fledged render farm deployed on multiple
hosts.

.. tip::
    While Buildcat is as simple as we could possibly make it, there are still
    many moving parts in a render farm - make sure you read and  understand the
    following description of how the parts of a Buildcat farm work together
    before you start!

Your Buildcat render farm will have all of the following:

Server
    The server keeps track of your render jobs, dispatching them to
    workers as the workers become available.  In Buildcat, the server
    is actually an instance of the widely used open source `Redis <https://redis.io>`_
    key-value store.

Workers
    Workers are the processes that carry out the actual work of rendering.
    Idle workers receive jobs from the server and execute commands with your
    DCC tools, typically (but not necessarily) instructions to render an image
    from an animation.  Buildcat workers are actually instances of `RQ <https://python-rq.org>`_
    workers executing Buildcat integrations written for rendering.

Integrations
    Integrations are the DCC-tool-specific code provided by Buildcat for
    rendering.  Technically, integrations are Python functions that are called
    when a job is executed by a worker.  You can easily use your own functions
    with Buildcat workers, written to work with your own tools for any purpose,
    not just rendering.

Clients
    Clients submit jobs to the server to be rendered by workers.  Any Python
    code can use the `RQ <https://python-rq.org>`_ API to submit a job to the
    server, and Buildcat provides API to make job submissions even easier.
    Buildcat also provides a command-line client that can be used to submit
    jobs using any of Buildcat's builtin integrations.  Using the API or the
    command line tool, jobs can  be submitted from within your DCC tool using
    scripting.

Shared Storage.
    Typically, a render job includes just the name of a scene file and a range
    of frames to render. To run the job, your workers must have access to the
    scene file and all of the assets it uses, including geometry, cached
    simulations, textures, and-so-on.  Typically, this means setting up a network
    share that all of the workers can reach.  It also means that artists will need
    to ensure that scene files and assets are moved to this location prior to job
    submission.

Network Connectivity.
    To function, all clients and all workers must be able to communicate with the
    server.


.. note::
    The server, workers, and clients in your Buildcat render farm can be run on any
    combination of hosts, including any mixture of platforms.


Platform Notes
--------------

Now you're ready to run through the tutorial.  In the sections that follow, we
will put platform-specific information in tabs, as you see here ... please choose
the tab for your platform before proceeding:

.. tabs::

   .. group-tab:: Linux

      You made the right choice! Proceed to the next section.

   .. group-tab:: MacOS

      You made the right choice! Proceed to the next section.

   .. group-tab:: Windows

      Due to platform limitations, Buildcat workers currently won't run on
      Windows.  However, you can use the `Windows Subsystem for Linux (WSL) <https://docs.microsoft.com/en-us/windows/wsl>`_
      to setup a very lightweight Linux VM on your Windows machine and run all
      of Buildcat's tools there.

      To install WSL, choose Start > Microsoft Store, and install "Ubuntu".  Once you've
      installed Ubuntu and enabled WSL using the instructions in the Microsoft Store app,
      you can continue on to the next section.

      .. note::

        Throughout the rest of this documentation, all references to a "command
        line" mean the WSL Ubuntu command line, **not** the Windows command
        prompt, Power Shell, or other Windows-specific shells.

Shared Storage
--------------

The first step in setting-up your render farm will be to create or choose a
filesystem location for the shared storage space.  Throughout this
documentation we will refer to this location as BUILDCAT_ROOT.  Keep in mind
that BUILDCAT_ROOT must have enough storage for your projects, their assets
(geometry, textures, simulations, etc), and all of their rendered outputs, so
you'll want to pick a location on a disk with as much free space as possible.

.. tabs::

   .. group-tab:: Linux

      For these examples, we'll assume that BUILDCAT_ROOT is located in an
      external drive mounted on the path `/mnt/farm`.

   .. group-tab:: MacOS

      For these examples, we'll assume that BUILDCAT_ROOT is an
      external drive named `Farm` and accessible from the path `/Volumes/Farm`.

   .. group-tab:: Windows

      For these examples, we'll assume that BUILDCAT_ROOT is located on the
      Windows D: drive in a folder named `farm`.  To access Windows files within
      WSL, you use the path `/mnt/<drive letter>/<folder>/...`, or in this case:
      `/mnt/d/farm`.

Network Communication
---------------------

The next step in setting-up any render farm is knowing how your server, workers,
and clients will communicate with one another.  In particular, you need to know
the network address of the machine running your server.

Since our sample render farm will be running on one machine, we'll use the
loopback address - `127.0.0.1` - as our server address throughout the rest of
this section.

Anaconda
--------

Now that we've selected BUILDCAT_ROOT and our network address, it's time to start
installing software.  We'll need Python and all of Buildcat's other dependencies.
Getting all of the pieces in place (and dealing with different platforms) is one of
the things that makes installing render farm software difficult.

Instead, whether you’re new to Python or an old hand, we strongly recommend
installing `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_, a
minimalist subset of Anaconda.  Anaconda is a portable (MacOS, Linux, and
Windows) Python distribution that you can use to conveniently install Python in
your home directory.  This is incredibly useful because installing the rest of
Buildcat's dependencies is easy and consistent across platforms, you get access
to the latest versions of Python and related software, and your separate Anaconda
install leaves your system-provided Python in pristine condition.

The remainder of this documentation will assume that you have Anaconda
installed.  You can still obtain Buildcat's dependencies using other methods,
but you'll need to handle those details on your own.

.. tabs::

   .. group-tab:: Linux

      Use the "Python 3.9 Miniconda3 Linux 64-bit" installer from
      https://docs.conda.io/en/latest/miniconda.html to install Anaconda in
      your home directory.

   .. group-tab:: MacOS

      Use the "Python 3.9 Miniconda3 MacOSX 64-bit" installer from
      https://docs.conda.io/en/latest/miniconda.html to install Anaconda in
      your home directory.

   .. group-tab:: Windows

      Use the **"Python 3.9 Miniconda3 Linux 64-bit"** installer from
      https://docs.conda.io/en/latest/miniconda.html to install Anaconda in
      your **WSL** home directory.  Note that this isn't a typo: you're
      installing Anaconda **for Linux** in WSL, not Anaconda for Windows.


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
previous step, there's nothing to do except fire it up:

.. tabs::

   .. group-tab:: Linux

        .. code-block:: bash

           $ cd /mnt/farm
           $ buildcat worker

   .. group-tab:: MacOS

        .. code-block:: bash

           $ cd /Volumes/Farm
           $ buildcat worker

   .. group-tab:: Windows

        .. code-block:: bash

           $ cd /mnt/d/farm
           $ buildcat worker

The worker will print a startup message, begin communicating with the server,
and wait for jobs to work on::

    13:23:51 Worker rq:worker:87138a93131c4b33a2ebe7d8a3c9c528: started, version 1.7.0
    13:23:51 Subscribing to channel rq:pubsub:87138a93131c4b33a2ebe7d8a3c9c528
    13:23:51 *** Listening on default...
    13:23:51 Cleaning registries for queue: default

Note that we didn't have to specify the server address because it defaults to
to `127.0.0.1` for the worker, too.  Also, before starting the worker we used
the `cd` command to change the working directory to BUILDCAT_ROOT.  This is how
the worker knows where BUILDCAT_ROOT is located without having to configure it.
Leave the worker running and open another command line for the following steps.

Client
------

Now it's time to test the farm, by submitting a job to the server.  To keep
things simple, we're going to use Buildcat's builtin command line client, as
this is the easiest way to confirm that everything's working::

    $ buildcat worker-info

This command submits a `buildcat.worker.info` job to the server, which hands it off to any
available worker.  If you check the console where we left our worker running, you'll see that it
accepts the job and runs it::

    13:25:53 default: buildcat.worker.info() (b8de2065-9fd7-4018-b77c-dd930f388880)
    13:25:53 default: Job OK (b8de2065-9fd7-4018-b77c-dd930f388880)
    13:25:53 Result is kept for 500 seconds

... and in the console where you submitted the job, information about the worker
is printed out::

    {'os': {'host': 'tim-aurora',
            'machine': 'x86_64',
            'processor': 'x86_64',
            'release': '4.4.0-19041-Microsoft',
            'system': 'Linux',
            'version': '#488-Microsoft Mon Sep 01 13:43:00 PST 2020'},
     'python': {'prefix': '/home/tshead/miniconda3',
                'version': '3.8.5 (default, Sep  4 2020, 07:30:14) \n[GCC 7.3.0]'},
     'worker': {'pid': 224,
                'root': '/home/tshead',
                'user': 'tshead',
                'version': '0.4.0-dev'}}

This confirms that the client, server, and worker are all communicating and
ready to go to work!

Summary
-------

That's it!  Your single-machine render farm is up-and-running.  Of course,
there are many details we've skipped in this section, such as how to run
workers on multiple machines, submit real render jobs, and how to secure your
farm's network connections.  The articles in the :ref:`user_guide` will address
these problems in detail.
