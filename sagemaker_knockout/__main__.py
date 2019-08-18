import os
import sys
import click
import logging
import psutil
import functools
from sagemaker_knockout.knockout import knockout_loop
from daemonize import Daemonize


def setup_logger(dst):
    if dst == '-':
        logging.basicConfig(stream=sys.stdout,
                            format='%(asctime)s - %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(
            filename=dst, format='%(asctime)s - %(message)s', level=logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--daemonize/--no-daemonize', default=False)
@click.option('--logfile', default='/home/ec2-user/SageMaker/sagemaker_knockout.log')
@click.option('--pidfile', default='/var/run/sagemaker_knockout.pid')
@click.option('-i', '--max-inactive-minutes', default=60)
def run(daemonize, logfile, pidfile, max_inactive_minutes):
    setup_logger(dst=logfile)
    max_inactive_minutes = int(max_inactive_minutes)
    if daemonize:
        if logfile == '-':
            print('Logfile cannot be stdout if --daemonize is passed')
            exit(1)
        action = functools.partial(knockout_loop, max_inactive_minutes)
        daemon = Daemonize(app='sagemaker_knockout',
                           pid=pidfile, action=action, auto_close_fds=False, logger=logging.getLogger(''))
        daemon.start()
    else:
        knockout_loop(max_inactive_minutes)


@cli.command()
@click.option('--pidfile', default='/var/run/sagemaker_knockout.pid')
def check_daemon(pidfile):
    if not os.path.exists(pidfile):
        print(f'🔴 Pidfile {pidfile} does not exist')
        exit(1)

    with open(pidfile, 'r') as fd:
        pid = int(fd.read())
        if not psutil.pid_exists(pid):
            print(f'🔴 Process with pid {pid} does not exist!')
            exit(1)
        print('✅ Daemon found')


if __name__ == "__main__":
    cli()
