.. Buildcat documentation master file, created by
   sphinx-quickstart on Fri Nov 25 17:53:50 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: ../artwork/buildcat.png
  :width: 300px
  :align: right

Welcome!
========

Buildcat is the elegant, flexible, and lightweight build system that's been
struggling to escape from bloated, monolithic tools like `make` and `SCons`.  Use
Buildcat to process data, run scientific experiments, create documentation, or
handle any other build automation task.  Some key Buildcat features:

* Written in Python, called from Python, using a Pythonic API: no new config file formats or DSLs to learn.
* It's a library, not an executable: add it to existing scripts piecemeal, create your own front-ends, or integrate with an IDE, if you're into that sort of thing.
* *Doesn't* provide tools for C++ or Java compilation: building a PDF from LaTeX sources?  You don't need another !@#$! chapter on shared library design.
* *Doesn't* assume all targets are on the filesystem: want to use a database record or a file stored in the cloud as a dependency?  Go for it.
* Easily extensible: derive from :class:`buildcat.action.Action` to define new actions on out-of-date targets.  Derive from :class:`buildcat.target.Target` to create new types of target that live outside the filesystem.  Bam!

Documentation
=============

.. toctree::
   :maxdepth: 2

   installation.rst
   dependencies.rst
   compatibility.rst
   user-guide.rst
   contributing.rst
   release-notes.rst
   reference.rst
   support.rst
   credits.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

