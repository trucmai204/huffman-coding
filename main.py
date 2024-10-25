import heapq
import tkinter as tk
from tkinter import ttk

# Class để xử lý Huffman Coding
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Hàm xây dựng cây Huffman
def build_huffman_tree(freq):
    heap = [HuffmanNode(char, freq[char]) for char in freq]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

# Hàm tạo mã Huffman từ cây
def create_huffman_code(root):
    huffman_code = {}

    def generate_code(node, current_code):
        if node is None:
            return
        if node.char is not None:
            huffman_code[node.char] = current_code
        generate_code(node.left, current_code + "0")
        generate_code(node.right, current_code + "1")

    generate_code(root, "")
    return huffman_code

# Hàm mã hóa dữ liệu
def huffman_encoding(text):
    freq = {}
    for char in text:
        if char not in freq:
            freq[char] = 0
        freq[char] += 1

    root = build_huffman_tree(freq)
    huffman_code = create_huffman_code(root)

    encoded_text = "".join([huffman_code[char] for char in text])
    return encoded_text, huffman_code, root

# Hàm giải mã dữ liệu
def huffman_decoding(encoded_text, root):
    decoded_text = []
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root

    return ''.join(decoded_text)

# Hàm xử lý khi nhấn nút mã hóa
def encode_data():
    input_text = input_text_box.get()
    if input_text:
        encoded_text, huffman_code, root = huffman_encoding(input_text)
        output_text_box.delete(0, tk.END)
        output_text_box.insert(0, encoded_text)
        window.huffman_root = root  # Lưu lại cây Huffman để giải mã sau

# Hàm xử lý khi nhấn nút giải mã
def decode_data():
    encoded_text = output_text_box.get()
    if encoded_text and hasattr(window, 'huffman_root'):
        decoded_text = huffman_decoding(encoded_text, window.huffman_root)
        decoded_output_box.delete(0, tk.END)  # Xóa nội dung ô hiển thị trước đó
        decoded_output_box.insert(0, decoded_text)  # Hiển thị kết quả giải mã

# Giao diện người dùng
window = tk.Tk()
window.title("Huffman Coding")
window.geometry("600x300")  # Tăng kích thước cửa sổ để chứa các thành phần

# Label "NHÓM 12" (căn giữa)
group_label = ttk.Label(window, text="NHÓM 12", font=('Arial', 25, 'bold'), foreground='blue', anchor="center")
group_label.grid(row=0, column=0, columnspan=3, pady=20)

# Ô EditText đầu vào (căn giữa)
input_text_box = ttk.Entry(window, width=40)
input_text_box.grid(row=1, column=1, padx=10, pady=20)

# Ô EditText hiển thị dữ liệu đã mã hóa (căn giữa)
output_text_box = ttk.Entry(window, width=40)
output_text_box.grid(row=1, column=2, padx=10, pady=20)

# Nút mã hóa (căn giữa)
encode_button = tk.Button(window, text="encode", command=encode_data, font=("Arial", 14, "bold"),
                          fg="blue",
                          width=8,
                          height=1,
                          relief="raised",
                          borderwidth=2)
encode_button.grid(row=2, column=1, padx=10, pady=10)

# Nút giải mã (căn giữa)
decode_button = tk.Button(window, text="decode", command=decode_data, font=("Arial", 14, "bold"),
                          fg="blue",
                          width=8,
                          height=1,
                          relief="raised",
                          borderwidth=2)
decode_button.grid(row=2, column=2, padx=10, pady=10)

# Ô EditText hiển thị dữ liệu đã giải mã (căn giữa)
decoded_output_box = ttk.Entry(window, width=40)
decoded_output_box.grid(row=3, column=2, padx=10, pady=20)  # Chiếm 2 cột để căn giữa

# Điều chỉnh lưới để căn giữa tất cả các thành phần
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Chạy ứng dụng
window.mainloop()
