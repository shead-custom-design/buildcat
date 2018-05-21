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

"""Elegant, flexible build system in Python complex processes."""

from __future__ import absolute_import, division, print_function

import logging
import os

import networkx
import networkx.algorithms.dag

import buildcat.action
import buildcat.target

log = logging.getLogger(__name__)


class Environment(object):
    def __init__(self, cwd=None):
        if cwd is None:
            cwd = os.getcwd()
        self._cwd = cwd

    def __repr__(self):
        return "buildcat.process.Environment(cwd=%r)" % (self._cwd)

    def abspath(self, path):
        return os.path.normpath(os.path.join(self._cwd, path))

    @property
    def cwd(self):
        return self._cwd


class Process(object):
    def __init__(self, cwd=None):
        self._graph = networkx.DiGraph()
        self._environment = Environment(cwd=cwd)

    def _repr_svg_(self):
        import graphviz
        graph = graphviz.Digraph()
        graph.attr("node", shape="box")
        for node in self._graph.nodes:
            if isinstance(node, buildcat.action.Action):
                graph.node(str(id(node)), node.label)
        graph.attr("node", shape="ellipse")
        for node in self._graph.nodes:
            if not isinstance(node, buildcat.action.Action):
                graph.node(str(id(node)), node.label)
        for source, target in self._graph.edges:
            graph.edge(str(id(source)), str(id(target)))
        return graph._repr_svg_()

    def add_action(self, action, outputs, inputs=None):
        if isinstance(outputs, buildcat.target.Target):
            outputs = [outputs]
        if isinstance(inputs, buildcat.target.Target):
            inputs = [inputs]
        elif inputs is None:
            inputs = []

        assert(isinstance(action, buildcat.action.Action))
        for node in outputs:
            assert(isinstance(node, buildcat.target.Target))
        for node in inputs:
            assert(isinstance(node, buildcat.target.Target))

        for node in inputs:
            self._graph.add_edge(node, action)
        for node in outputs:
            self._graph.add_edge(action, node)

        return self

    def run(self):
        stop = False
        log.info("Environment: %r", self._environment)
        for node in networkx.algorithms.dag.topological_sort(self._graph):
            #log.debug("Visiting: %r", node)
            if isinstance(node, buildcat.action.Action):
                log.info("Running: %r", node)
                inputs = [source for source, target in self._graph.in_edges(node)]
                outputs = [target for source, target in self._graph.out_edges(node)]
                node.execute(self._environment, inputs, outputs)
                for output in outputs:
                    if not output.exists(self._environment):
                        stop = True
                        log.error("Missing: %r", output)

            if stop:
                break

        return self

