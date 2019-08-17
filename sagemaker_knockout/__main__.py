import sagemaker_knockout
import os
from daemonize import Daemonize

PIDFILE = os.environ.get('PIDFILE', '/var/run/sagemaker_knockout.pid')

if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False) == '1'
    if debug:
        sagemaker_knockout.main()
    else:
        daemon = Daemonize(app='sagemaker_knockout',
                           pid=PIDFILE, action=sagemaker_knockout.main)
        daemon.start()
