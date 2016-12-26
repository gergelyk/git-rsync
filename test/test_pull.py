from shared import *

def test_remote_pull_auto():
    """ We have bare and local repo. We import files from the directory name of
        which corresponds to the most recent tag.
    """
    init_repos()
    fill_repos(repos_v1)
    fill_storage(storage_v1)
    os.chdir('local')
    files = set(shell('ls'))
    assert(files == {'f {}'.format(i) for i in range(12)})
    os.system(exepath + ' pull')
    files = set(shell('ls'))
    assert(files == {'b 2', 'b 3'} | {'f {}'.format(i) for i in range(12)})
    
def test_remote_pull_selected():
    """ We have bare and local repo. We import files from the directory name of
        which is specified in command line.
    """
    init_repos()
    fill_repos(repos_v1)
    fill_storage(storage_v1)
    os.chdir('local')
    files = set(shell('ls'))
    assert(files == {'f {}'.format(i) for i in range(12)})
    shell(exepath + ' pull 1.0.0')
    files = set(shell('ls'))
    assert(files == {'b 0', 'b 1'} | {'f {}'.format(i) for i in range(12)})
    
def test_remote_pull_filtered():
    """ We have bare and local repo. We import files from the directory name of
        which corresponds to the most recent tag that matches pattern defined
        in git config.
    """
    init_repos()
    fill_repos(repos_v1)
    fill_storage(storage_v1)
    os.chdir('local')
    shell('git config --add rsync.tag fo*')
    files = set(shell('ls'))
    assert(files == {'f {}'.format(i) for i in range(12)})
    shell(exepath + ' pull')
    files = set(shell('ls'))
    assert(files == {'b 4', 'b 5'} | {'f {}'.format(i) for i in range(12)})
    
def test_local_pull_auto():
    """ We have only local repo. We import files from the directory name of
        which corresponds to the most recent tag.
    """
    init_repos(remote=False)
    fill_repos(repos_v1, remote=False)
    fill_storage(storage_v1, target='.')
    storage = (Path(os.getcwd()) / 'storage' / '').replace('\\', '/')
    os.chdir('local')
    shell('git config --add rsync.url ' + storage)
    files = set(shell('ls'))
    assert(files == {'f {}'.format(i) for i in range(12)})
    os.system(exepath + ' pull')
    files = set(shell('ls'))
    assert(files == {'b 2', 'b 3'} | {'f {}'.format(i) for i in range(12)})
    
def test_local_pull_selected():
    """ We have only local repo. We import files from the directory name of
        which is specified in command line.
    """
    init_repos(remote=False)
    fill_repos(repos_v1, remote=False)
    fill_storage(storage_v1, target='.')
    storage = (Path(os.getcwd()) / 'storage' / '').replace('\\', '/')
    os.chdir('local')
    shell('git config --add rsync.url ' + storage)
    files = set(shell('ls'))
    assert(files == {'f {}'.format(i) for i in range(12)})
    shell(exepath + ' pull 1.0.0')
    files = set(shell('ls'))
    assert(files == {'b 0', 'b 1'} | {'f {}'.format(i) for i in range(12)})
    
def test_local_pull_filtered():
    """ We have only local repo. We import files from the directory name of
        which corresponds to the most recent tag that matches pattern defined
        in git config.
    """
    init_repos(remote=False)
    fill_repos(repos_v1, remote=False)
    fill_storage(storage_v1, target='.')
    storage = (Path(os.getcwd()) / 'storage' / '').replace('\\', '/')
    os.chdir('local')
    shell('git config --add rsync.url ' + storage)
    shell('git config --add rsync.tag fo*')
    files = set(shell('ls'))
    assert(files == {'f {}'.format(i) for i in range(12)})
    shell(exepath + ' pull')
    files = set(shell('ls'))
    assert(files == {'b 4', 'b 5'} | {'f {}'.format(i) for i in range(12)})


