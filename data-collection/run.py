import subprocess
import time
import signal
import os
import threading 

python_interpreter = 'myenv/bin/python'

motion_script = 'ambient-sensors/motion.py'
netatmo_script = 'ambient-sensors/netatmo.py'
intellicare_script = 'main.py'

# List of processes to manage
processes = []

# def start_processes():
#     processes.append(subprocess.Popen(['python3', motion_script]))
#     processes.append(subprocess.Popen(['python3', netatmo_script]))

# def stop_processes():
#     for process in processes:
#         try:
#             os.killpg(os.getpgid(process.pid), signal.SIGTERM)
#         except ProcessLookupError:
#             print(f"Process {process.pid} already terminated.")
            

# try:
#     print("Starting all sensor scripts...")
#     start_processes()
#     duration = 3600  # run for 1 hour
#     time.sleep(duration)
# finally:
#     print("Stopping all sensor scripts...")
#     stop_processes()


def start_process(script):
    process = subprocess.Popen(['python3', script], preexec_fn=os.setsid)
    processes.append(process)
    return process

def stop_process(process):
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except ProcessLookupError:
        print(f"Process {process.pid} already terminated.")

def monitor_processes():
    while True:
        for process in processes:
            if process.poll() is not None:  # Check if the process has stopped
                print(f"Process {process.pid} has stopped. Restarting...")
                processes.remove(process)  # Remove the stopped process
                if process.args[1] == motion_script:
                    start_process(motion_script)
                elif process.args[1] == netatmo_script:
                    start_process(netatmo_script)
        time.sleep(10)  # Check every 10 seconds

def start_all_processes():
    start_process(motion_script)
    start_process(netatmo_script)

def stop_all_processes():
    for process in processes:
        stop_process(process)

try:
    print("Starting all sensor scripts...")
    start_all_processes()
    duration = 3600  # Run for 1 hour
    monitor_processes_thread = threading.Thread(target=monitor_processes, daemon=True)
    monitor_processes_thread.start()
    time.sleep(duration)
finally:
    print("Stopping all sensor scripts...")
    stop_all_processes()