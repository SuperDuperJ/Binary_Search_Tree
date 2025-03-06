import random

class BinarySearchTree:
    def __init__(self, value, depth=1):
        self.value = value
        self.depth = depth
        self.left = None
        self.right = None


    def insert(self, value):
        if (value < self.value):
            if (self.left is None):
                self.left = BinarySearchTree(value, self.depth + 1)
            else:
                self.left.insert(value)
        else:
            if (self.right is None):
                self.right = BinarySearchTree(value, self.depth + 1)
            else:
                self.right.insert(value)
        
    def get_node_by_value(self, value):
        if (self.value == value):
            return self
        elif ((self.left is not None) and (value < self.value)):
            return self.left.get_node_by_value(value)
        elif ((self.right is not None) and (value >= self.value)):
            return self.right.get_node_by_value(value)
        else:
            return None
    
    def get_node_and_parent(self, value):
        parent = None
        current = self
        while current:
            if current.value == value:
                return current, parent
            elif value < current.value:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right
        return None, None

    def in_order_traversal(self):
        if (self.left is not None):
            self.left.depth_first_traversal()
        print(f'Depth={self.depth}, Value={self.value}')
        if (self.right is not None):
            self.right.depth_first_traversal()
    
    def decrement_depth(self):
        # Perform traversal
        if (self.left is not None):
            self.left.decrement_depth()
        # decrement depth
        self.depth -= 1
        if (self.right is not None):
            self.right.decrement_depth()
    
    def in_order_predecessor(self, value):
        poss_pred = None
        current = self
        while current:
            # if target is to the right
            if current.value < value:
                poss_pred = current
                current = current.right
            # if target is to the left
            # No update poss_pred since moving left is getting smaller
            elif current.value > value:
                current = current.left
            # current == target
            elif current.value == value:
                # if left branch exists we don't need pred anymore
                if current.left:
                    current = current.left
                    while current.right:
                        current = current.right
                    return current
                else:
                    return poss_pred
        return None
    
    def in_order_successor(self, value):
        poss_succ = None
        current = self
        while current:
            # if target is to the left
            if current.value > value:
                poss_succ = current
                current = current.left
            # if target is to the right
            # No update poss_succ since moving right is getting bigger
            elif current.value < value:
                current = current.right
            # current == target
            elif current.value == value:
                # if right branch exists we don't need parent anymore
                if current.right:
                    current = current.right
                    while current.left:
                        current = current.left
                    return current
                else:
                    return poss_succ
        return None

    def delete(self, value):
        node, parent = self.get_node_and_parent(value)
        if node is None:
            print('There is no node with that value.')
            return None
        if parent is None:
            print('You can\'t delete the root.')
            return None
        # if degree == 1
        if parent and node.left is None and node.right is None:
            if parent.left == node:
                parent.left = None
            else:
                parent.right = None
            return
        # if degree == 2
        # degree 2, case 1: node to delete only has left branch
        if parent and node.left and (node.right is None):
            if parent.right == node:
                parent.right = node.left
                parent.right.decrement_depth()
            else:
                parent.left = node.left
                parent.left.decrement_depth()
            return
        # degree 2, case 2: node to delete only has right branch
        if parent and node.right and (node.left is None):
            if parent.right == node:
                parent.right = node.right
                parent.right.decrement_depth()
            else:
                parent.left = node.right
                parent.left.decrement_depth()
            return
        # if degree == 3
        if parent and node.left and node.right:
            prev_succ = node
            # Step 1: Find in_order_successor
            current = node
            current = current.right
            while current.left:
                prev_succ = current
                current = current.left
            successor = current 
            # Step 2: Replace node's value with successor's value
            node.value = successor.value
            # Step 3: Remove successor, repair references and adjust depths
            if prev_succ == node:
                node.right = successor.right
                node.right.decrement_depth()
            else:
                prev_succ.left = successor.right
                prev_succ.left.decrement_depth()
            return

