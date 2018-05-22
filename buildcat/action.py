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
import subprocess

import six

import buildcat.node
import buildcat.target

log = logging.getLogger(__name__)


class Action(buildcat.node.Node):
    def __init__(self):
        super(Action, self).__init__()

    def __repr__(self):
        return "buildcat.action.Action()"

    def execute(self, environment, inputs, outputs):
        pass


class MakeDirectory(Action):
    def __init__(self):
        super(MakeDirectory, self).__init__()

    def __repr__(self):
        return "buildcat.action.MakeDirectory()"

    def execute(self, environment, inputs, outputs):
        for node in outputs:
            assert(isinstance(node, buildcat.target.Directory))
        for node in outputs:
            if not node.exists(environment):
                path = environment.abspath(node.path)
                os.makedirs(path)


class Shell(Action):
    def __init__(self, command):
        assert(isinstance(command, six.string_types))
        super(Shell, self).__init__()
        self._command = command

    def __repr__(self):
        return "buildcat.action.Shell(command=%r)" % (self._command)

    def execute(self, environment, inputs, outputs):
        command = self._command.format(
            source=inputs[0].string(environment) if inputs else "",
            sources=[node.string(environment) for node in inputs],
            target=outputs[0].string(environment) if outputs else "",
            targets=[node.string(environment) for node in outputs],
        )
        log.debug("Shell: %s", command)
        process = subprocess.Popen(command, shell=True, cwd=environment.cwd, env={}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stdout:
            log.debug("Stdout: %s", stdout)
        if stderr:
            log.debug("Stderr: %s", stderr)
        if process.returncode:
            log.debug("Returncode: %s", process.returncode)



class TouchFile(Action):
    def __init__(self):
        super(TouchFile, self).__init__()

    def __repr__(self):
        return "buildcat.action.TouchFile()"

    def execute(self, environment, inputs, outputs):
        for node in outputs:
            assert(isinstance(node, buildcat.target.File))
        for node in outputs:
            path = environment.abspath(node.path)
            with open(path, "a"):
                os.utime(path, None)


