import threading
import time
import random


class Process:
    def __init__(self, pid, num_processes):
        self.pid = pid
        self.num_processes = num_processes
        self.state = f"Initial state of process {pid}"
        self.channels = {i: [] for i in range(num_processes)}  # Communication channels
        self.snapshot_marker_received = [False] * (num_processes)
        self.snapshot_marker_received[self.pid] = True
        self.snapshots = []
        self.recording = False
        self.lock = threading.Lock()

    def send_message(self, to_pid, message):
        """Send a message to another process."""
        print(f"Process {self.pid} sends message to process {to_pid}: {message}")
        time.sleep(0.5)
        processes[to_pid].receive_message(self.pid, message)

    def receive_message(self, from_pid, message):
        """Receive a message from another process."""
        print(f"Process {self.pid} receives message from process {from_pid}: {message}")
        if self.recording:
            with self.lock:
                self.channels[from_pid].append(message)

    def initiate_snapshot(self):
        """Initiate the snapshot process by sending markers to all processes."""
        print(f"Process {self.pid} initiates a snapshot.")
        self.save_state()
        self.recording = True
        for i in range(self.num_processes):
            if i != self.pid:
                self.send_marker(i)

    def send_marker(self, to_pid):
        """Send a snapshot marker to another process."""
        print(f"Process {self.pid} sends marker to process {to_pid}")
        time.sleep(0.1)
        processes[to_pid].receive_marker(self.pid)

    def receive_marker(self, from_pid):
        """Receive a snapshot marker from another process."""
        print(f"Process {self.pid} receives marker from process {from_pid}")
        if not self.recording:
            self.save_state()
            self.recording = True
            for i in range(self.num_processes):
                if i != self.pid:
                    self.send_marker(i)
        self.snapshot_marker_received[from_pid] = True
        if all(self.snapshot_marker_received):
            self.finish_snapshot()

    def save_state(self):
        """Save the state of the process."""
        print(f"Process {self.pid} saves its state: {self.state}")
        self.snapshots.append(self.state)

    def finish_snapshot(self):
        """Finish recording the snapshot."""
        print(f"Process {self.pid} finishes recording snapshot.")
        for pid, messages in self.channels.items():
            if pid != self.pid:
                print(f"Channel from {pid} to {self.pid}: {messages}")
        self.recording = False
        global_snapshots[self.pid] = (self.snapshots[-1], self.channels.copy())
        check_global_snapshot()


# Create a list of processes
num_processes = 3
processes = [Process(i, num_processes) for i in range(num_processes)]
global_snapshots = [None] * num_processes  # Store global snapshot


# Function to check if all processes have finished their snapshot
def check_global_snapshot():
    if all(snapshot is not None for snapshot in global_snapshots):
        print("\n--- Global Snapshot ---")
        for pid, (state, channels) in enumerate(global_snapshots):
            print(f"Process {pid} state: {state}")
            for channel_pid, messages in channels.items():
                if channel_pid != pid:
                    print(f"  Channel from {channel_pid} to {pid}: {messages}")
        print("--- End of Global Snapshot ---\n")


# Function to simulate events and initiate the snapshot
def simulate_events():
    # Simulate message passing, but ensure they happen after snapshot initiation
    threading.Timer(
        1, lambda: processes[0].send_message(1, "Message 1 from P0 to P1")
    ).start()
    threading.Timer(
        2, lambda: processes[1].send_message(2, "Message 2 from P1 to P2")
    ).start()

    # P0 initiates the snapshot a bit later
    time.sleep(2)  # Ensure some events happen before snapshot
    processes[0].initiate_snapshot()

    threading.Timer(
        3, lambda: processes[2].send_message(0, "Message 3 from P2 to P0")
    ).start()
    threading.Timer(
        4, lambda: processes[1].send_message(0, "Message 4 from P1 to P0")
    ).start()


simulate_events()
