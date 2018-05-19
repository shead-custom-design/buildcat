# Copyright 2018 Timothy M. Shead
#
# This file is part of Buildcat.
#
# Buildcat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Buildcat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Buildcat.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import os
import re
import shutil
import subprocess

import nbconvert.preprocessors
import nbformat
import traitlets.config

parser = argparse.ArgumentParser()
parser.add_argument("command", nargs="?", default="html", choices=["clean", "convert", "html"], help="Command to run.")
arguments = parser.parse_args()

root_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
docs_dir = os.path.join(root_dir, "docs")
build_dir = os.path.join(docs_dir, "_build")
test_dir = os.path.join(docs_dir, "_test")

class SkipCells(nbconvert.preprocessors.Preprocessor):
    def preprocess(self, nb, resources):
        cells = []
        for cell in nb.cells:
            if cell["cell_type"] == "code" and cell["source"].startswith("# nbconvert: hide"):
                continue
            if cell["cell_type"] == "code" and cell["source"].startswith("# nbconvert: stop"):
                break
            cells.append(cell)
        nb.cells = cells
        return nb, resources

def convert_notebook(name, force):
    print("Converting %s" % name)

    # If the Sphinx source is up-to-date, we're done.
    source = os.path.join(docs_dir, "%s.ipynb" % name)
    target = os.path.join(docs_dir, "%s.rst" % name)
    if os.path.exists(target) and os.path.getmtime(target) >= os.path.getmtime(source) and not force:
        return

    nbconvert_version = subprocess.check_output(["jupyter", "nbconvert", "--version"]).strip()
    if nbconvert_version not in ["4.0.0", "4.1.0", "4.2.0"]:
        raise Exception("Unsupported nbconvert version: %s" % nbconvert_version)

    # Some installations of ipython don't properly configure the hooks for Pygments lexers, which leads to missing
    # source code cells when the documentation is built on readthedocs.org.
    import pygments.plugin
    if not list(pygments.plugin.find_plugin_lexers()):
        raise Exception("It appears that ipython isn't configured correctly.  This is a known issue with the stock conda ipython package.  Try `conda update ipython -c conda-forge` instead.")

    # Convert the notebook into restructured text suitable for the
    # documentation.
    with open(source) as f:
        notebook = nbformat.read(f, as_version=4)
        # Execute the notebook to update its contents and ensure it runs
        # without error.
        execute = nbconvert.preprocessors.ExecutePreprocessor()
        execute.preprocess(notebook, {"metadata": {"path": "."}})
        # Setup the RST exporter.
        config = traitlets.config.Config()
        config.RSTExporter.preprocessors = [SkipCells]
        rst_exporter = nbconvert.RSTExporter(config=config)
        (body, resources) = rst_exporter.from_notebook_node(notebook)
        # Unmangle Sphinx cross-references in the tutorial that get mangled by
        # markdown.
        body = re.sub(":([^:]+):``([^`]+)``", ":\\1:`\\2`", body)
        body = re.sub("[.][.].*\\\\(_[^:]+):", ".. \\1:", body)

        body = """
.. image:: ../artwork/buildcat.png
    :width: 200px
    :align: right
""" + body

        with open(target, "wb") as file:
            file.write(body)


# Always build the documentation from scratch.
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

notebooks = [
    #"battery-chargers",
    #"gps-receivers",
    ]

# Clean the build.
if arguments.command == "clean":
    for name in notebooks:
        if os.path.exists("%s.rst" % name):
            os.remove("%s.rst" % name)

# Convert notebooks.
if arguments.command == "convert":
    for name in notebooks:
        convert_notebook(name, force=True)

# Generate the HTML documentation.
if arguments.command in ["html"]:
    for name in notebooks:
        convert_notebook(name, force=False)
    subprocess.check_call(["make", arguments.command], cwd=docs_dir)

