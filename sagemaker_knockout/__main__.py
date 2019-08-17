import sagemaker_knockout
import os
from daemonize import Daemonize

PIDFILE = os.environ.get('PIDFILE', '/var/run/sagemaker_knockout.pid')

if __name__ == "__main__":
    no_deamon = os.environ.get('NO_DEAMON', False) == '1'
    if no_deamon:
        sagemaker_knockout.main()
    else:
        daemon = Daemonize(app='sagemaker_knockout', pid=PIDFILE, action=sagemaker_knockout.main)
        daemon.start()
