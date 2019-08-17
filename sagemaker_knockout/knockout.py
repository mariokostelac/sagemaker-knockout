import psutil
import GPUtil
import os
import sys
import logging
from time import sleep
from pprint import pprint as pp

def netcons(listen_port=None,status=None,pid=None):
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

def gpu_load():
  load = [gpu.load for gpu in GPUtil.getGPUs()]
  if not load:
    return 0.0
  return sum(load)/len(load)*100

def cpu_load(interval=1):
  return psutil.cpu_percent(interval=interval)

def jupyter_connections():
  jupyter = listen_proc(8443)
  connections = [n for n in netcons(status='ESTABLISHED', listen_port=8443, pid=jupyter.pid)]
  return connections

def setup_logger():
  fh = logging.FileHandler('/var/log/sagemaker_knockout.log')
  fmt = logging.Formatter('%(asctime)s - %(message)s')
  fh.setFormatter(fmt)
  logger = logging.getLogger('')
  logger.addHandler(fh)
  logger.setLevel(logging.INFO)

CPU_THRESHOLD=10
GPU_THRESHOLD=5
JUPYTER_CONNS_THRESHOLD=0
MEMORY_POINTS=60
CHECK_INTERVAL=60

def main():
  setup_logger()
  stats = []
  while True:
    stat = { 'cpu_load': cpu_load(), 'gpu_load': gpu_load(), 'jupyter_connections': len(jupyter_connections()) }
    stats.append(stat)
    stats = stats[-MEMORY_POINTS:]
    cpu_inactive = [s for s in stats if s['cpu_load'] <= CPU_THRESHOLD]
    gpu_inactive = [s for s in stats if s['gpu_load'] <= GPU_THRESHOLD]
    jupyter_inactive = [s for s in stats if s['jupyter_connections'] <= JUPYTER_CONNS_THRESHOLD]
    msg = f"CPU inactive: {len(cpu_inactive)}/{MEMORY_POINTS}"
    msg += f"\tGPU inactive: {len(gpu_inactive)}/{MEMORY_POINTS}"
    msg += f"\tJupyter inactive: {len(jupyter_inactive)}/{MEMORY_POINTS}"
    msg += "\tCurrent: " + str(stat)
    logging.info(msg)
    if len(cpu_inactive) == MEMORY_POINTS and len(gpu_inactive) == MEMORY_POINTS and len(jupyter_inactive) == MEMORY_POINTS:
       logging.info("Shutting down...")
       os.system("shutdown 0")
    sleep(CHECK_INTERVAL)
