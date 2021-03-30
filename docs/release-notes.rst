.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _release-notes:

Release Notes
=============

Buildcat 0.3.0 - March 30th, 2021
---------------------------------

* Create a single command-line client with subcommands for starting the server, starting workers, and submitting jobs.
* Added integrations for Modo and Redshift.
* Removed support for Python 2 in the Buildcat module.
* Removed support for Windows, use WSL instead.
* Eliminated the need for custom worker code, so we can use vanilla RQ workers instead.
* Completely reorganized and harmonized behavior among integrations.
* Added a command to estimate when a queue will be empty.
* Explicitly use pickle protocol 2 for serialization, so (non-Buildcat) Python 2 clients can submit jobs.

Buildcat 0.2.0 - July 8th, 2019
-------------------------------

* Greatly expanded documentation.
* Introduced support for multiple render queues in Houdini.
* Added support for rendering multiple frames at a time from DOP ROPs in Houdini.
* Improved error checking and troubleshooting messages in Houdini.
* Support rendering with step sizes other than one in Houdini.

Buildcat 0.1.0 - March 20th, 2019
---------------------------------

* Initial release, including basic Houdini integration.

Buildcat 0.0.1 - May 18th, 2018
-------------------------------

* Setting up the project.

