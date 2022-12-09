.. image:: ../artwork/logo.png
  :width: 200px
  :align: right

.. _development:

Development
===========

Getting Started
---------------

If you haven't already, you'll want to get familiar with the Buildcat repository
at http://github.com/shead-custom-design/buildcat ... there, you'll find the Buildcat
sources, issue tracker, discussions, and wiki.

Next, you'll need to install all of the extra dependencies needed for Buildcat development::

    $ pip install buildcat[all]

Then, you'll be ready to obtain Buildcat's source code and install it using "editable mode".  Editable
mode is a feature provided by `pip` that links the Buildcat source code into the install directory
instead of copying it ... that way you can edit the source code in your git sandbox, and you don't
have to keep re-installing it to test your changes::

    $ git clone https://github.com/shead-custom-design/buildcat.git
    $ cd buildcat
    $ pip install --editable .

Versioning
----------

Buildcat version numbers follow the `Semantic Versioning <http://semver.org>`_ standard.

Coding Style
------------

The Buildcat source code follows the `PEP-8 Style Guide for Python Code <http://legacy.python.org/dev/peps/pep-0008>`_.

Running Regression Tests
------------------------

To run the Buildcat test suite, simply run `regression.py` from the
top-level source directory::

    $ cd buildcat
    $ python regression.py

The tests will run, providing feedback on successes / failures.

Test Coverage
-------------

When you run the test suite with `regression.py`, it also automatically
generates code coverage statistics.  To see the coverage results, open
`buildcat/.cover/index.html` in a web browser.

Building the Documentation
--------------------------

To build the documentation, run::

    $ cd buildcat/docs
    $ make html

Once the documentation is built, you can view it by opening
`buildcat/docs/_build/html/index.html` in a web browser.
