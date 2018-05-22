# Welcome!

<img src="artwork/buildcat.png" width="300" style="float:right"/>

Buildcat is the elegant, flexible, and lightweight build system that's
been been freed from bloated, monolithic tools like `make` and `SCons`.
Use Buildcat to process data, run scientific experiments, create documentation,
or handle any other build automation task.  Some key Buildcat features:

* Written in Python, called from Python, using a Pythonic API: no new config file formats or DSLs to learn.
* It's a library, not an executable: add it to existing scripts piecemeal, create your own front-ends, or integrate with an IDE, if you're into that sort of thing.
* *Doesn't* provide tools for C++ or Java compilation: building a PDF from LaTeX sources?  You don't need another !@#$! chapter on shared library design.
* *Doesn't* assume all targets are on the filesystem: want to use a database record or a file stored in the cloud as a dependency?  Go for it.
* Easily extensible: derive from `buildcat.Action` to define new actions on out-of-date targets.  Derive from `buildcat.Target` to create new types of target that live outside the filesystem.  Bam!
* Thorough [documentation](https://buildcat.readthedocs.io).  `Nuff said.

You can see the full Buildcat documentation with tutorials at
https://buildcat.readthedocs.io ... for questions, comments, or suggestions, get
in touch with our team at https://gitter.im/shead-custom-design/buildcat.

License
=======

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
