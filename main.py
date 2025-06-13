# main.py (Integrated Version)
import sys
sys.dont_write_bytecode = True
import tkinter as tk
from tkinter import ttk, messagebox
from gui import SteganographyApp

# Hardcoded passcode
PASSCODE = "goku"

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Secure Login")
        master.configure(bg="#2C3E50")
        master.resizable(False, False)
        
        # Center window
        self._center_window(300, 150)
        
        # Create UI
        self._create_widgets()

    def _center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("TLabel", background="#2C3E50", foreground="#ECF0F1")
        style.configure("TButton", font=('Arial', 10))

        ttk.Label(main_frame, text="Enter Passcode:", font=('Arial', 12)).grid(row=0, column=0, pady=5)
        self.pass_entry = ttk.Entry(main_frame, show="•", font=('Arial', 12), width=20)
        self.pass_entry.grid(row=1, column=0, pady=5)
        self.pass_entry.bind("<Return>", lambda e: self._check_password())

        ttk.Button(main_frame, text="Unlock", command=self._check_password).grid(row=2, column=0, pady=10)

    def _check_password(self):
        if self.pass_entry.get() == PASSCODE:
            self.master.destroy()
            self._launch_main_app()
        else:
            messagebox.showerror("Access Denied", "Incorrect passcode!")
            self.pass_entry.delete(0, tk.END)

    def _launch_main_app(self):
        root = tk.Tk()
        app = SteganographyApp(root)
        root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
