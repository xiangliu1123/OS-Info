import os
import sys
import time
import threading
import queue

# This will use a queue for IPC as a demonstration.
ipc_queue = queue.Queue()

# Print put for components
class Process:
    def __init__(self, pid, parent_pid):
        self.pid = pid
        self.parent_pid = parent_pid
        self.state = 'RUNNING'
        self.threads = []

    def terminate(self):
        self.state = 'TERMINATED'

    def info(self):
        return f"PID: {self.pid}, Parent PID: {self.parent_pid}, State: {self.state}"


class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutex = threading.Lock()
        self.semaphore = threading.Semaphore()

    def run(self):
        # of mutex locking
        with self.mutex:
            time.sleep(2)
            ipc_queue.put(f"Thread {self.name} completed.")


processes = {}


def create_process():
    # Using fork to create a child process
    pid = os.fork()

    if pid == 0:  # Child Process
        # Replacing the child's image with a new instance of Python interpreter
        os.execvp('python3', ['python3', __file__])  # This will run the same script in a new instance
    else:  # Parent Process
        parent_pid = os.getpid()
        # Create an object for the child process
        process = Process(pid, parent_pid)
        processes[pid] = process
        print(f"Child process with PID {pid} created. Parent PID: {parent_pid}")



# List process
def list_processes():
    for pid, process in processes.items():
        print(process.info())

# Terminate Process
def terminate_process(pid):
    if pid in processes:
        processes[pid].terminate()
        print(f"Process with PID {pid} terminated.")
    else:
        print(f"No process with PID {pid}.")

# create thread follow by the process ID
def create_thread(pid):
    if pid not in processes:
        print(f"No process with PID {pid}.")
        return

    process = processes[pid]
    thread = CustomThread()
    process.threads.append(thread)
    thread.start()
    print(f"Thread {thread.name} started for process {pid}.")

# list thread follow by the process ID
def list_threads(pid):
  # check for PID
    if pid not in processes:
        print(f"No process with PID {pid}.")
        return
    # check for PID's process threads
    process = processes[pid]
    if not process.threads:
        print(f"Process with PID {pid} has no threads.")
        return

    print(f"Threads for process {pid}:")
    for thread in process.threads:
        print(f"Thread Name: {thread.name}, Status: {'Alive' if thread.is_alive() else 'Not Alive'}")


def main():
    print("Comand:")
    print("cp = Create process")
    print("lp = List process")
    print("tp, = List process")
    print("ct,PID = Create Thread follow by the process ID")
    print("lt, PID = List threads follow by the process ID")
    print("ri = Read IPC")

    while True:
        cmd = input("Enter Command: ")

        if cmd == "cp":
            create_process()
        elif cmd == "lp":
            list_processes()
        elif cmd.startswith("tp"):
            _, pid = cmd.split()
            terminate_process(int(pid))
        elif cmd.startswith("ct"):
            _, pid = cmd.split()
            create_thread(int(pid))
        elif cmd == "ri":
            while not ipc_queue.empty():
                print(ipc_queue.get())
        elif cmd.startswith("lt"):
            _, pid = cmd.split()
            list_threads(int(pid))
        elif cmd == "exit":
            sys.exit(0)
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
