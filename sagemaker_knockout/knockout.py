import psutil
import GPUtil
import os
import sys
import logging
from time import sleep
from pprint import pprint as pp
from datetime import datetime, timedelta


def netcons(listen_port=None, status=None, pid=None):
    cons = [n for n in psutil.net_connections()]
    if status:
        cons = [c for c in cons if c.status == status]
    if listen_port:
        cons = [c for c in cons if c.laddr.port == listen_port]
    if pid:
        cons = [c for c in cons if c.pid == pid]
    return cons


def listen_procs(port=None):
    cons = netcons(listen_port=port, status='LISTEN')
    return [psutil.Process(c.pid) for c in cons]


def listen_proc(port):
    return listen_procs(port)[0]


def get_gpu_load():
    load = [gpu.load for gpu in GPUtil.getGPUs()]
    if not load:
        return 0.0
    return sum(load)/len(load)*100


def get_cpu_load(interval=1):
    return psutil.cpu_percent(interval=interval)


def get_jupyter_connections():
    jupyter = listen_proc(8443)
    connections = [n for n in netcons(
        status='ESTABLISHED', listen_port=8443, pid=jupyter.pid)]
    return connections


CPU_THRESHOLD = 10
GPU_THRESHOLD = 5
JUPYTER_CONNS_THRESHOLD = 1
CHECK_INTERVAL = 30
CONSECUTIVE_INTERVALS_ACTIVE = 3

def _loop(max_inactive_minutes):
    logging.info("Starting the watcher loop. Max inactivity interval %sm", max_inactive_minutes)
    now = datetime.now()
    cpu_last_active, gpu_last_active, jupyter_last_active = now, now, now
    cpu_active_intervals, gpu_active_intervals = 0, 0
    max_inactive_interval = timedelta(minutes=max_inactive_minutes)
    while True:
        cpu_load, gpu_load, jupyter_connections = get_cpu_load(
        ), get_gpu_load(), get_jupyter_connections()

        if cpu_load >= CPU_THRESHOLD:
            cpu_active_intervals += 1
            if cpu_active_intervals >= CONSECUTIVE_INTERVALS_ACTIVE:
                logging.info("Marking CPU as active")
                cpu_last_active = datetime.now()
        else:
            cpu_active_intervals = 0

        if gpu_load >= GPU_THRESHOLD:
            gpu_active_intervals += 1
            if gpu_active_intervals >= CONSECUTIVE_INTERVALS_ACTIVE:
                logging.info("Marking GPU as active")
                gpu_last_active = datetime.now()
        else:
            gpu_active_intervals = 0

        if len(jupyter_connections) >= JUPYTER_CONNS_THRESHOLD:
            logging.info("Marking Jupyter as active")
            jupyter_last_active = datetime.now()

        msg = f"CPU last active: {cpu_last_active.time().strftime('%H:%M:%S')}"
        msg += f" | GPU last active: {gpu_last_active.time().strftime('%H:%M:%S')}"
        msg += f" | Jupyter last active: {jupyter_last_active.time().strftime('%H:%M:%S')}"
        msg += f" | CPU: {cpu_load}% | GPU: {gpu_load}% | Jupyter: {len(jupyter_connections)} connections"
        logging.info(msg)

        now = datetime.now()
        cpu_inactive = (now - cpu_last_active) > max_inactive_interval
        gpu_inactive = (now - gpu_last_active) > max_inactive_interval
        jupyter_inactive = (now - jupyter_last_active) > max_inactive_interval
        if cpu_inactive and gpu_inactive and jupyter_inactive:
            logging.info("Shutting down...")
            os.system("shutdown 0")
        sleep(CHECK_INTERVAL)


def knockout_loop(max_inactive_minutes):
    try:
        _loop(max_inactive_minutes)
    except Exception as e:
        logging.exception("Knockout loop crashed with exception %s", e)
