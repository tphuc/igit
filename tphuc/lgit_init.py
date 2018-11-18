from lgit_lib import *

def init():
    # Make dir structure
    os.mkdir('.lgit')
    os.mkdir('.lgit/objects')
    os.mkdir('.lgit/commits')
    os.mkdir('.lgit/snapshots')
    with open('.lgit/index', 'w'):
        pass
    with open('.lgit/config', 'w') as f:
        f.write(os.environ['LOGNAME'] + '\n')
    os.mkdir('.lgit/refs')
    os.mkdir('.lgit/refs/heads')
    with open('.lgit/HEAD', 'w') as f:
        f.write('master')
    with open('.lgit/refs/heads/master', 'w') as f:
        pass
