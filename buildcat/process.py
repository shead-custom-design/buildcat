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
import buildcat.build
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

    def __repr__(self):
        return "buildcat.process.Process()"

    def _repr_svg_(self):
        import graphviz
        graph = graphviz.Digraph()
        graph.attr("node", shape="box")
        for node in self._graph.nodes:
            if isinstance(node, buildcat.action.Action):
                graph.node(str(id(node)), type(node).__name__)
        graph.attr("node", shape="ellipse")
        for node in self._graph.nodes:
            if not isinstance(node, buildcat.action.Action):
                graph.node(str(id(node)), type(node).__name__)
        for source, target in self._graph.edges:
            graph.edge(str(id(source)), str(id(target)))
        return graph._repr_svg_()

    def add_action(self, action, outputs, inputs=None, build=None):
        if isinstance(outputs, buildcat.target.Target):
            outputs = [outputs]
        if isinstance(inputs, buildcat.target.Target):
            inputs = [inputs]
        elif inputs is None:
            inputs = []
        if build is None:
            build = buildcat.build.Outdated()

        assert(isinstance(action, buildcat.action.Action))
        for node in outputs:
            assert(isinstance(node, buildcat.target.Target))
        for node in inputs:
            assert(isinstance(node, buildcat.target.Target))
        assert(isinstance(build, buildcat.build.Criteria))

        self._graph.add_node(action, build=build)

        for node in inputs:
            self._graph.add_edge(node, action)
        for node in outputs:
            self._graph.add_edge(action, node)

        return self

    def run(self):
        log.info("Started process: %s", self)

        environment = self._environment
        log.info("Environment: %r", environment)

        stop = False
        for node in networkx.algorithms.dag.topological_sort(self._graph):
            log.debug("Visiting: %r", node)
            if isinstance(node, buildcat.action.Action):
                inputs = [source for source, target in self._graph.in_edges(node)]
                outputs = [target for source, target in self._graph.out_edges(node)]
                build = networkx.get_node_attributes(self._graph, "build")[node]

                outdated = build.outdated(environment, inputs, outputs)
                log.debug("Testing: %r => %s", build, outdated)
                if outdated:
                    log.info("Running: %r", node)
                    node.execute(environment, inputs, outputs)

                for output in outputs:
                    if not output.exists(environment):
                        stop = True
                        log.error("Missing: %r", output)

            if stop:
                break

        log.info("Finished process: %s", self)

        return self

