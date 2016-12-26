from shared import *

def test_remote_init():
    """ We have bare and local repo. After invoking init, storage should be
        placed in the bare one. .gitrsync should be created in the local one.
    """
    init_repos()
    os.chdir('local')
    shell(exepath + ' init')
    files = set(shell('ls -a'))
    assert('.gitrsync' in files)
    os.chdir(topdir)
    os.chdir('bare')
    files = set(shell('ls'))
    assert('storage' in files)

def test_local_init():
    """ We have only local repo. After invoking init, storage should be placed
        in .git directory. .gitrsync should be created in the local repo.
    """
    init_repos(remote=False)
    os.chdir('local')
    shell(exepath + ' init')
    files = set(shell('ls -a'))
    assert('.gitrsync' in files)
    os.chdir('.git')
    files = set(shell('ls'))
    assert('storage' in files)

def test_remote_custom_init():
    """ We have bare and local repo. Location of the storage is defined in
        git config. .gitrsync should be placed in the local repo.
    """
    init_repos()
    os.chdir('local')
    shell('git config --add rsync.url ../storage')
    shell(exepath + ' init')
    files = set(shell('ls -a'))
    assert('.gitrsync' in files)
    os.chdir(topdir)
    files = set(shell('ls'))
    assert('storage' in files)

def test_local_custom_init():
    """ We have only local repo. Location of the storage is defined in
        git config. .gitrsync should be placed in the local repo.
    """
    init_repos(remote=False)
    os.chdir('local')
    shell('git config --add rsync.url ../storage')
    shell(exepath + ' init')
    files = set(shell('ls -a'))
    assert('.gitrsync' in files)
    os.chdir('.git')
    files = set(shell('ls'))
    assert('storage' in files)

def test_remote_custom_init2():
    """ The same as remote_custom_init, but configured using init command.
    """
    init_repos()
    os.chdir('local')
    shell(exepath + ' init ../storage')
    files = set(shell('ls -a'))
    assert('.gitrsync' in files)
    os.chdir(topdir)
    files = set(shell('ls'))
    assert('storage' in files)

def test_local_custom_init2():
    """ The same as local_custom_init, but configured using init command.
    """
    init_repos(remote=False)
    os.chdir('local')
    shell(exepath + ' init ../storage')
    files = set(shell('ls -a'))
    assert('.gitrsync' in files)
    os.chdir('.git')
    files = set(shell('ls'))
    assert('storage' in files)

