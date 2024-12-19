import threading
import time
from queue import PriorityQueue
from typing import Dict, List, Tuple

class Site:
    def __init__(self, site_id: int, total_sites: int):
        self.site_id = site_id
        self.timestamp = 0
        self.request_queue = PriorityQueue()
        self.request_set = set(range(total_sites)) - {self.site_id}
        self.replies_received = 0
        self.cs_lock = threading.Lock()
        self.in_cs = False
        self.waiting_for_cs = False

    def send_request(self, sites: Dict[int, 'Site']):
        self.timestamp += 1
        request = (self.timestamp, self.site_id)
        self.request_queue.put(request)
        self.waiting_for_cs = True
        print(f"Site {self.site_id} is requesting the CS at timestamp {self.timestamp}.")
        
        for site_id in self.request_set:
            sites[site_id].receive_request(request, sites)

    def receive_request(self, request: Tuple[int, int], sites: Dict[int, 'Site']):
        self.timestamp = max(self.timestamp, request[0]) + 1
        self.request_queue.put(request)
        print(f"Site {self.site_id} received request from Site {request[1]} at timestamp {request[0]}.")
        
        # Send a reply to the requesting site
        site_id = request[1]
        sites[site_id].receive_reply(self.site_id)

    def receive_reply(self, site_id: int):
        self.replies_received += 1
        print(f"Site {self.site_id} received reply from Site {site_id}.")
    
    def send_release(self, sites: Dict[int, 'Site']):
        print(f"Site {self.site_id} is releasing the CS.")
        for site_id in self.request_set:
            sites[site_id].receive_release(self.site_id)

    def receive_release(self, site_id: int):
        # Remove request from the queue if it's at the top
        top_request = self.request_queue.queue[0]
        if top_request[1] == site_id:
            self.request_queue.get()
            print(f"Site {self.site_id} removed Site {site_id}'s request from the queue.")
        
    def can_enter_cs(self):
        top_request = self.request_queue.queue[0]
        return (top_request[1] == self.site_id) and (self.replies_received == len(self.request_set))
    
    def request_cs(self, sites: Dict[int, 'Site']):
        self.send_request(sites)
        
        # Wait until conditions for entering CS are met
        while not self.can_enter_cs():
            time.sleep(0.1)  # Allow other threads to proceed
            
        # Enter CS
        self.cs_lock.acquire()
        self.in_cs = True
        print(f"Site {self.site_id} is entering the CS at timestamp {self.timestamp}.")
        
        # Simulate CS execution
        time.sleep(1)
        
        self.release_cs(sites)
        self.cs_lock.release()

    def release_cs(self, sites: Dict[int, 'Site']):
        # Exit CS and send RELEASE message
        self.in_cs = False
        self.request_queue.get()  # Remove own request from queue
        self.replies_received = 0  # Reset replies count for next CS request
        self.send_release(sites)
        print(f"Site {self.site_id} exited the CS.")

# Test case to verify mutual exclusion
def test_lamport_mutex():
    total_sites = 3
    sites = {i: Site(i, total_sites) for i in range(total_sites)}
    
    # Site 0, Site 1, and Site 2 will request the critical section
    def site_routine(site_id: int):
        sites[site_id].request_cs(sites)
    
    threads = [threading.Thread(target=site_routine, args=(i,)) for i in range(total_sites)]
    
    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check that mutual exclusion was respected
    for i in range(total_sites):
        assert not sites[i].in_cs, f"Site {i} is still in the CS after release."

    print("Test completed: Mutual exclusion verified.")

# Run the test
test_lamport_mutex()