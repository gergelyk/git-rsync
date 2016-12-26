User's Manual
=============

Operation
---------

``git-rsync`` creates ``storage`` directory with sub-directories where large files are stored. For transferring files between storage and working copy, system ``rsync`` command is used. Following options are in place by default for transferring to the storage and to the working copy respectively:

::

    rsync -Rrav --progress {src} {url}
    rsync -rav --progress {url} .

They can be redefined by using ``git config --add rsync.push <COMMAND>`` and ``git config --add rsync.pull <COMMAND>``. ``{url}`` placeholder will be raplaced by `<storage>\<sub-directory>\`. ``{src}`` placeholder will be raplaced by space-separated lines from ``.gitrsync`` file. For more details read following sections of this document.

Storage
-------

``git-rsync`` uses one of three locations for storage directory:

* local repositories without corresponding remote repository use ``.git/storage`` directory by default.
* local repositories with remote repository specified in ``git config --get remote.origin.url`` use ``<remote_repo>/storage`` directory by default.
* user can redefine location of the storage by invoking ``git config --add rsync.url <URL>``

<URL> can be anything supported by rsync. Note that for CIFS shares cwRsync prefers ``//foo/bar/baz`` rather than ``\\foo\bar\baz``.

``<storage>`` parameter of ``git-rsync init`` command can be used as an alternative to ``git config --add rsync.url``.

Sub-directory
-------------

Before exporting/importing files, ``git-rsync`` needs to know the name of sub-directory in ``storage`` directory.

* By default, name of the last tag reachable from the current commit is used as sub-directory name.
* User can define a filter to discard undesirable tags. ``git config --add rsync.tag <PATTERN>`` command can be used. ``<PATTERN>`` should be a `glob(7)` expression acceptable by ``git-describe`` command.
* Alternatively explicite name of the sub-directory can be passed as ``<dir>`` parameter of `git-rsync pull` of `git-rsync push` command.

Sources
-------

Sources are files/directories which ``git-rsync`` exports from the working copy to the storage. They should be defined in ``.gitrsync`` file located in the top directory of working copy. This file is also expected to be added to the repository. Each line of the file defines separate source(s). Keep in mind that these entries are expanded by underlying shell. This means that you can use patterns (containing asterisks, question marks, etc.) as long as they are supported by shells used by the other users. Usually using `glob(7)` is a reasonable choice. Lines of ``.gitrsync`` that begin with hash symbol (``#``) are discarded.

Tips
----

* git-rsync supports as many protocols as rsync itself. To access unsupported remote locations, one may mount them into the local file system.

* It is convenient to assign a short alias to ``git-rsync`` command. For more details refer to `git help <https://git-scm.com/book/it/v2/Git-Basics-Git-Aliases>`_.





