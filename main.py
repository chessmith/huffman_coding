import timeit
from huffman import compress, decompress


if __name__ == '__main__':
    # time the compression and decompression and print the results
    # Compress the input file and write the compressed text and Huffman tree to a binary file
    t = timeit.timeit('compress("tale_of_two_cities.txt", "tale_of_two_cities.huff")',
                      globals={'compress': compress}, number=10)
    print('Compression time:', t)
    # Read the compressed text and Huffman tree from the binary file, decompress the text,
    # and write it to an output file
    t = timeit.timeit('decompress("tale_of_two_cities.huff", "tale_of_two_cities_decompressed.txt")',
                      globals={'decompress': decompress}, number=10)
    print('Decompression time:', t)