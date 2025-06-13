import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk, Image
import os

from encode_lsb import encode_lsb
from decode_lsb import decode_lsb
from aes import encrypt, decrypt
from hmac_handler import generate_hmac, verify_hmac
from utils import can_message_fit


class SteganographyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("LSB Image Steganography")

        # Maximize the main window
        self.master.state('zoomed')

        # Configure grid layout for the main window
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Main Frame
        self.main_frame = tk.Frame(self.master, bg="#E6F8E0", padx=20, pady=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid layout for the main frame
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=0)  # Row for image
        self.main_frame.grid_rowconfigure(4, weight=1)  # Allow extra content to expand
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="LSB Image Steganography", font=("Arial", 24, "bold"), bg="#E6F8E0", fg="#3B5998")
        self.title_label.grid(row=0, column=0, pady=20)

        # Buttons for Encode and Decode with custom styles
        button_style = {
            'bg': '#58D68D',
            'fg': 'white',
            'font': ('Helvetica', 16, 'bold'),
            'activebackground': '#2ECC71',
            'relief': tk.RAISED,
            'borderwidth': 5
        }

        self.encode_button = tk.Button(self.main_frame, text="Encode Message", command=self.open_encode_window, **button_style)
        self.encode_button.grid(row=1, column=0, pady=15)

        self.decode_button = tk.Button(self.main_frame, text="Decode Message", command=self.open_decode_window, **button_style)
        self.decode_button.grid(row=2, column=0, pady=15)

        # Load and display the image (placed above explanation content)
        self.display_image("James_Bond.jpg")

        # Fun Explanation Content
        explanation_text = (
            "Welcome to the Secret Agent Academy!\n"
            "Your mission: Master the art of steganography!\n"
            "\n"
            "Steganography: Hiding messages in plain sight. Think invisible ink, but with images!\n"
            "LSB (Least Significant Bit): The sneakiest bit! We change it to hide your message.\n"
            "AES (Advanced Encryption Standard): Scrambles your message with a secret key.\n"
            "HMAC (Hashed Message Authentication Code): A secret code that makes sure no one messes with your message!"
        )

        self.explanation_label = tk.Label(
            self.main_frame,
            text=explanation_text,
            bg="#E6F8E0",
            font=("Comic Sans MS", 15),
            wraplength=2000,
            justify=tk.CENTER 
        )
        self.explanation_label.grid(row=4, column=0, pady=0, sticky="nsew")  # Set pady to 0

    def display_image(self, image_path):
        """Load and display an image."""
        try:
            # Open the image file
            img = Image.open(image_path)
            img = img.resize((400, 400), Image.LANCZOS)  # Resize if needed
            photo = ImageTk.PhotoImage(img)

            # Create a label to display the image
            image_label = tk.Label(self.main_frame, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.grid(row=3, column=0, pady=0)  # Set pady to 0

        except Exception as e:
            print(f"Error loading image: {e}")

    def open_encode_window(self):
        EncodeWindow(self.master)

    def open_decode_window(self):
        DecodeWindow(self.master)

class EncodeWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Encode Message")

        # Maximize the encode window
        self.window.state('zoomed')

        # Main Frame
        self.main_frame = tk.Frame(self.window, bg="#F0E68C", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Scrollable Canvas
        self.canvas = tk.Canvas(self.main_frame, bg="#F0E68C", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F0E68C")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Configure grid layout for the scrollable frame
        for i in range(15):  # Configure 15 rows
            self.scrollable_frame.grid_rowconfigure(i, weight=0)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Image Selection
        self.image_path = ""
        self.image = None  # Store the loaded image

        self.image_label = tk.Label(self.scrollable_frame, text="Select an image:", bg="#F0E68C", font=("Times", 14), fg="#654321", anchor="center")  
        self.image_label.grid(row=0, column=0, pady=10, sticky="ew")

        button_style = {
            'bg': '#CD853F',  
            'fg': 'white',
            'font': ('Helvetica', 12, 'bold'),
            'activebackground': '#A0522D',  
            'relief': tk.RAISED,
            'borderwidth': 3
        }

        self.select_image_button = tk.Button(self.scrollable_frame, text="Browse", command=self.load_image, **button_style)
        self.select_image_button.grid(row=1, column=0, pady=5, sticky="ew")

        # Display Image
        self.image_display = tk.Label(self.scrollable_frame)
        self.image_display.grid(row=2, column=0, pady=10)

        # Properties and Message Input
        self.properties_label = tk.Label(self.scrollable_frame, text="", bg="#F0E68C", font=("Arial", 12), fg="#654321", anchor="center")
        self.properties_label.grid(row=3, column=0, pady=10, sticky="ew")

        self.method_label = tk.Label(self.scrollable_frame, text="Select Encoding Method:", bg="#F0E68C", font=("Times", 14), fg="#654321", anchor="center") 
        self.method_label.grid(row=4, column=0, pady=5, sticky="ew")

        self.encoding_method = ttk.Combobox(self.scrollable_frame ,values=["Normal LSB"], justify='center')
        self.encoding_method.current(0)
        self.encoding_method.grid(row=5, column=0, pady=5 ,sticky="ew")
        
        # HMAC Key Input and Dropdown
        self.hmac_key_label = tk.Label(self.scrollable_frame, text="Select or Enter HMAC Key:", bg="#F0E68C", font=("Times", 14), fg="#654321", anchor="center")
        self.hmac_key_label.grid(row=6, column=0, pady=5, sticky="ew")

        self.hmac_key_options = ["", "DemoHMACKey-1-ForTestingPurposes", "DemoHMACKey-2-ForTestingPurposes"]  # Demo HMAC keys
        self.hmac_key_var = tk.StringVar()
        self.hmac_key_dropdown = ttk.Combobox(self.scrollable_frame, textvariable=self.hmac_key_var, values=self.hmac_key_options, justify='center')
        self.hmac_key_dropdown.grid(row=7, column=0, pady=5, sticky="ew")

        # AES Key Input and Dropdown
        self.aes_key_label = tk.Label(self.scrollable_frame, text="Select or Enter AES Key (16, 24, or 32 characters):", bg="#F0E68C", font=("Times", 14), fg="#654321", anchor="center")
        self.aes_key_label.grid(row=8, column=0, pady=5, sticky="ew")

        self.aes_key_options = ["", "Sixteen byte key", "TwentyFourByteKey1234567", "ThirtyTwoByteKey1234567890123456"]  # Demo AES keys
        self.aes_key_var = tk.StringVar()
        self.aes_key_dropdown = ttk.Combobox(self.scrollable_frame, textvariable=self.aes_key_var, values=self.aes_key_options, justify='center')
        self.aes_key_dropdown.grid(row=9, column=0, pady=5, sticky="ew")

        # Secret message input
        self.message_label = tk.Label(self.scrollable_frame, text="Enter Message:", bg="#F0E68C", font=("Times", 14), fg="#654321", anchor="center") 
        self.message_label.grid(row=10, column=0, pady=(10, 5), sticky="ew")

        self.message_entry = tk.Text(self.scrollable_frame, height=5, font=("Arial", 12))
        self.message_entry.grid(row=11, column=0, pady=(5, 10), sticky="ew")

        # Dynamic character limit display label
        self.char_limit_label = tk.Label(self.scrollable_frame, text="", bg="#F0E68C", font=("Arial", 12), fg="#FF5733")
        self.char_limit_label.grid(row=12, column=0, pady=(5, 10), sticky="ew")

        # Update character limit when message is typed
        self.message_entry.bind("<KeyRelease>", lambda event: self.update_char_limit())

        # Ciphertext display field
        self.ciphertext_label = tk.Label(self.scrollable_frame, text="Ciphertext:", bg="#F0E68C", font=("Times", 14), fg="#654321", anchor="center") 
        self.ciphertext_label.grid(row=13, column=0, pady=(10, 5), sticky="ew")

        self.ciphertext_display = tk.Text(self.scrollable_frame, height=3, font=("Arial", 12))
        self.ciphertext_display.grid(row=14, column=0, pady=(5, 20), sticky="ew")

        # Save Button
        self.save_button = tk.Button(self.scrollable_frame, text="Save Encoded Image", command=self.save_encoded_image, **button_style)
        self.save_button.grid(row=15,column=0,pady=20)

    def update_char_limit(self):
        if not self.image:
            self.char_limit_label.config(text="Select an image to see character limits.")
            return

        message_text = self.message_entry.get("1.0", "end-1c")
    
        # Calculate theoretical maximum characters that can fit in the image
        theoretical_max_chars = (self.image.size[0] * self.image.size[1] * 3) // 8 - 1

        # Apply a conservative factor to minimize noticeable quality loss (e.g., 25%)
        conservative_factor = 0.25  # Reduce usable capacity to 25% to preserve image quality
        recommended_max_chars = int(theoretical_max_chars * conservative_factor)

        # Calculate remaining characters that can be entered without exceeding the recommended limit
        remaining_text_message = f"Recommended characters: {recommended_max_chars}. "
    
        # Calculate how many characters can still be entered before reaching the limit
        chars_left = recommended_max_chars - len(message_text)
    
        if chars_left < 0:
            chars_left = 0
        
        remaining_text_message += f"You can still enter {chars_left} characters before noticeable quality loss."
    
        if len(message_text) >= recommended_max_chars:
            remaining_text_message += " (Reaching limit!)"

        self.char_limit_label.config(text=f"{remaining_text_message}")


    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])

        if file_path:
            self.image = Image.open(file_path)  # Store the image
            original_width, original_height = self.image.size  # Store original size for properties display
            image = self.image.copy()  # Create a copy for thumbnail
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_display.config(image=photo)
            self.image_display.image = photo  # Keep a reference to avoid garbage collection

            # Display actual image properties
            size = os.path.getsize(file_path) / 1024  # Size in KB
            resolution = f"{original_width} x {original_height}"  # Use original resolution
            num_pixels = original_width * original_height

            properties_text = (
                f"Image Name: {os.path.basename(file_path)}\n"
                f"Path: {file_path}\n"
                f"Size: {size:.2f} KB\n"
                f"Resolution: {resolution}\n"
                f"Number of Pixels: {num_pixels}"
            )
            self.properties_label.config(text=properties_text)
            self.image_path = file_path

            # Update character limit when image is loaded
            self.update_char_limit()

    def save_encoded_image(self):
        message = self.message_entry.get("1.0", "end-1c")
        aes_key = self.aes_key_var.get()
        hmac_key = self.hmac_key_var.get()

        # Check if AES key is provided and valid
        if len(aes_key) not in [16, 24, 32]:
            messagebox.showerror("Error", "AES Key must be 16, 24, or 32 characters long.")
            return

        if not hmac_key:
            messagebox.showerror("Error", "Please provide an HMAC key.")
            return

        if not message or not self.image_path:
            messagebox.showerror("Error", "Please provide a message and select an image.")
            return
        
        # Calculate theoretical maximum characters that can fit in the image
        theoretical_max_chars = (self.image.size[0] * self.image.size[1] * 3) // 8 - 1

        # Apply a conservative factor to minimize noticeable quality loss (e.g., 25%)
        conservative_factor = 0.25  
        recommended_max_chars = int(theoretical_max_chars * conservative_factor) - len(message)

        if recommended_max_chars < 0:
            messagebox.showerror("Error", "The message is too large to fit in the image without noticeable quality loss.")
            return

        # Generate ciphertext here for saving and print to terminal
        ciphertext = encrypt(message, aes_key).decode('utf-8')

        print(f"Key: {aes_key}")  
        print(f"Ciphertext: {ciphertext}")  

        # Generate HMAC of the ciphertext
        hmac_value = generate_hmac(hmac_key, ciphertext)

        # Display ciphertext in the GUI
        self.ciphertext_display.delete("1.0", tk.END)  
        self.ciphertext_display.insert(tk.END, ciphertext)  

        encoded_img = encode_lsb(self.image_path, ciphertext + "\n" + hmac_value + "\n" + aes_key)

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])

        if save_path and encoded_img:
            encoded_img.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully!")
class DecodeWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Decode Message")

        # Maximize the decode window
        self.window.state('zoomed')

        # Main Frame
        self.main_frame = tk.Frame(self.window, bg="#ADD8E6", padx=20, pady=20)  # A soft blue background
        self.main_frame.pack(fill="both", expand=True)

        # Scrollable Canvas
        self.canvas = tk.Canvas(self.main_frame, bg="#ADD8E6", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ADD8E6")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand="True")
        self.scrollbar.pack(side="right", fill="y")

        # Configure grid layout for the scrollable frame
        for i in range(13):  # Configure 13 rows
            self.scrollable_frame.grid_rowconfigure(i, weight=0)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Image Selection for Decoding
        self.encoded_image_path = ""

        self.image_label = tk.Label(self.scrollable_frame, text="Select an encoded image:", bg="#ADD8E6", font=("Times", 14), fg="#000080", anchor="center")  # A navy blue color
        self.image_label.grid(row=0, column=0, pady=10, sticky="ew")

        button_style = {
            'bg': '#4682B4',  # A steelblue color
            'fg': 'white',
            'font': ('Helvetica', 12, 'bold'),
            'activebackground': '#2E86C1',  # A slightly darker blue on hover
            'relief': tk.RAISED,
            'borderwidth': 3
        }

        # Browse Button to load encoded image
        self.select_image_button = tk.Button(self.scrollable_frame, text="Browse", command=self.load_encoded_image, **button_style)
        self.select_image_button.grid(row=1, column=0, pady=5, sticky="ew")

        # Display Image
        self.image_display = tk.Label(self.scrollable_frame)
        self.image_display.grid(row=2, column=0, pady=10)

        # Properties and Decoding Options
        self.properties_label = tk.Label(self.scrollable_frame, text="", bg="#ADD8E6", font=("Arial", 12), fg="#000080", anchor="center")
        self.properties_label.grid(row=3, column=0, pady=10, sticky="ew")

        # Decoding Method Selection
        self.method_label = tk.Label(self.scrollable_frame, text="Select Decoding Method:", bg="#ADD8E6", font=("Times", 14), fg="#000080", anchor="center")
        self.method_label.grid(row=4, column=0, pady=5, sticky="ew")

        self.decoding_method = ttk.Combobox(self.scrollable_frame, values=["Normal LSB"], justify='center')
        self.decoding_method.current(0)
        self.decoding_method.grid(row=5, column=0, pady=5, sticky="ew")

        # HMAC Key Input and Dropdown
        self.hmac_key_label = tk.Label(self.scrollable_frame, text="Select or Enter HMAC Key:", bg="#ADD8E6", font=("Times", 14), fg="#000080", anchor="center")
        self.hmac_key_label.grid(row=6, column=0, pady=5, sticky="ew")

        self.hmac_key_options = ["", "DemoHMACKey-1-ForTestingPurposes", "DemoHMACKey-2-ForTestingPurposes"]  # Demo HMAC keys
        self.hmac_key_var = tk.StringVar()
        self.hmac_key_dropdown = ttk.Combobox(self.scrollable_frame, textvariable=self.hmac_key_var, values=self.hmac_key_options, justify='center')
        self.hmac_key_dropdown.grid(row=7, column=0, pady=5, sticky="ew")

        # AES Key Input and Dropdown
        self.aes_key_label = tk.Label(self.scrollable_frame, text="Select or Enter AES Key (if applicable):", bg="#ADD8E6", font=("Times", 14), fg="#000080", anchor="center")
        self.aes_key_label.grid(row=8, column=0, pady=5, sticky="ew")

        self.aes_key_options = ["", "Sixteen byte key", "TwentyFourByteKey1234567", "ThirtyTwoByteKey1234567890123456"]  # Demo AES keys
        self.aes_key_var = tk.StringVar()
        self.aes_key_dropdown = ttk.Combobox(self.scrollable_frame, textvariable=self.aes_key_var, values=self.aes_key_options, justify='center')
        self.aes_key_dropdown.grid(row=9, column=0, pady=5, sticky="ew")

        # Decode Button
        self.decode_button = tk.Button(self.scrollable_frame, text="Decode Message", command=self.decode_message, **button_style)
        self.decode_button.grid(row=10, column=0, pady=20)

        # Display Decoded Message and Ciphertext
        self.decoded_message_label = tk.Label(self.scrollable_frame, text="Decoded Message:", bg="#ADD8E6", font=("Times", 14), fg="#000080", anchor="center")
        self.decoded_message_label.grid(row=11, column=0, pady=5, sticky="ew")

        self.decoded_message_display = tk.Text(self.scrollable_frame, height=10, font=("Arial", 12))
        self.decoded_message_display.grid(row=12, column=0, pady=5, sticky="nsew")

        # Configure columns to center content 
        for i in range(self.scrollable_frame.grid_size()[0]):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

        # Bind mousewheel scrolling
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_to_mousewheel)

    def _bind_to_mousewheel(self,event):
         self.canvas.bind_all("<MouseWheel>",self._on_mousewheel)

    def _unbind_to_mousewheel(self,event):
         self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self,event):
         self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_encoded_image(self):
         file_path = filedialog.askopenfilename(filetypes=[("Image Files","*.png;*.jpg")])

         if file_path:
             original_image = Image.open(file_path)
             original_width , original_height = original_image.size

             original_image.thumbnail((300 ,300))
             photo = ImageTk.PhotoImage(original_image)
             self.image_display.config(image=photo)
             self.image_display.image = photo

             size = os.path.getsize(file_path) / 1024 
             resolution = f"{original_width} x {original_height}"
             num_pixels = original_width * original_height

             properties_text = (
                 f"Encoded Image Name: {os.path.basename(file_path)}\n"
                 f"Path: {file_path}\n"
                 f"Size: {size:.2f} KB\n"
                 f"Resolution: {resolution}\n"
                 f"Number of Pixels: {num_pixels}"
             )
             self.properties_label.config(text=properties_text)
             self.encoded_image_path = file_path

    def decode_message(self):
         if not self.encoded_image_path:
             messagebox.showerror("Error","Please select an encoded image.")
             return

         aes_key =self.aes_key_var.get()
         hmac_key=self.hmac_key_var.get()

         if len(aes_key) not in [16 ,24 ,32]:
             messagebox.showerror("Error","AES Key must be 16 ,24 ,or 32 characters long.")
             return

         if not hmac_key:
             messagebox.showerror("Error","Please provide an HMAC key.")
             return

         try:
             original_message,hmac_value ,stored_key = decode_lsb(self.encoded_image_path)

             if stored_key.strip() != aes_key:
                 raise ValueError("Decryption failed: The provided AES key does not match the encryption key.")

             if not verify_hmac(hmac_key ,original_message.strip() ,hmac_value.strip()):
                 raise ValueError("HMAC verification failed: The message has been tampered with or the key is incorrect.")

             decrypted_message = decrypt(original_message.strip() ,aes_key)

             full_decoded_message=f"Decrypted Message:\n{decrypted_message}\nCiphertext:\n{original_message.strip()}"

             # Display decoded message in the text area
             self.decoded_message_display.delete("1.0" ,tk.END)
             self.decoded_message_display.insert(tk.END ,full_decoded_message)

         except ValueError as ve:
             messagebox.showerror("Decoding Error" ,str(ve))
         except Exception as e:
             messagebox.showerror("Decoding Error" ,"An error occurred during decryption: " + str(e))
