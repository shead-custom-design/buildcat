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

import networkx
import networkx.algorithms.dag

__version__ = "0.1.0-dev"

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Node(object):
    def __init__(self, label):
        self._label = label

    def __repr__(self):
        return "<buildcat.Node %r>" % self._label

    @property
    def label(self):
        return self._label

class Target(Node):
    def __init__(self, label):
        super(Target, self).__init__(label)

    def __repr__(self):
        return "<buildcat.Target %r>" % self._label

class Action(Node):
    def __init__(self, label):
        super(Action, self).__init__(label)

    def __repr__(self):
        return "<buildcat.Action %r>" % self._label

    def execute(self):
        pass

class Process(object):
    def __init__(self):
        self._graph = networkx.DiGraph()

    def _repr_svg_(self):
        import graphviz
        graph = graphviz.Digraph()
        graph.attr("node", shape="box")
        for node in self._graph.nodes:
            if isinstance(node, Action):
                graph.node(str(id(node)), node.label)
        graph.attr("node", shape="ellipse")
        for node in self._graph.nodes:
            if not isinstance(node, Action):
                graph.node(str(id(node)), node.label)
        for source, target in self._graph.edges:
            graph.edge(str(id(source)), str(id(target)))
        return graph._repr_svg_()

    def add_action(self, action, outputs, inputs=None):
        if isinstance(outputs, Target):
            outputs = [outputs]
        if isinstance(inputs, Target):
            inputs = [inputs]
        elif inputs is None:
            inputs = []

        assert(isinstance(action, Action))
        for node in outputs:
            assert(isinstance(node, Target))
        for node in inputs:
            assert(isinstance(node, Target))

        for node in inputs:
            self._graph.add_edge(node, action)
        for node in outputs:
            self._graph.add_edge(action, node)

    def run(self):
        for node in networkx.algorithms.dag.topological_sort(self._graph):
            log.debug("Visiting %r", node)
            if isinstance(node, Action):
                log.debug("Executing %r", node)
                node.execute()

        return self

