.. image:: ../../artwork/buildcat.png
  :width: 200px
  :align: right

.. _multiple-workers:

Multiple Worker Setup
=====================

This section covers the additional details you'll need to setup a real Buildcat
render farm on multiple machines.  If you haven't already, we strongly
recommend that you create a single-machine farm using the :ref:`basic-setup`
documentation before proceeding.

Shared Storage
--------------

You'll need to ensure that your shared storage is accessible to every worker
that will be running jobs, and every client that will be submitting jobs.  To
do so, you'll have to enable network file sharing for the shared storage
directory on your platform.  After doing so, we recommend that you manually
verify that all of your worker and client hosts can access the shared
storage before proceeding.

.. note::
    Keep in mind that BUILDCAT_ROOT will vary from host-to-host depending on
    the platform and whether it's being accessed locally or across the network.
    For example, on a Mac named `Aurora` hosting shared storage
    on an external drive named `Farm`, BUILDCAT_ROOT would be
    `/Volumes/Farm`.  On the other Mac and Linux hosts on the network, BUILDCAT_ROOT
    would be `//Aurora/Farm`.  On Windows hosts, it would be `\\\\Aurora\\Farm`.

Network Communication
---------------------

All of your workers and clients will need to communicate with the server, so
you'll need to identify a public network address on the server host that they
can access.  For example, instead of `127.0.0.1`, which can only be accessed by
processes running on the local host, you'll need the address of an ethernet or
wireless interface on the machine where the server is running.  You should
verify that all of your workers and clients can ping the server at that
address.

We'll use the address `192.168.2.1` for our server throughout the rest of this section.

Server
------

When we ran the Buildcat server in :ref:`basic-setup`, it defaulted to the
loopback address `127.0.0.1`, which meant that it would only accept connections
from workers and clients running on the same host.  Now, we need the server to
accept connections from other machines, using a public server address.  To do
so, just specify the server's network address at startup::

    $ buildcat server --bind 192.168.2.1

Now, the server will be listening at the given address, allowing workers and clients
to connect from other machines.

Workers
-------

Now that we've changed the address that the server is listening on, we have to tell
workers to contact it at that address (and we have to point them to the correct
BUILDCAT_ROOT directory for their platform)::

    $ cd <local BUILDCAT_ROOT>
    $ buildcat worker --host 192.168.2.1

There is no secret to running multiple workers for your farm - simply start as
many workers as you need, on multiple hosts or even the same host, pointing
them to the server's address.

Clients
-------

Similarly, clients will need to specify the server address to submit jobs::

    $ buildcat worker-info --host 192.168.2.1

Keep in mind that, now that we're running multiple workers, the job may be run
on any one of them, so that the information returned by the worker-info job in
this example will change depending on the host and worker where it was handled.

