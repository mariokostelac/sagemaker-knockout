import sagemaker_knockout
from daemonize import Daemonize

PIDFILE='/var/run/sagemaker_knockout.pid'

if __name__ == "__main__":
  daemon = Daemonize(app="sagemaker_knockout", pid=PIDFILE, action=sagemaker_knockout.main)
  daemon.start()
