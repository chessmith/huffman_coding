import heapq
from collections import Counter, deque
from pathlib import Path
from node import Node

Pathlike = str | Path


# Count the frequency of each character in a given file.
def _count_chars(filename: str):
    # Open the file and read its contents
    with open(filename) as f:
        # Encode the text as utf-8, decode as ascii to remove non-ascii characters
        text = f.read().encode('utf-8').decode('ascii', errors='ignore')
    # Count the frequency of each character in the text
    c = Counter(text)
    return c


# Build a Huffman encoding binary tree given a counter of character frequencies.
def _build_huffman_tree(counter: Counter):
    # Convert the counter to a list of nodes
    nodes = []
    for char, freq in counter.items():
        heapq.heappush(nodes, Node(freq, char))
    # Build the binary tree by combining nodes with the lowest frequency until there is only one node left
    while len(nodes) > 1:
        # Get the two nodes with the lowest frequency
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        # Create a new node with the sum of the frequencies
        new_node = Node(left.freq + right.freq, None, left=left, right=right)
        # Add the new node to the priority queue
        heapq.heappush(nodes, new_node)
    # The last node in the list is the root of the binary tree
    return nodes[0]


# Traverse the binary tree and create a dictionary of characters and their codes.
def _traverse_tree(node: Node, code: int = 0, length: int = 0, codes: dict[str, tuple[int, int]] = None):
    if codes is None:
        codes = dict()
    if node.char is not None:
        # If the current node is a leaf, add its code to the dictionary
        codes[node.char] = (code, length)
        return codes
    # If the current node is not a leaf, traverse its left and right subtrees
    _traverse_tree(node.left, (code << 1), length + 1, codes)
    _traverse_tree(node.right, (code << 1) + 1, length + 1, codes)
    return codes


# Compress a text using the Huffman binary tree.
def _compress_text(text: str, codes: dict[str, tuple[int, int]]):
    compressed = 0
    i = 0
    b = []
    # Encode each character using its code and concatenate the encoded bits into bytes
    for c in text:
        compressed <<= codes[c][1]
        compressed += codes[c][0]
        i += codes[c][1]
        if i >= 8:
            # Add the first 8 bits to the list of bytes
            b.append(compressed >> (i - 8))
            i -= 8
            # Remove the first 8 bits from the compressed bits
            compressed &= (1 << i) - 1
    # Add any remaining bits to the list of bytes
    if i > 0:
        b.append(compressed << (8 - i))
    # Concatenate the list of bytes into a byte string and return it
    return bytes(b)


# Decompress a byte string using the Huffman binary tree.
def _decompress_data(compressed: bytes, root: Node):
    current = root
    chars = []
    # Decode each byte using the Huffman binary tree and add the decoded character to the output
    for b in compressed:
        for j in range(7, -1, -1):
            if current.char is not None:
                chars.append(current.char)
                current = root
            bit = b & (1 << j)
            if bit:
                current = current.right
            else:
                current = current.left
    # Return the output as a string
    return ''.join(chars)


# Traverse a binary tree in pre-order and create a byte string encoding the tree.
def _pre_order_traversal(node: Node, result: list[str] = None):
    if result is None:
        result = []
    if node is None:
        return
    # If the current node is a leaf, add its character to the list of bytes
    if node.char is not None:
        result.append(node.char)
    else:
        result.append(chr(0))
    # Traverse the left and right subtrees
    _pre_order_traversal(node.left, result)
    _pre_order_traversal(node.right, result)
    # Concatenate the list of bytes into a byte string and return it
    return ''.join(result).encode('ascii', errors='ignore')


# Rebuild a binary tree from the pre-order traversal of the tree recursively.
def _rebuild(flat: deque[int]):
    if len(flat) == 0:
        return None
    # Get the current node byte from the front of the deque
    c = flat.popleft()
    if c == 0:
        # If the current byte is 0, it is an internal node
        left, right = None, None
        # Rebuild the left and right subtrees
        if len(flat) > 0:
            left = _rebuild(flat)
        if len(flat) > 0:
            right = _rebuild(flat)
        return Node(0, None, left, right)
    else:
        # If the current byte is not 0, it is a leaf node
        return Node(0, chr(c), None, None)


# Rebuild a binary tree from a byte string encoding the pre-order traversal of the tree.
def _rebuild_tree(traversal: bytes):
    flat = deque(traversal)
    return _rebuild(flat)


# Write the compressed text and Huffman tree to a binary file.
def _write_compressed(filename: Pathlike, traversal: bytes, compressed: bytes):
    with open(filename, 'wb') as f:
        # Write the length of the Huffman tree and compressed text as big-endian integers
        f.write(len(traversal).to_bytes(2, 'big'))
        f.write(len(compressed).to_bytes(4, 'big'))
        # Write the Huffman tree and compressed text as byte strings
        f.write(traversal)
        f.write(compressed)


# Read the compressed text and Huffman tree from a binary file.
def _read_compressed(filename: Pathlike):
    with open(filename, 'rb') as f:
        # Read the length of the Huffman tree and compressed text as big-endian integers
        traversal_length = int.from_bytes(f.read(2), 'big')
        compressed_length = int.from_bytes(f.read(4), 'big')
        # Read the Huffman tree and compressed text as byte strings
        traversal = f.read(traversal_length)
        compressed = f.read(compressed_length)
    return traversal, compressed


def compress(filename_in: Pathlike, filename_out: Pathlike):
    """
    Compresses the text in a file using Huffman coding and
    writes the compressed text and Huffman tree to a binary file.

    Args:
        filename_in (str): The name of the input file to compress.
        filename_out (str): The name of the output file to write the compressed text
        and Huffman tree.

    """
    # Count the frequency of each character in the input file
    freq = _count_chars(filename_in)
    # Build a Huffman encoding binary tree from the character frequencies
    tree = _build_huffman_tree(freq)
    # Traverse the tree and create a dictionary of characters and their codes
    codes = _traverse_tree(tree)
    # Create a byte string encoding the Huffman tree
    traversal = _pre_order_traversal(tree)
    # Read the text from the input file and remove non-ascii characters
    with open(filename_in, 'r') as f:
        text = f.read().encode('utf-8').decode('ascii', errors='ignore')
    # Compress the text using the Huffman codes
    compressed = _compress_text(text, codes)
    # Write the compressed text and Huffman tree to a binary file
    _write_compressed(filename_out, traversal, compressed)


def decompress(filename_in: Pathlike, filename_out: Pathlike):
    """
    Decompresses the text in a file that has been compressed using Huffman coding
    and writes the decompressed text to a file.

    Args:
        filename_in (str): The name of the input file to decompress.
        filename_out (str): The name of the output file to write the decompressed text.

    """
    # Read the Huffman tree and compressed text from a binary file
    traversal, compressed = _read_compressed(filename_in)
    # Rebuild the Huffman tree from the byte string encoding
    tree = _rebuild_tree(traversal)
    # Decompress the compressed text using the Huffman tree
    text = _decompress_data(compressed, tree)
    # Write the decompressed text to the output file
    with open(filename_out, 'w') as f:
        f.write(text)
