from threading import Thread, Lock, Event
import time

lock = Lock()
uptime_history = []
energy_history = []

def reset_history():
    global uptime_history
    global energy_history
    global lock
    with lock:
        uptime_history = []
        energy_history = []

def get_uptime_history():
    global lock
    with lock:
        l = len(uptime_history)
        return uptime_history
    
def get_energy_history():
    global lock
    with lock:
        l = len(energy_history)
        return energy_history
