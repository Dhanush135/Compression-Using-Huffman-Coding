# Compression-Using-Huffman-Coding

This project is an implementation of Huffman coding, a popular algorithm used for data compression. Huffman coding is a lossless compression technique that assigns variable-length codes to different characters in a given input text. It achieves compression by assigning shorter codes to more frequently occurring characters and longer codes to less frequently occurring characters.

## Features

- Compression: The project provides functionality to compress a given input text file using Huffman coding. It analyzes the input text to determine the frequency of each character and constructs a Huffman tree based on the frequencies. It then generates the compressed binary representation of the input text using the Huffman codes derived from the tree.

- Decompression: The project also supports decompressing a previously compressed text using the Huffman codes generated during compression. It decodes the binary data to retrieve the original text.

- File Compression: In addition to compressing and decompressing text input, the project allows compression and decompression of files. It provides methods to read the content of a file, perform compression, and save the compressed data to a new file. Similarly, it can read a compressed file, decompress the data, and save the decompressed content to a new file.

- Efficiency: The implementation focuses on efficiency and aims to achieve high compression ratios. It uses a priority queue and a binary heap to efficiently construct the Huffman tree and perform the compression and decompression operations. The project also includes optimizations, such as bit-level operations, to minimize the memory footprint and improve the overall performance.

## Requirements

- Python 3.x
- tkinter
- PIL (Python Imaging Library)

## Usage

1. Clone the repository:

```shell
git clone https://github.com/Dhanush135/Compression-Using-Huffman-Coding.git
```
2. Navigate to the project directory:

```shell
cd huffman-coding
```

3. Run the Huffman_Compression.py file:

```shell
python Huffman_Compression.py 
```
4. Compressing a Text File:

   - Click on the "Compress" button.

   - Select the text file you want to compress using the file dialog.

   - The compressed file will be saved with the same name as the original file with suffix "_compressed", but with the extension ".bin".

5. Decompressing a Compressed File:

   - Click on the "Decompress" button.

   - Select the compressed file you want to decompress using the file dialog.

   - The decompressed text file will be saved with the suffix "_decompressed" added to the original file name, and the extension ".txt".
   
6. Compressing an Image File:

   - Click on the "Compress" button for image compression.
   
   - Select the image file you want to compress using the file dialog.
    
   - The compressed image file will be saved with the name "compressed_image.jpg".

