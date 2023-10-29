# Advanced Process Manager with Process Synchronization

## Implemented Functionalities:
- Process Creation: This functionality allows for the creation of new child processes.
- Process Listing: List all the active processes.
- Process Termination: Terminate a specified process using its Process ID (PID).
- Thread Creation: Create a thread within a specified process.
- Thread Listing: List all the threads for a specific process.
- Inter-thread Communication (IPC) using Queue: Read messages sent from threads, demonstrating basic IPC.

## Test Results:
### Process Creation:

- Command: cp

- Figure:
Child process with PID 20459 created. Parent PID: 19935

### Process Listing:
- Command: lp
- Figure:
PID: 20459, Parent PID: 19935, State: RUNNING

### Process Termination:
- Command: tp, 20459
- Figure:
Process with PID 20459 terminated.

### Thread Creation:
- Command: Enter Command: ct, 21084
- Figure:
Thread Thread-10 started for process 21084. 
### Thread Listing:
- Command: Enter Command: lt, 21084
- Figure:
Threads for process 21084:
Thread Name: Thread-10, Status: Alive
### Inter-thread Communication:
- Command: Enter Command: ri
- Figure: Thread Thread-10 completed.

# Discussion on the Project Result:
The project successfully implements a simple system for inter-process and inter-thread communication and management. The user can create, list, and terminate processes as well as manage threads within those processes. The system utilizes Python's native modules for processes, threads, and queues.

The queue.Queue() is used as an IPC mechanism to communicate messages from threads. This proves to be an efficient method for IPC in Python, especially for thread-to-thread communication.

The use of the os.fork() method allows the parent process to spawn child processes. The child processes run a new instance of the Python interpreter, and their behavior is defined within the create_process() function.

Threads within a process utilize mutex locks to ensure synchronized access to shared resources, in this case, the IPC queue. This ensures thread-safe operations when multiple threads try to communicate simultaneously.

The project provides an interactive interface where users can enter commands to manage processes and threads. This interface is crucial for testing the functionalities and visualizing the IPC mechanism in action.

In conclusion, the system provides a basic demonstration of IPC mechanisms, process, and thread management in Python. Future improvements could include implementing more advanced IPC mechanisms like shared memory or pipes and enhancing the user interface for better user experience.
