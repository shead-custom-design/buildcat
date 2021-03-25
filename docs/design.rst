.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _design:

Design
======

We created Buildcat because we were frustrated with the complexity and builtin
assumptions with other render farm systems.  Buildcat is written in Python for
portability, simplicity, and flexibility.  It runs on MacOS, Linux, and Windows
(using WSL), and uses existing open source software wherever possible instead
of reinventing wheels.

.. tip::
    While Buildcat is as simple as we could possibly make it, there are still
    many moving parts in a render farm - you'll need to understand the
    following concepts to make yours work.

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

