import sys
from path import Path 

ext = Path(sys.executable).ext

def task_build():
    """ Build executable specific for current platform.
    """
    return {'actions': ['mkdir -p bin',
                        'nim c ' + Path('src') / 'gitrsync.nim',
                        'mv ' + Path('src') / 'gitrsync' + ext + ' ' + Path('bin') / 'git-rsync' + ext],
           }

def task_test():
    """ Run all unit tests.
    """
    return {'actions': ['py.test -v ' + Path('test')],
            'verbosity': 2
           }

def task__junk():
    """ Hidden task. Enables `clean` command which removes all the files not tracked by git.
    """
    return {'actions': [],
            'clean': ['git clean -dfx'],
           }

