.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _advanced-setup:

Advanced Setup
==============

This section covers the additional details you'll need to setup a real Buildcat
render farm on multiple machines.  If you haven't already, we strongly recommend
that you cover the :ref:`basic-setup` documentation.

Shared Storage
--------------

In addition to the other considerations already discussed, you'll need to
ensure that your shared storage is accessible to every worker that will be a
member of your render farm, and every client that will be submitting jobs.  To
do so, you'll have to enable network file sharing for the shared storage
directory on your platform.  We recommend that you try remote browsing from
all of your worker and client hosts to ensure that they can access the
shared storage.

.. note::
    Keep in mind that BUILDCAT_ROOT will vary from host-to-host depending on
    the platform and whether it's being accessed locally or across the network.
    For example, on a Mac named `Aurora` hosting shared storage
    on an external drive named `Buildcat`, BUILDCAT_ROOT would be
    `/Volumes/Buildcat`.  Elsewhere on the network, BUILDCAT_ROOT
    would be `//Aurora/Buildcat` on Mac and Linux hosts, and `\\\\\\Aurora\\Buildcat`
    on Windows hosts.

Network Communication
---------------------

So workers and clients can communicate with the server, you'll need to identify
a public network address on the server host that they can access.  For example,
instead of `127.0.0.1`, which can only be accessed by processes running on the
local host, you'll need the address of an ethernet or wireless interface on the
machine where the server is running.

We'll use the address `192.168.2.1` throughout the rest of this section.

Server
------

When we ran the Buildcat server previously, it defaulted to the loopback address
`127.0.0.1`, which meant that it would only accept connections from the same
machine it was running on.  Now, we need the server to accept connections from
other machines, using a public server address.  To do so, pass the server network
address at startup::

    $ buildcat server --bind 192.168.2.1

Now, the server will be listening at the given address, allowing workers and clients
to connect from other machines.

Worker
------

Now that we've changed the address that the server is listening on, we have to tell
workers to contact it at that address (and we have to point them to the correct
BUILDCAT ROOT directory for their platform)::

    $ cd //Aurora/Buildcat
    $ buildcat worker --host 192.168.2.1

There is no secret to running multiple workers - simply start as many workers
as you need, on multiple hosts or even the same host, pointing them to the server's
address.

Testing
-------

Similarly, our testing code needs the new server address to function::

    $ buildcat worker-info --host 192.168.2.1

Keep in mind that, now that we're running multiple workers, the job may
be run on any one of them, so that the ping job results will vary
dependeing on which worker handled it.

Monitoring
----------

RQ already has a variety of builtin and third party monitoring tools
`here <python-rq.org/docs/monitoring>`_.
