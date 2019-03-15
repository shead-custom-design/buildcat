.. image:: ../artwork/buildcat.png
  :width: 200px
  :align: right

.. _dependencies:

Dependencies
============

Minimum Requirements
--------------------

To use Buildcat you will need, at a minimum, Python 2 or 3 (duh):

* Python 2.7 / Python 3 - http://python.org

plus the following (if you install Buildcat
using pip, these are automatically installed for you):

* RQ - Simple job queues for Python - http://python-rq.org
* redis - The Python interface to the Redis key-value store - https://pypi.org/project/redis/
* six - Python 2/3 portability - http://pythonhosted.org/six

Source Installation
-------------------

If you're installing Buildcat from source, you'll need setuptools to run the
Buildcat setup.py script:

* setuptools - https://setuptools.readthedocs.io

Regression Testing
------------------

The following are required to run Buildcat's regression tests and view
code coverage:

* behave - BDD test framework - http://pythonhosted.org/behave
* coverage - code coverage module - http://nedbatchelder.com/code/coverage
* mock - mocking and testing library - http://www.voidspace.org.uk/python/mock
* nose - unit test framework - https://nose.readthedocs.io/en/latest

Generating Documentation
------------------------

And you'll need to following to generate this documentation:

* Sphinx - documentation builder - http://sphinx-doc.org
* Sphinx readthedocs theme - https://github.com/snide/sphinx_rtd_theme
* napoleon - http://sphinxcontrib-napoleon.readthedocs.io/en/latest/
* Jupyter - http://ipython.org
* Pandoc - http://johnmacfarlane.net/pandoc

