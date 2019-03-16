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

"""Functionality for testing the buildcat installation and setup.
"""

from __future__ import absolute_import, division, print_function

import buildcat

def log_message(message):
    """Log a message.

    Parameters
    ----------
    message: str, required
        The message to be logged.
    """
    buildcat.log.info(message)

def raise_exception(e):
    """Raise an exception.

    Useful for testing the reliability of workers.

    Parameters
    ----------
    e: exception object, required
        The exception to be raised.
    """
    raise e

