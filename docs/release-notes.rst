.. image:: ../artwork/logo.png
  :width: 200px
  :align: right

.. _release-notes:

Release Notes
=============

Buildcat 0.5.0 - December 9th, 2022
-----------------------------------

* Added certificate-info command to show certificate file details.
* Added workers command to start more than one worker at a time.
* Updated houdini-render-ifd command can submit multiple jobs at once.
* Set a reasonable default timeout for the houdini-render-ifd command.
* Added timeout arguments for houdini-render-hip, modo-render, and redshift-render commands.
* Allow newer Redis versions.
* Switched to pyproject.toml and flit for packaging.

Buildcat 0.4.1 - October 22nd, 2021
-----------------------------------

* Updated the way we collect code coverage data.
* Switched from Zulip to Github Discussions for support.

Buildcat 0.4.0 - October 14th, 2021
-----------------------------------

* Removed DCC-specific files from the install.
* Improved consistency among subcommand arguments.
* Added subcommands to secure communication channels with TLS.
* Allow clients to contact the server using a nonstandard port.
* Organized and streamlined the documentation.
* Switched from Travis-CI to Github Actions for continuous integration.
* Buildcat server can serialize tasks to an arbitrary storage path.
* Added an option to run workers without forking, for Windows.
* Added an integration to render Houdini .ifd files.
* Added support for rendering arbitrary collections of frames and frame ranges from a Houdini .hip file.
* Added an option to specify the maximum number of jobs executed by a worker.

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

