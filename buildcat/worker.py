# Copyright 2018 Timothy M. Shead
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functionality for retrieving information about workers.
"""

import buildcat


def info():
    """Returns information about a worker.

    Useful for testing that the system is functioning.

    Returns
    -------
    metadata: :class:`dict`
        A collection of key-value pairs containing information describing the
        local worker.
    """
    return buildcat.info()


def logtree():
    import logging_tree
    logging_tree.printout()


