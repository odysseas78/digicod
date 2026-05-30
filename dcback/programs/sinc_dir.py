import sys

from dirsync import sync
import os
import time
#hhhhhhhhhh

def sinc_encript():
    excl = [r'.{2,}venv', r'.{2,}node_modules', r'.{2,}build']

    args = {'exclude': excl, 'create': True, 'verbose': True, 'purge': True}
    sync('/home/dc', '/mnt/hgfs/shared/dc', 'sync', **args)


def sinc_encript2():
    excl = [r'.{2,}venv', r'.{2,}node_modules', r'.{2,}build']

    args = {'exclude': excl, 'create': True, 'verbose': True, 'purge': True}
    sync('/home/projects', '/mnt/hgfs/shared/projects', 'sync', **args)


def get_tree_size(path, exclude):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False) and entry.name not in exclude:
            total += get_tree_size(entry.path, exclude)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total

def main():
    _cached_stamp = 0
    _cached_stamp2 = 0
    while True:
        time.sleep(3)
        try:
            _stamp = get_tree_size('/home/dc', exclude=['venv', '.idea', 'node_modules'])
            if _cached_stamp != _stamp:
                print('Changed')
                sinc_encript()
                _cached_stamp = _stamp
        except KeyboardInterrupt:
            print('\nDone')
            break
        except FileNotFoundError:
            # Action on file not found
            pass
        except:
            print('Unhandled error: %s' % sys.exc_info()[0])
        
        try:
            _stamp2 = get_tree_size('/home/projects', exclude=['venv', '.idea', 'node_modules'])
            if _cached_stamp2 != _stamp2:
                print('Changed')
                sinc_encript2()
                _cached_stamp2 = _stamp2
        except KeyboardInterrupt:
            print('\nDone')
            break
        except FileNotFoundError:
            # Action on file not found
            pass
        except:
            print('Unhandled error: %s' % sys.exc_info()[0])


if __name__ == '__main__':
    main()