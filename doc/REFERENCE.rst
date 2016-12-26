Reference
=========


Commands
--------

``git rsync init [<storage>]``

    Create ``.gitrsync`` file in the local repository. Also creates ``storage`` directory in the place inferred from the configuration of the local repository.

    ``<storage>`` - can be used for defining location of the ``storage`` directory explicitly.

``git rsync push [<dir>]``

    Copy files specified in ``.gitrsync`` to sub-directory of the ``storage`` directory. Name of the sub-directory is selected as name the most recent tag reachable from the current commit.

    ``<dir>`` - can be used for defining sub-directory of the ``storage`` directory explicitly.

``git rsync pull [<dir>]``

    Copy files from sub-directory of the ``storage`` directory to the working copy. Name of the sub-directory is selected as name the most recent tag reachable from the current commit.

    ``<dir>`` - can be used for defining sub-directory of the ``storage`` directory explicitly.

Configuration
-------------

Items below correspond to the entries in configuration file of git. They can be accessed using ``git config`` command.

``rsync.pull``

    Command used for transferring files from the ``storage`` to the working copy. Refer to the `Manual` for more details.

``rsync.push``

    Command used for transferring files from the working copy to the ``storage``. Refer to the `Manual` for more details.

``rsync.tag``

    Pattern defining tags used as names of sub-directories in the ``storage``. Refer to the `Manual` for more details.

``rsync.url``

    User-defined URL of the ``storage`` directory. Refer to the `Manual` for more details.

