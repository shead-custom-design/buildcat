.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _developers:

Developers
==========

Even if you're not in a position to contribute code to Buildcat, there are many
ways you can help the project out:

* Show us cool stuff that you rendered using Buildcat!
* Tell us if Buildcat doesn't work for your pipeline.
* Help us write documentation.
* Spread the word!

Getting Started
---------------

If you haven't already, you'll want to get familiar with the Buildcat repository
at http://github.com/shead-custom-design/buildcat ... there, you'll find the Buildcat
sources, issue tracker, and wiki.

Next, you'll need to install Buildcat's dependencies, listed in setup.py.  Then, you'll be
ready to get Buildcat's source code and use setuptools to install it. To do
this, you'll almost certainly want to use "develop mode".  Develop mode is a a
feature provided by setuptools that links the Buildcat source code into the
install directory instead of copying it ... that way you can edit the source
code in your git sandbox, and you don't have to re-install it to test your
changes::

    $ git clone https://github.com/sandialabs/buildcat.git
    $ cd buildcat
    $ python setup.py develop

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
`.cover/index.html` in a web browser.

Building the Documentation
--------------------------

To build the documentation, run::

    $ cd buildcat/docs
    $ make html

Once the documentation is built, you can view it by opening
`buildcat/docs/_build/html/index.html` in a web browser.
