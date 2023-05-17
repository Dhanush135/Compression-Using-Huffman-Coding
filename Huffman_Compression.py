from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image
import gzip

import heapq
import os


class HuffmanNode:
    def __init__(self, value, frequency, left=None, right=None):
        self.value = value
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency
    
    def __eq__(self, other):
        return self.frequency == other.frequency

def build_huffman_tree(freq_dict):
    priority_queue = []
    for value, frequency in freq_dict.items():
        node = HuffmanNode(value, frequency)
        priority_queue.append((frequency, node))
    priority_queue.sort()
    
    while len(priority_queue) > 1:
        f1, n1 = priority_queue.pop(0)
        f2, n2 = priority_queue.pop(0)
        new_node = HuffmanNode(None, f1 + f2, left=n1, right=n2)
        priority_queue.append((f1 + f2, new_node))
        priority_queue.sort()
        
    root = priority_queue[0][1]
    return root

def get_code_map(root):
    code_map = {}
    def traverse(node, code):
        if node.value is not None:
            code_map[node.value] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    traverse(root, "")
    return code_map

def visualize_huffman_tree(freq_dict):
    root = build_huffman_tree(freq_dict)
    code_map = get_code_map(root)
    
    master = tk.Tk()
    master.title("Huffman Coding Tree Visualization")
    
    canvas_width = 1500
    canvas_height = 1000
    canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
    canvas.pack()
    
    node_radius = 25
    node_vertical_spacing = 75
    node_horizontal_spacing = 100
    
    def draw_node(node, x, y):
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, width=2)
        canvas.create_text(x, y, text=node.frequency)
        if node.value is not None:
            canvas.create_text(x, y + node_radius + 10, text=node.value)
    
    def draw_tree(node, x, y):
        if node is not None:
            draw_node(node, x, y)
            if node.left is not None:
                canvas.create_line(x - node_horizontal_spacing, y + node_vertical_spacing, x, y)
                draw_tree(node.left, x - node_horizontal_spacing, y + node_vertical_spacing)
            if node.right is not None:
                canvas.create_line(x + node_horizontal_spacing, y + node_vertical_spacing, x, y)
                draw_tree(node.right, x + node_horizontal_spacing, y + node_vertical_spacing)
                
    draw_tree(root, canvas_width // 2, node_vertical_spacing)
    
    for value, code in code_map.items():
        canvas.create_text(canvas_width // 2, canvas_height - 50, text=f"{value}: {code}")
    
    tk.mainloop()



class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			# if(not isinstance(other, HeapNode)):
			# 	return False
			return self.freq == other.freq

	# functions for compression:

	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"

		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			frequency = self.make_frequency_dict(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(text)
			padded_encoded_text = self.pad_encoded_text(encoded_text)

			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))
		
		input_size = os.path.getsize(self.path)
		output_size = os.path.getsize(output_path)
		ratio = "The compression ratio is " + str(output_size/input_size) + "\n"
		result_text1.insert(tk.END,f"{ratio}\n")
		print(output_size/input_size)

		print("Compressed")
		# visualize_huffman_tree(frequency)
		return output_path




	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)
			result_text.insert(tk.END,f"{decompressed_text}\n\n")
			print(decompressed_text)
			output.write(decompressed_text)

		print("Decompressed")
		return output_path
	

	def print_codes(self):
		S = ""
		for key in self.codes:
			print(f"{key}:{self.codes[key]}")
		# S = str(self.codes)
		res = ' '.join(sorted(self.codes, key=lambda key: len(self.codes[key])))
		count=0
		for i in res:
			if count%2==0:
				result_text1.insert(tk.END,f"{i}:{self.codes[i]}\n")
				count+=1
			else:
				count+=1



def solve():	
	source_path = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Text Files", ".txt"), ("All Files", ".*")))
	h = HuffmanCoding(source_path)
	h.compress()
	h.print_codes()
	# visualize_huffman_tree(h.codes)


def solve1():	
	source_path1 = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Bin Files", ".bin"), ("All Files", ".*")))
	path=source_path1[:-3]
	path=path+"txt"
	h = HuffmanCoding(path)
	h.compress()
	h.decompress(source_path1)


def compress_image():
    source_path2 = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Text Files", ".png"), ("All Files", ".*")))
    # Load the image
    image = Image.open(source_path2)

    # Set the compression level (0-100)
    quality = 50

    # Save the compressed image
    image.save('compressed_image.jpg', optimize=True, quality=quality)     



root=Tk()

root.geometry("1500x1000")

l1=Label(root,text="Enter the path of the file")
l1.pack(padx=35)
pathval = StringVar()
pathentry=Entry(root,textvariable=pathval)
pathentry.pack()
b1=Button(root,text="Compress",command=solve)
b1.pack()

l2=Label(root,text="Enter the path of the file")
l2.pack(padx=35)
path1val = StringVar()
path1entry=Entry(root,textvariable=path1val)
path1entry.pack()
b2=Button(root,text="Decompress",command=solve1)
b2.pack()

l3 = Label(root,text="Enter the image name")
l3.pack(padx=35)
path2val = StringVar()
path2entry = Entry(root,textvariable=path2val)
path2entry.pack()
b3=Button(root,text="Compress",command=compress_image)
b3.pack()


result_frame = tk.Frame(root)
result_frame.pack(side=tk.TOP)
result_text = tk.Text(result_frame, height=40, width=100)
result_text.pack(side=tk.LEFT, fill=tk.Y)
scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
result_text.configure(yscrollcommand=scrollbar.set)

result_frame1 = tk.Frame()
result_frame1.pack(side=tk.BOTTOM)
result_text1 = tk.Text(result_frame, height=400, width=100)
result_text1.pack(side=tk.LEFT, fill=tk.Y)
scrollbar1 = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text1.yview)
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
result_text1.configure(yscrollcommand=scrollbar.set)

root.mainloop()



# solve("/Users/selvarajandhanush/Documents/Mini_Project/sample_decompressed.txt")