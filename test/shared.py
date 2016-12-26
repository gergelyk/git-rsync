import os, sys
import pytest
from miscutils.shell import shell
from path import Path
ext = Path(sys.executable).ext
topdir = Path(__file__).abspath().parent
exepath = topdir.parent / 'bin' / 'git-rsync' + ext

def clean_up():
    os.chdir(topdir)
    shell('rm -fr bare')
    shell('rm -fr local')
    shell('rm -fr storage')

@pytest.fixture(autouse=True)
def fixture_clean_up():
    clean_up() # clean before test
    yield
    clean_up() # clean after test

def init_repos(remote=True):
    if remote:
        shell('mkdir bare')
        os.chdir('bare')
        shell('git init --bare')
        os.chdir(topdir)
        shell('git clone bare local')
    else:
        shell('mkdir local')
        os.chdir('local')
        shell('git init')
        os.chdir(topdir)
        
def _add_file(idx):
    shell('echo file{idx} > "f {idx}"'.format(idx=idx))
    shell('git add "f {idx}"'.format(idx=idx))
    shell('git ci -am "f {idx} added"'.format(idx=idx))

def _add_tag(tag):
    shell('git tag {tag}'.format(tag=tag))

def fill_repos(spec, remote=True):
    os.chdir('local')
    f = [_add_file, _add_tag]
    for line in spec.strip().split('\n'):
        for item in line.split():
            f[0](item)
        f = f[1:] + [f[0]]
    if remote:
        shell('git push')
    os.chdir(topdir)

def fill_storage(spec, target='bare'):
    os.chdir(target)
    shell('mkdir storage')
    os.chdir('storage')
    for tag in spec:
        shell('mkdir {tag}'.format(tag=tag))
        os.chdir(tag)
        for item in spec[tag]:
            shell('echo big{name} > "b {name}"'.format(name=item))
        os.chdir('..')
    os.chdir(topdir)

def create_large_files(spec):
    os.chdir('local')
    for name in spec:
        shell('echo "Executable {name}" > "app {name}.exe"'.format(name=name))
    os.chdir(topdir)
    
repos_v1 = """
0 1 2
1.0.0
3 4 5
foo
6 7 8
1.1.0
9 10 11
"""

storage_v1 = {'1.0.0': '0 1'.split(),
              '1.1.0': '2 3'.split(),
              'foo':   '4 5'.split(),
             }
             
