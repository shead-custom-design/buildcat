.. _design:

.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

Design
======

We created Buildcat because we were frustrated with opaque render farm software
that was needlessly complex.  Buildcat is written in Python for portability,
simplicity, and flexibility, using existing capabilities wherever possible.

.. tip::
    While Buildcat is as simple as we could possibly make it, there are many moving
    parts in a render farm - you'll need to understand the following concepts to
    make yours work.

Your Buildcat render farm will have all of the following:

Server
    The server keeps track of your render jobs, dispatching them to
    workers as the workers become available.  In Buildcat, the server
    is actually an instance of the widely used `Redis <https://redis.io>`_
    open source key-value store.

Workers
    Workers are the processes that carry out the actual work of rendering.
    Idle workers request jobs from the server and turn them into commands to
    your CG tools, typically (but not necessarily) instructions to render an
    animation frame.  Buildcat workers are instances of `RQ <http://python-rq.org>`_
    workers that have been customized to handle rendering jobs.

Clients
    Clients submit jobs to the server to be rendered by workers.  In Buildcat,
    the client is typically an integration with your DCC tool that uses `RQ <http://python-rq.org>`_
    to communicate with the server.  For example, the Buildcat `Houdini <https://sidefx.com>`_
    integration is a special Houdini ROP that communicates with the server to submit
    a render or simulation job.

Shared storage.
    Typically, a render job includes just the name of a scene file and a range
    of frames to render. To run the job, your workers must have access to the
    scene file and all of the assets it uses, including geometry, cached
    simulations, textures, and-so-on.  Typically, this means setting up a network
    share that all of the workers can reach.  It also means that artists will need
    to ensure that scene files and assets are moved to this location prior to job
    submission.

Network connectivity.
    To function, all clients and all workers must be able to communicate with the
    server.


.. note::
    The server, workers, and clients in your Buildcat render farm can be run on any
    host, or the same host.

