import os
import sys
import time
import threading
import queue
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# This will use a queue for IPC as a demonstration.
ipc_queue = queue.Queue()

class Process:
    def __init__(self, pid, parent_pid):
        self.pid = pid
        self.parent_pid = parent_pid
        self.state = 'RUNNING'
        self.threads = []

    def terminate(self):
        self.state = 'TERMINATED'
        logging.info(f"Process {self.pid} terminated.")

    def info(self):
        return f"PID: {self.pid}, Parent PID: {self.parent_pid}, State: {self.state}"


class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutex = threading.Lock()
        self.semaphore = threading.Semaphore()

    def run(self):
        with self.mutex:
            time.sleep(2)
            ipc_queue.put(f"Thread {self.name} completed.")
            logging.info(f"Thread {self.name} completed.")


processes = {}


def create_process():
    pid = os.fork()

    if pid == 0:
        os.execvp('python3', ['python3', __file__])
    else:
        parent_pid = os.getpid()
        process = Process(pid, parent_pid)
        processes[pid] = process
        logging.info(f"Child process with PID {pid} created. Parent PID: {parent_pid}.")


def list_processes():
    logging.info("Listing processes:")
    for pid, process in processes.items():
        logging.info(process.info())


def terminate_process(pid):
    if pid in processes:
        processes[pid].terminate()
    else:
        logging.warning(f"No process with PID {pid}.")


def create_thread(pid):
    if pid not in processes:
        logging.warning(f"No process with PID {pid}.")
        return

    process = processes[pid]
    thread = CustomThread()
    process.threads.append(thread)
    thread.start()
    logging.info(f"Thread {thread.name} started for process {pid}.")


def list_threads(pid):
    if pid not in processes:
        logging.warning(f"No process with PID {pid}.")
        return

    process = processes[pid]
    logging.info(f"Listing threads for process {pid}:")
    for thread in process.threads:
        logging.info(f"Thread Name: {thread.name}, Status: {'Alive' if thread.is_alive() else 'Not Alive'}")


def main():
    logging.info("Starting the program...")

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
                logging.info(ipc_queue.get())
        elif cmd.startswith("lt"):
            _, pid = cmd.split()
            list_threads(int(pid))
        elif cmd == "exit":
            logging.info("Exiting the program.")
            sys.exit(0)
        else:
            logging.warning("Unknown command.")


if __name__ == "__main__":
    main()
