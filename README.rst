===============
   git-rsync
===============

**Extends git with ability of handling large files.**

Syntax:

::

    git rsync init [<storage>]
    git rsync push [<dir>]
    git rsync pull [<dir>]


What differs ``git-rsync`` from other solutions is that large files are not bundled to the commits, but rather to the tags, or user-defined names. Large files are stored under original names, which makes it easy to restore them manually if such need arises. ``git-rsynch`` is distributed as compliled executable, which significantly reduces number of dependencies. Finally ``git-rsync`` can be used right away, without any configuration. At the same time, tool is configurable to reflect everyone's needs.

Installation
============

Pre-compiled versions of the application can be found `here <https://github.com/gergelyk/git-rsync/releases>`_.

Linux
-----

1. ``git-rsync`` executable should be copied to one of the directories listed in system ``PATH`` variable. Typically it should go to ``/usr/bin`` directory.

2. ``rsync`` command must be available in the system.

Windows
-------

1. ``git-rsync`` executable should be copied to ``<git-installation>\usr\bin`` directory.

2. ``rsync`` command must be available. It's location should be added to system PATH variable. ``git-rsync`` has been tested with `cwRsync <https://www.itefix.net/cwrsync>`_ which is a suggested solution.

Building
========

Requirements
------------

``git-rsync`` has been developed in `Nimrod <http://nim-lang.org/>`_ programming language. For compiling executable, corresponding `compiler <http://nim-lang.org/download.html>`_ needs to be installed in version 0.15.0 or compatible.

Beside the standard library, following libraries should be also installed:

* strfmt~0.8.4
* docopt~0.6.4

``nimble`` package manager can be used to accomplish this task.

Toolchain used in this porject is based on Python 3. Following packages are required:

* path.py~8.1.2
* miscutils~0.20
* doit~0.29.0
* pytest~3.0.5

Toolchain
---------

Following commands are available in the top directory of the project:

::

    doit build  # builds executable and stores it in /bin directory
    doit test   # runs unit tests
    doit clean  # removes all files and directories not tracked by git

Documentation
=============

Separate documents contain `Tutorial` and `User's Manual` and `Reference` respectively. Check `doc` directory.

Disclaimer
==========

This software has been created for personal use of the author. It has never been extensively tested. One should use it only on his own responsibility.

Alternatives
============

There are multiple tools that add support of large files to git:

* `lfs <https://git-lfs.github.com/>`_ - Introduced by GitHub. Requires dedicated server to be running. The only one which is available for free at the time of writing (`lfs-test-server <https://github.com/git-lfs/lfs-test-server>`_) is not intended to be used in production.

* `fat <https://github.com/jedbrown/git-fat>`_ - Replaces large files in the repository with small files which contain references to the original ones. Original files are stored in a dedicated directory. Each file is identified by a hash code.

* `media <https://github.com/alebedev/git-media>`_ - Similar to ``git-far``. Supports automatic synchronization and more protocols.

* `annex <http://git-annex.branchable.com/>`_ - Uses symlinks (indirect mode) or hash codes (direct mode) to substitute large files.

Donations
=========

It is absolutely fine if you use this software for free for commercial or non-commercial purposes. On the other hand, if you would like to repay author's efforts you are welcome to use following button:

.. image:: https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url
