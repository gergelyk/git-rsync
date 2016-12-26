from shared import *

def test_remote_push_auto():
    """ We have bare and local repo. We export files to the directory name of
        which corresponds to the most recent tag.
    """
    init_repos()
    fill_repos(repos_v1)
    os.chdir('bare')
    shell('mkdir storage')
    os.chdir(topdir)
    create_large_files(['1', '2', '3'])
    os.chdir('local')
    init_gitrsync(['1', '2', '3'])
    shell(exepath + ' push')
    os.chdir(topdir)
    os.chdir('bare')
    os.chdir('storage')
    os.chdir('1.1.0')
    files = set(shell('ls'))
    assert(files == {'app 1.exe', 'app 2.exe', 'app 3.exe'})
    
def test_remote_push_selected():
    """ We have bare and local repo. We export files to the directory name of
        which is specified in command line.
    """
    init_repos()
    fill_repos(repos_v1)
    os.chdir('bare')
    shell('mkdir storage')
    os.chdir(topdir)
    create_large_files(['1', '2', '3'])
    os.chdir(topdir)
    os.chdir('local')
    init_gitrsync(['1', '2', '3'])
    shell(exepath + ' push foobar')
    os.chdir(topdir)
    os.chdir('bare')
    os.chdir('storage')
    os.chdir('foobar')
    files = set(shell('ls'))
    assert(files == {'app 1.exe', 'app 2.exe', 'app 3.exe'})
    
def test_remote_push_filtered():
    """ We have bare and local repo. We export files to the directory name of
        which corresponds to the most recent tag that matches pattern defined
        in git config.
    """
    init_repos()
    fill_repos(repos_v1)
    os.chdir('bare')
    shell('mkdir storage')
    os.chdir(topdir)
    create_large_files(['1', '2', '3'])
    os.chdir(topdir)
    os.chdir('local')
    init_gitrsync(['1', '2', '3'])
    shell('git config --add rsync.tag fo*')
    shell(exepath + ' push')
    os.chdir(topdir)
    os.chdir('bare')
    os.chdir('storage')
    os.chdir('foo')
    files = set(shell('ls'))
    assert(files == {'app 1.exe', 'app 2.exe', 'app 3.exe'})

def test_local_push_auto():
    """ We have only local repo. We export files to the directory name of
        which corresponds to the most recent tag.
    """
    init_repos(remote=False)
    fill_repos(repos_v1, remote=False)
    shell('mkdir storage')
    create_large_files(['1', '2', '3'])
    storage = (Path(os.getcwd()) / 'storage' / '').replace('\\', '/')
    os.chdir('local')
    shell('git config --add rsync.url ' + storage)
    init_gitrsync(['1', '2', '3'])
    shell(exepath + ' push')
    os.chdir(topdir)
    os.chdir('storage')
    os.chdir('1.1.0')
    files = set(shell('ls'))
    assert(files == {'app 1.exe', 'app 2.exe', 'app 3.exe'})
    
def test_local_push_selected():
    """ We have only local repo. We export files to the directory name of
        which is specified in command line.
    """
    init_repos(remote=False)
    fill_repos(repos_v1, remote=False)
    shell('mkdir storage')
    create_large_files(['1', '2', '3'])
    storage = (Path(os.getcwd()) / 'storage' / '').replace('\\', '/')
    os.chdir('local')
    shell('git config --add rsync.url ' + storage)
    init_gitrsync(['1', '2', '3'])
    shell(exepath + ' push foobar')
    os.chdir(topdir)
    os.chdir('storage')
    os.chdir('foobar')
    files = set(shell('ls'))
    assert(files == {'app 1.exe', 'app 2.exe', 'app 3.exe'})
    
def test_local_push_filtered():
    """ We have only local repo. We export files to the directory name of
        which corresponds to the most recent tag that matches pattern defined
        in git config.
    """
    init_repos(remote=False)
    fill_repos(repos_v1, remote=False)
    shell('mkdir storage')
    create_large_files(['1', '2', '3'])
    storage = (Path(os.getcwd()) / 'storage' / '').replace('\\', '/')
    os.chdir('local')
    shell('git config --add rsync.url ' + storage)
    init_gitrsync(['1', '2', '3'])
    shell('git config --add rsync.tag fo*')
    shell(exepath + ' push')
    os.chdir(topdir)
    os.chdir('storage')
    os.chdir('foo')
    files = set(shell('ls'))
    assert(files == {'app 1.exe', 'app 2.exe', 'app 3.exe'})

