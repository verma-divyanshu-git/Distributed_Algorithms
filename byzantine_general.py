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
    print(f"\n[OM] Starting OM({x}) with commander {commander} sending value {value} to nodes {nodes}")
    
    if x == 0:
        # Base case: If no faults are tolerated, nodes directly accept the commander's value.
        final_decisions = {node: value for node in nodes}
        print(f"[OM] Level {x}: All nodes directly accept the commander's value: {final_decisions}")
        return final_decisions
    
    # Step 1: The commander sends the initial command to each lieutenant.
    decisions = {}
    for node in nodes:
        print(f"\n[OM] Commander {commander} sends value {value} to node {node}")
        decisions[node] = OM_Recursive(node, [n for n in nodes if n != node], value, x - 1)
    
    # Step 2: Each lieutenant applies majority voting on the received values.
    final_decisions = {}
    for node in nodes:
        # Collect the values that node has received from the other nodes
        received_values = [decisions[other][node] for other in nodes if other != node]
        # Include the direct command value
        received_values.append(value)
        # Majority vote to decide on a final value
        final_value = 1 if received_values.count(1) > received_values.count(0) else 0
        final_decisions[node] = final_value
        print(f"[OM] Node {node} received values {received_values} and decides on {final_value}")
    
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
        print(f"    [OM-Recursive] Level {x}: Nodes {nodes} accept value {value} directly from commander {commander}")
        return {node: value for node in nodes}
    
    print(f"\n    [OM-Recursive] Commander {commander} at level {x} sending value {value} to nodes {nodes}")
    # Step 1: Propagate commands recursively
    decisions = {}
    for node in nodes:
        print(f"    [OM-Recursive] Commander {commander} sends value {value} to node {node} at level {x - 1}")
        decisions[node] = OM_Recursive(node, [n for n in nodes if n != node], value, x - 1)
    
    # Step 2: Apply majority voting to decide the final value at this recursion level
    final_decisions = {}
    for node in nodes:
        received_values = [decisions[other][node] for other in nodes if other != node]
        received_values.append(value)
        final_value = 1 if received_values.count(1) > received_values.count(0) else 0
        final_decisions[node] = final_value
        print(f"    [OM-Recursive] Node {node} at level {x} received values {received_values} and decides on {final_value}")
    
    return final_decisions

# Example Usage:
commander = 0
nodes = [1, 2, 3]  # 3 lieutenants
initial_value = 1   # Command issued by commander (0 or 1)
max_faulty_nodes = 1  # Maximum number of faulty nodes tolerated

# Get the final decision of each node
final_decisions = OM(commander, nodes, initial_value, max_faulty_nodes)
print("\nFinal decisions:", final_decisions)