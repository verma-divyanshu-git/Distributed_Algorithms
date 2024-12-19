class TreeNode:
    def __init__(self, node_id, grants_permission=True, left=None, right=None):
        self.node_id = node_id
        self.grants_permission = grants_permission  # Whether this node grants permission for quorum
        self.left = left  # Left child
        self.right = right  # Right child

    def __repr__(self):
        return f"Node({self.node_id}, Permission: {self.grants_permission})"


def get_quorum(tree: TreeNode):
    # Base case: If the tree is empty, return None indicating no quorum
    if tree is None:
        return None

    # If the node grants permission, we proceed to get the quorum from left or right child
    if tree.grants_permission:
        # Get quorum from both left and right children
        left_quorum = get_quorum(tree.left)
        right_quorum = get_quorum(tree.right)

        # If both left and right children have valid quorums, return their union
        if left_quorum is not None and right_quorum is not None:
            return {tree.node_id} | left_quorum | right_quorum
        # If left child has valid quorum, return it
        elif left_quorum is not None:
            return {tree.node_id} | left_quorum
        # If right child has valid quorum, return it
        elif right_quorum is not None:
            return {tree.node_id} | right_quorum
        else:
            return {tree.node_id} 
    else:
        # If the current node doesn't grant permission, try to get quorum from both children
        left_quorum = get_quorum(tree.left)
        right_quorum = get_quorum(tree.right)

        # If either left or right quorum is None, return None (no quorum)
        if left_quorum is None or right_quorum is None:
            return None
        else:
            # Return the union of both quorums
            return left_quorum | right_quorum


def construct_tree():
    # Constructing a tree as an example
    leaf1 = TreeNode(5, grants_permission=True)
    leaf2 = TreeNode(6, grants_permission=True)
    leaf3 = TreeNode(7, grants_permission=False)  # This node grants permission
    leaf4 = TreeNode(8, grants_permission=True)  # This node grants permission

    node2 = TreeNode(2, grants_permission=True, left=leaf1, right=leaf2)
    node3 = TreeNode(3, grants_permission=True, left=leaf3, right=leaf4)

    root = TreeNode(1, grants_permission=True, left=node2, right=node3)

    return root


# Driver code
tree_root = construct_tree()
quorum = get_quorum(tree_root)

if quorum is None:
    print("Quorum could not be established.")
else:
    print(f"Quorum Set: {quorum}")