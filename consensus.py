# # Paxos Consensus Algorithm Implementation in Python
# import random
# import time

# class Proposer:
#     def __init__(self, proposer_id, acceptors):
#         self.proposer_id = proposer_id
#         self.acceptors = acceptors
#         self.proposal_number = 0
#         self.value = None

#     def propose(self, value):
#         self.value = value
#         self.proposal_number += 1
#         print(f"Proposer {self.proposer_id}: Proposing value '{self.value}' with proposal number {self.proposal_number}")

#         # Phase 1: Prepare Request
#         promises = 0
#         for acceptor in self.acceptors:
#             if acceptor.prepare(self.proposal_number):
#                 promises += 1
        
#         # Phase 2: Accept Request
#         if promises > len(self.acceptors) // 2:
#             print(f"Proposer {self.proposer_id}: Received majority promises, sending accept request...")
#             accepts = 0
#             for acceptor in self.acceptors:
#                 if acceptor.accept(self.proposal_number, self.value):
#                     accepts += 1
            
#             if accepts > len(self.acceptors) // 2:
#                 print(f"Proposer {self.proposer_id}: Consensus achieved on value '{self.value}'!")
#             else:
#                 print(f"Proposer {self.proposer_id}: Failed to achieve consensus.")
#         else:
#             print(f"Proposer {self.proposer_id}: Not enough promises received, aborting proposal.")

# class Acceptor:
#     def __init__(self, acceptor_id):
#         self.acceptor_id = acceptor_id
#         self.promised_id = -1
#         self.accepted_id = -1
#         self.accepted_value = None

#     def prepare(self, proposal_number):
#         if proposal_number > self.promised_id:
#             self.promised_id = proposal_number
#             print(f"Acceptor {self.acceptor_id}: Promising proposal number {proposal_number}")
#             return True
#         else:
#             print(f"Acceptor {self.acceptor_id}: Rejecting proposal number {proposal_number}")
#             return False

#     def accept(self, proposal_number, value):
#         if proposal_number >= self.promised_id:
#             self.accepted_id = proposal_number
#             self.accepted_value = value
#             print(f"Acceptor {self.acceptor_id}: Accepting value '{value}' with proposal number {proposal_number}")
#             return True
#         else:
#             print(f"Acceptor {self.acceptor_id}: Rejecting accept request for proposal number {proposal_number}")
#             return False

# # Example Usage
# acceptors = [Acceptor(i) for i in range(5)]
# proposer = Proposer(1, acceptors)
# proposer.propose("Consensus Value")

from typing import List, Dict

def OM(commander: int, nodes: List[int], value: int, x: int) -> Dict[int, int]:
    """
    OM(x) algorithm implementation for consensus with Byzantine faults.
    
    Args:
    - commander (int): The node ID of the commander issuing the initial value.
    - nodes (List[int]): List of node IDs (excluding the commander).
    - value (int): The command value issued by the commander (0 or 1).
    - x (int): The number of allowable Byzantine faults (levels of recursion).
    
    Returns:
    - Dict[int, int]: The decided value for each node.
    """
    if x == 0:
        # Base case: If no faults are tolerated, nodes directly accept the commander's value.
        return {node: value for node in nodes}
    
    # Step 1: The commander sends the initial command to each lieutenant.
    decisions = {}
    for node in nodes:
        decisions[node] = OM_Recursive(node, [n for n in nodes if n != node], value, x - 1)
    
    # Step 2: Each lieutenant applies majority voting on the received values.
    final_decisions = {}
    for node in nodes:
        # Collect the values that node has received from the other nodes
        received_values = [decisions[other][node] for other in nodes if other != node]
        # Include the direct command value
        received_values.append(value)
        # Majority vote to decide on a final value
        final_decisions[node] = 1 if received_values.count(1) > received_values.count(0) else 0
    
    return final_decisions

def OM_Recursive(commander: int, nodes: List[int], value: int, x: int) -> Dict[int, int]:
    """
    Recursive helper function for the OM(x) algorithm.
    
    Args:
    - commander (int): The node issuing the command at this recursive level.
    - nodes (List[int]): List of nodes (excluding the commander) receiving the command.
    - value (int): The command value issued by the commander (0 or 1).
    - x (int): The current level of allowable Byzantine faults.
    
    Returns:
    - Dict[int, int]: The value received by each node at this level of recursion.
    """
    if x == 0:
        return {node: value for node in nodes}
    
    # Step 1: Propagate commands recursively
    decisions = {}
    for node in nodes:
        # Send to next level with reduced fault tolerance (x - 1)
        decisions[node] = OM_Recursive(node, [n for n in nodes if n != node], value, x - 1)
    
    # Step 2: Apply majority voting to decide the final value at this recursion level
    final_decisions = {}
    for node in nodes:
        received_values = [decisions[other][node] for other in nodes if other != node]
        received_values.append(value)
        final_decisions[node] = 1 if received_values.count(1) > received_values.count(0) else 0
    
    return final_decisions

# Example Usage:
commander = 0
nodes = [1, 2, 3,4,5,6,7]  # 3 lieutenants
initial_value = 1   # Command issued by commander (0 or 1)
max_faulty_nodes = 2  # Maximum number of faulty nodes tolerated

# Get the final decision of each node
final_decisions = OM(commander, nodes, initial_value, max_faulty_nodes)
print("Final decisions:", final_decisions)