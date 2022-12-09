.. image:: ../../artwork/logo.png
  :width: 200px
  :align: right

.. _monitoring:

Monitoring
==========

Buildcat is based on `RQ <https://python-rq.org>`_, which already has a variety
of builtin and third party monitoring tools. You can read about them in detail
at http://python-rq.org/docs/monitoring, but in brief, you can see a quick
overview of your farm from the command line with::

    $ rq info

... which will print information about your current queues, jobs, and workers.  To see continuously-updating information,
specify a poll interval in seconds::

    $ rq info --interval 5

For a more sophisticated, web-based interface to your farm, try `RQ dashboard
<https://github.com/Parallels/rq-dashboard>`_, which provides
continuously-updated information, plus the ability to delete and reschedule
jobs.

Finally, the :ref:`buildcat` tool provides a command to estimate how long it
might take for a collection of jobs to finish::

    $ buildcat eta

... the eta command will monitor the number of jobs submitted to your server
over time; as long as the number of jobs is decreasing, it will estimate when
the number of jobs will become zero.

