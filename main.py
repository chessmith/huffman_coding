from huffman import compress, decompress


if __name__ == '__main__':
    # Compress the input file and write the compressed text and Huffman tree to a binary file
    compress('tale_of_two_cities.txt', 'tale_of_two_cities.huff')
    # Read the compressed text and Huffman tree from the binary file, decompress the text,
    # and write it to an output file
    decompress('tale_of_two_cities.huff', 'tale_of_two_cities_decompressed.txt')

