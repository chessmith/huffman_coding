class Node:
    def __init__(self, freq: int, char: str, left=None, right=None):
        """
        Initialize a node for the binary tree used in Huffman encoding.

        Args:
        freq (int): frequency of the character
        char (str): character stored in the node
        left (Node): left child node
        right (Node): right child node
        """
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        """
        Defines the '<' operator for nodes. This is used when comparing nodes in a priority queue.

        Args:
        other (Node): node being compared to

        Returns:
        bool: True if self's frequency is less than other's frequency, False otherwise
        """
        return self.freq < other.freq

    def __eq__(self, other):
        """
        Defines the '==' operator for nodes. This is used when comparing nodes in a priority queue.

        Args:
        other (Node): node being compared to

        Returns:
        bool: True if self's frequency is equal to other's frequency, False otherwise
        """
        return self.freq == other.freq

    def __gt__(self, other):
        """
        Defines the '>' operator for nodes. This is used when comparing nodes in a priority queue.

        Args:
        other (Node): node being compared to

        Returns:
        bool: True if self's frequency is greater than other's frequency, False otherwise
        """
        return self.freq > other.freq

    def __repr__(self):
        """
        Returns a string representation of the node.

        Returns:
        str: a string representation of the node
        """
        return f"Node({self.freq}, {self.char})"
