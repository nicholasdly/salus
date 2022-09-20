
class Node:
    """
    Represents a Node object, which are points on an AVL tree that store data.
    Modified to better represent the financial security data.
    """

    def __init__(self, index, data):
        """
        Initializes a Node object with given data.
        """
        # Tree-related properties
        self.height = 1
        self.left = None
        self.right = None

        # Data-related properties
        self.index = index
        self.data = data

    def __str__(self):
        """
        Returns a string representation of the Node for readability.
        """
        return str(self.index)

    def __repr__(self):
        """
        Returns a string representation of the Node for debugging.
        """
        return repr(self.index)

class AVLTree:
    """
    Represents an AVL Tree data structure that has been slightly modified to
    better represent the financial security data.
    """

    def __init__(self):
        """
        Initializes an AVL tree.
        """
        self.root = None

    def __str__(self):
        """
        Returns a string representation of the AVL tree for readability.
        """
        dataset = [str(node) for node in self.inorder(self.root)]
        return "[" + ", ".join(dataset) + "]"

    def __repr__(self):
        """
        Returns a string representation of the AVL tree for debugging.
        """
        dataset = [repr(node) for node in self.inorder(self.root)]
        return "[" + ", ".join(dataset) + "]"

    def leftRotate(self, node):
        """
        Applies a left rotation at a specific node in the AVL tree.
        """
        temp = node.right

        # Apply rotation
        node.right.left, node.right = node, node.right.left

        # Update heights
        node.height = 1 + max(
            self.getHeight(node.left), self.getHeight(node.right)
        )
        temp.height = 1 + max(
            self.getHeight(temp.left), self.getHeight(temp.right)
        )
        
        return temp

    def rightRotate(self, node):
        """
        Applies a right rotation at a specific node in the AVL tree.
        """
        temp = node.left

        # Apply rotation
        node.left.right, node.left = node, node.left.right

        # Update heights
        node.height = 1 + max(
            self.getHeight(node.left), self.getHeight(node.right)
        )
        temp.height = 1 + max(
            self.getHeight(temp.left), self.getHeight(temp.right)
        )

        return temp

    def getBalance(self, node):
        """
        Returns the balance factor of a specific node in the AVL tree.
        """
        if node is None:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def getHeight(self, node):
        """
        Returns the height of a specific node in the AVL tree.
        """
        if node is None:
            return 0
        return node.height

    def inorder(self, node):
        """
        Represents an iterator that iterates the AVL tree through in-order
        traversal.
        """
        if node:
            yield from self.inorder(node.left)
            yield node
            yield from self.inorder(node.right)

    def insert(self, node, index, data):
        """
        Inserts data into the AVL tree as a new node.
        """
        # Inserts node into tree
        if node is None:
            return Node(index, data)
        if index < node.index:
            node.left = self.insert(node.left, index, data)
        elif index > node.index:
            node.right = self.insert(node.right, index, data)

        # Update node height
        node.height = 1 + max(
            self.getHeight(node.left), self.getHeight(node.right)
        )

        # Balances the tree
        balance = self.getBalance(node)
        if balance > 1:
            if index < node.left.index:
                return self.rightRotate(node)
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        elif balance < -1:
            if index > node.right.index:
                return self.leftRotate(node)
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node
