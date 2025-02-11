import hashlib
import tkinter as tk
from tkinter import messagebox
 # Chunk Linked List Implementation
class ChunkNode:
    def __init__(self, data):
        self.data = data
        self.next_node = None
        self.next_checksum = None
    def calculate_checksum(self):
        return hashlib.sha256(self.data).hexdigest() if self.data else None
def split_file_into_chunks(file_data, chunk_size=5):
    return [file_data[i:i + chunk_size] for i in range(0, len(file_data), 
chunk_size)]
def create_linked_chunks(chunks):
    if not chunks:
        return None
    head = ChunkNode(chunks[0])
    current = head
    for i in range(1, len(chunks)):
        new_node = ChunkNode(chunks[i])
        current.next_node = new_node
        current.next_checksum = new_node.calculate_checksum()
        current = new_node
    return head
def reconstruct_file(head):
    file_data = b""
    current = head
    while current:
        file_data += current.data
        current = current.next_node
    return file_data
def validate_linked_chunks(head):
    current = head
    while current and current.next_node:
        if current.next_checksum != current.next_node.calculate_checksum():
            return False
        current = current.next_node
    return True
 # Tkinter UI Implementation
class ChunkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chunk Linked List UI")
        # Input field
        self.file_data_entry = tk.Entry(root, width=50)
        self.file_data_entry.pack(pady=5)
        # Buttons
        tk.Button(root, text="Split & Create Chunks", 
command=self.split_and_create).pack(pady=5)
        tk.Button(root, text="Display Chunks", 
command=self.display_chunks).pack(pady=5)
        tk.Button(root, text="Reconstruct File", 
command=self.reconstruct).pack(pady=5)
        tk.Button(root, text="Validate Integrity", 
command=self.validate).pack(pady=5)
        tk.Button(root, text="Simulate Tampering", 
command=self.tamper_data).pack(pady=5)
        # Output label
        self.output_label = tk.Label(root, text="")
        self.output_label.pack(pady=10)
        self.head = None
        self.chunks = []
    def split_and_create(self):
        file_data = self.file_data_entry.get().encode()
        self.chunks = split_file_into_chunks(file_data)
        self.head = create_linked_chunks(self.chunks)
        self.output_label.config(text="Chunks Created Successfully")
    def display_chunks(self):
        if self.chunks:
            chunks_display = '\n'.join([chunk.decode(errors='ignore') for chunk 
in self.chunks])
            self.output_label.config(text=f"Chunks:\n{chunks_display}")
        else:
            messagebox.showerror("Error", "No chunks to display")
    def reconstruct(self):
        if self.head:
            reconstructed_data = reconstruct_file(self.head)
            self.output_label.config(text=f"Reconstructed; {reconstructed_data.decode()}")
        else:
            messagebox.showerror("Error", "No data to reconstruct")
    def validate(self):
        if self.head:
            is_valid = validate_linked_chunks(self.head)
            self.output_label.config(text=f"Integrity Valid: {is_valid}")
        else:
            messagebox.showerror("Error", "No data to validate")
    def tamper_data(self):
        if self.head and self.head.next_node:
            self.head.next_node.data = b"Tampered"  # Simulate tampering
            self.output_label.config(text="Data Tampered for Testing")
        else:
            messagebox.showerror("Error", "Not enough data to tamper")
 # Run Application
root = tk.Tk()
app = ChunkApp(root)
root.mainloop() 