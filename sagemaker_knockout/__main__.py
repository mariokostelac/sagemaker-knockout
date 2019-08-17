import os
import sys
import click
import logging
from sagemaker_knockout.knockout import knockout_loop
from daemonize import Daemonize


def setup_logger(dst):
    if dst == '-':
        logging.basicConfig(stream=sys.stdout,
                            format='%(asctime)s - %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(
            filename=dst, format='%(asctime)s - %(message)s', level=logging.INFO)


def daemon_action(logger_dst):
    setup_logger(logger_dst)
    knockout_loop()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--daemonize/--no-daemonize', default=False)
@click.option('--logfile', default='/var/log/sagemaker_knockout.log')
@click.option('--pidfile', default='/var/run/sagemaker_knockout.pid')
def run(daemonize, logfile, pidfile):
    if daemonize:
        daemon = Daemonize(app='sagemaker_knockout',
                           pid=pidfile, action=daemon_action)
        daemon.start()
    else:
        setup_logger(dst=logfile)
        knockout_loop()


if __name__ == "__main__":
    cli()
