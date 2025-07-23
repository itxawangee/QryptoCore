from random import randint
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import webbrowser
import base64
from ciphers import CipherImplementations

class QryptoCore:
    def __init__(self, root):
        self.root = root
        self.root.title("QryptoCore")
        self.root.geometry("1100x800")
        self.root.minsize(1000, 700)
        
        # Initialize text widgets as None first
        self.input_text = None
        self.decrypt_text = None
        self.history_listbox = None
        
        # Create assets directory if it doesn't exist
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        os.makedirs(self.assets_path, exist_ok=True)
        
        # App variables
        self.theme = tk.StringVar(value="dark")
        self.font_size = tk.IntVar(value=11)
        self.cipher_history = []
        self.settings_file = os.path.join(self.assets_path, "settings.json")
        
        # Cipher implementations
        self.ciphers = CipherImplementations()
        
        # Initialize UI
        self.create_fallback_icons()
        self.setup_fonts()
        self.load_settings()
        self.setup_menu()
        self.setup_main_ui()
        
        # Show splash screen
        self.show_splash()
    
    def create_fallback_icons(self):
        """Create simple fallback icons if real images aren't found"""
        # App icon
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 31, 31), fill='#00b4ff', outline='white')
        draw.text((8, 6), "Q", fill='white')
        self.app_icon = ImageTk.PhotoImage(img)
        
        # Tab icons
        def create_icon(text, color):
            img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 0, 15, 15), fill=color)
            draw.text((4, 2), text, fill='white')
            return ImageTk.PhotoImage(img)
        
        self.encrypt_icon = create_icon("E", "#4CAF50")
        self.decrypt_icon = create_icon("D", "#F44336")
        self.settings_icon = create_icon("S", "#2196F3")
        self.history_icon = create_icon("H", "#9C27B0")
    
    def setup_fonts(self):
        self.title_font = ("Segoe UI", 18, "bold")
        self.subtitle_font = ("Segoe UI", 10)
        self.mono_font = ("Consolas", self.font_size.get())
        self.button_font = ("Segoe UI", 10, "bold")
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                self.theme.set(settings.get("theme", "dark"))
                self.font_size.set(settings.get("font_size", 11))
            except:
                pass
    
    def save_settings(self):
        settings = {
            "theme": self.theme.get(),
            "font_size": self.font_size.get()
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.browse_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save As...", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_radiobutton(label="Dark Theme", variable=self.theme, value="dark", command=self.change_theme)
        view_menu.add_radiobutton(label="Light Theme", variable=self.theme, value="light", command=self.change_theme)
        view_menu.add_radiobutton(label="Tech Theme", variable=self.theme, value="tech", command=self.change_theme)
        view_menu.add_separator()
        view_menu.add_command(label="Increase Font Size", command=self.increase_font)
        view_menu.add_command(label="Decrease Font Size", command=self.decrease_font)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.open_docs)
        help_menu.add_command(label="User Manual", command=self.open_user_manual)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def configure_styles(self):
        style = ttk.Style()
        
        if self.theme.get() == "dark":
            # Tech Dark Theme (Electric Blue + Deep Gray)
            self.colors = {
                "bg": "#121212",
                "fg": "#e0e0e0",
                "accent": "#00b4ff",
                "secondary": "#1e1e1e",
                "text_bg": "#1e1e1e",
                "text_fg": "#ffffff",
                "entry_bg": "#2d2d2d",
                "entry_fg": "#ffffff",
                "button_bg": "#00b4ff",
                "button_fg": "#ffffff",
                "tab_bg": "#1e1e1e",
                "tab_fg": "#e0e0e0",
                "select_bg": "#00b4ff",
                "select_fg": "#ffffff",
                "success": "#4CAF50",
                "error": "#F44336",
                "warning": "#FFC107"
            }
        elif self.theme.get() == "tech":
            # High-Tech Theme (Neon Green + Dark Gray)
            self.colors = {
                "bg": "#0a0a0a",
                "fg": "#00ff9d",
                "accent": "#00ff9d",
                "secondary": "#1a1a1a",
                "text_bg": "#1a1a1a",
                "text_fg": "#00ff9d",
                "entry_bg": "#252525",
                "entry_fg": "#00ff9d",
                "button_bg": "#006644",
                "button_fg": "#00ff9d",
                "tab_bg": "#1a1a1a",
                "tab_fg": "#00ff9d",
                "select_bg": "#006644",
                "select_fg": "#00ff9d",
                "success": "#00ff9d",
                "error": "#ff0033",
                "warning": "#ffcc00"
            }
        else:  # light
            # Light Tech Theme (Electric Blue + Light Gray)
            self.colors = {
                "bg": "#f5f5f5",
                "fg": "#333333",
                "accent": "#0078d7",
                "secondary": "#ffffff",
                "text_bg": "#ffffff",
                "text_fg": "#333333",
                "entry_bg": "#ffffff",
                "entry_fg": "#333333",
                "button_bg": "#0078d7",
                "button_fg": "#ffffff",
                "tab_bg": "#ffffff",
                "tab_fg": "#333333",
                "select_bg": "#0078d7",
                "select_fg": "#ffffff",
                "success": "#4CAF50",
                "error": "#F44336",
                "warning": "#FFC107"
            }
        
        # Configure styles
        style.theme_create("qrypto", settings={
            ".": {
                "configure": {
                    "background": self.colors["bg"],
                    "foreground": self.colors["fg"],
                    "font": self.mono_font
                }
            },
            "TFrame": {
                "configure": {"background": self.colors["bg"]}
            },
            "TLabel": {
                "configure": {
                    "background": self.colors["bg"],
                    "foreground": self.colors["fg"]
                }
            },
            "TNotebook": {
                "configure": {
                    "background": self.colors["tab_bg"],
                    "tabmargins": [2, 5, 2, 0]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": self.colors["tab_bg"],
                    "foreground": self.colors["tab_fg"],
                    "padding": [10, 5],
                    "font": self.button_font
                },
                "map": {
                    "background": [("selected", self.colors["secondary"])],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            },
            "TEntry": {
                "configure": {
                    "fieldbackground": self.colors["entry_bg"],
                    "foreground": self.colors["entry_fg"],
                    "insertcolor": self.colors["accent"],
                    "padding": 5,
                    "relief": "flat"
                }
            },
            "TCombobox": {
                "configure": {
                    "fieldbackground": self.colors["entry_bg"],
                    "foreground": self.colors["entry_fg"],
                    "selectbackground": self.colors["select_bg"],
                    "selectforeground": self.colors["select_fg"]
                }
            },
            "TButton": {
                "configure": {
                    "background": self.colors["button_bg"],
                    "foreground": self.colors["button_fg"],
                    "font": self.button_font,
                    "padding": 8,
                    "relief": "flat"
                },
                "map": {
                    "background": [("active", self.colors["accent"])],
                    "foreground": [("active", self.colors["button_fg"])]
                }
            },
            "Accent.TButton": {
                "configure": {
                    "background": self.colors["accent"],
                    "foreground": self.colors["button_fg"],
                    "font": self.button_font,
                    "padding": 10
                }
            },
            "Success.TButton": {
                "configure": {
                    "background": self.colors["success"],
                    "foreground": "#ffffff",
                    "font": self.button_font
                }
            },
            "Warning.TButton": {
                "configure": {
                    "background": self.colors["warning"],
                    "foreground": "#000000",
                    "font": self.button_font
                }
            },
            "Error.TButton": {
                "configure": {
                    "background": self.colors["error"],
                    "foreground": "#ffffff",
                    "font": self.button_font
                }
            },
            "TLabelframe": {
                "configure": {
                    "background": self.colors["bg"],
                    "foreground": self.colors["accent"],
                    "relief": "groove",
                    "borderwidth": 1
                }
            },
            "TLabelframe.Label": {
                "configure": {
                    "background": self.colors["bg"],
                    "foreground": self.colors["accent"],
                    "font": self.button_font
                }
            },
            "Horizontal.TProgressbar": {
                "configure": {
                    "background": self.colors["accent"],
                    "troughcolor": self.colors["secondary"],
                    "thickness": 20
                }
            }
        })
        style.theme_use("qrypto")
        
        # Configure root window
        self.root.config(bg=self.colors["bg"])
    
    def setup_main_ui(self):
        self.configure_styles()
        
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with logo and title
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Logo and title
        logo_frame = ttk.Frame(header_frame)
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(logo_frame, image=self.app_icon).pack(side=tk.LEFT)
        ttk.Label(logo_frame, text="QryptoCore", font=self.title_font, 
                 foreground=self.colors["accent"]).pack(side=tk.LEFT, padx=5)
        
        # Tagline
        ttk.Label(header_frame, text="Classical to Quantum—One Tool to Lock Them All", 
                 font=self.subtitle_font).pack(side=tk.LEFT, padx=10, expand=True)
        
        # Theme switcher
        theme_frame = ttk.Frame(header_frame)
        theme_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        self.theme_selector = ttk.Combobox(
            theme_frame, 
            textvariable=self.theme, 
            values=["dark", "light", "tech"],
            state="readonly",
            width=8
        )
        self.theme_selector.pack(side=tk.LEFT, padx=5)
        self.theme_selector.bind("<<ComboboxSelected>>", lambda e: self.change_theme())
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Setup tabs
        self.setup_encryption_tab()
        self.setup_decryption_tab()
        self.setup_settings_tab()
        self.setup_history_tab()
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root, 
            text="Ready", 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=("Segoe UI", 9),
            foreground=self.colors["fg"],
            background=self.colors["secondary"]
        )
        self.status_bar.pack(fill=tk.X)
        
        # Initialize text widget colors after all widgets are created
        self.update_text_widget_colors()
    
    def setup_encryption_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Encrypt", image=self.encrypt_icon, compound=tk.LEFT)
        
        # Input section
        input_frame = ttk.LabelFrame(tab, text="Input Text", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input_text = tk.Text(input_frame, wrap=tk.WORD, font=self.mono_font)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Cipher selection
        cipher_frame = ttk.Frame(tab)
        cipher_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cipher_frame, text="Cipher:").pack(side=tk.LEFT)
        
        self.cipher_var = tk.StringVar()
        cipher_combo = ttk.Combobox(cipher_frame, textvariable=self.cipher_var,
                                   values=["AES", "Caesar", "Vigenère", "OTP", "Atbash", "Rail Fence", "DES3"])
        cipher_combo.pack(side=tk.LEFT, padx=5)
        cipher_combo.current(0)
        
        ttk.Label(cipher_frame, text="Key:").pack(side=tk.LEFT, padx=(10, 0))
        self.key_entry = ttk.Entry(cipher_frame)
        self.key_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Generate Key", command=self.generate_key).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Encrypt", command=self.encrypt, style="Accent.TButton").pack(side=tk.RIGHT, padx=2)
        ttk.Button(button_frame, text="Clear", command=self.clear_input).pack(side=tk.RIGHT, padx=2)
    
    def setup_decryption_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Decrypt", image=self.decrypt_icon, compound=tk.LEFT)
        
        # File selection
        file_frame = ttk.LabelFrame(tab, text="Input", padding=10)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.decrypt_text = tk.Text(file_frame, wrap=tk.WORD, font=self.mono_font)
        self.decrypt_text.pack(fill=tk.BOTH, expand=True)
        
        # Cipher selection
        cipher_frame = ttk.Frame(tab)
        cipher_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cipher_frame, text="Cipher:").pack(side=tk.LEFT)
        
        self.decrypt_cipher_var = tk.StringVar()
        cipher_combo = ttk.Combobox(cipher_frame, textvariable=self.decrypt_cipher_var,
                                   values=["AES", "Caesar", "Vigenère", "OTP", "Atbash", "Rail Fence", "DES3"])
        cipher_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(cipher_frame, text="Key:").pack(side=tk.LEFT, padx=(10, 0))
        self.decrypt_key_entry = ttk.Entry(cipher_frame)
        self.decrypt_key_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Browse File", command=self.browse_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Decrypt", command=self.decrypt, style="Accent.TButton").pack(side=tk.RIGHT, padx=2)
        ttk.Button(button_frame, text="Clear", command=self.clear_decrypt).pack(side=tk.RIGHT, padx=2)
    
    def setup_settings_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Settings", image=self.settings_icon, compound=tk.LEFT)
        
        # Theme settings
        theme_frame = ttk.LabelFrame(tab, text="Appearance", padding=10)
        theme_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(theme_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(theme_frame, text="Dark", variable=self.theme, value="dark",
                       command=self.change_theme).grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(theme_frame, text="Light", variable=self.theme, value="light",
                       command=self.change_theme).grid(row=0, column=2, sticky=tk.W)
        ttk.Radiobutton(theme_frame, text="Tech", variable=self.theme, value="tech",
                       command=self.change_theme).grid(row=0, column=3, sticky=tk.W)
        
        # Font settings
        font_frame = ttk.LabelFrame(tab, text="Font", padding=10)
        font_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(font_frame, text="Font Size:").grid(row=0, column=0, sticky=tk.W)
        ttk.Scale(font_frame, from_=8, to=18, variable=self.font_size,
                 command=lambda e: self.change_font_size()).grid(row=0, column=1, sticky=tk.EW)
        
        # Reset button
        ttk.Button(tab, text="Reset to Defaults", command=self.reset_settings).pack(pady=10)
    
    def setup_history_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="History", image=self.history_icon, compound=tk.LEFT)
        
        # History list
        self.history_listbox = tk.Listbox(tab, font=self.mono_font)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Clear History", command=self.clear_history).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Copy Selected", command=self.copy_history_item).pack(side=tk.RIGHT)
    
    def update_text_widget_colors(self):
        if hasattr(self, 'input_text') and self.input_text:
            self.input_text.config(
                bg=self.colors["text_bg"],
                fg=self.colors["text_fg"],
                insertbackground=self.colors["accent"],
                selectbackground=self.colors["select_bg"],
                selectforeground=self.colors["select_fg"]
            )
        
        if hasattr(self, 'decrypt_text') and self.decrypt_text:
            self.decrypt_text.config(
                bg=self.colors["text_bg"],
                fg=self.colors["text_fg"],
                insertbackground=self.colors["accent"],
                selectbackground=self.colors["select_bg"],
                selectforeground=self.colors["select_fg"]
            )
        
        if hasattr(self, 'history_listbox') and self.history_listbox:
            self.history_listbox.config(
                bg=self.colors["text_bg"],
                fg=self.colors["text_fg"],
                selectbackground=self.colors["select_bg"],
                selectforeground=self.colors["select_fg"]
            )
    
    def show_splash(self):
        splash = tk.Toplevel(self.root)
        splash.geometry("400x300")
        splash.overrideredirect(True)
        
        # Center splash screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (300 // 2)
        splash.geometry(f"+{x}+{y}")
        
        # Splash content
        splash.config(bg="#121212")
        ttk.Label(splash, text="QryptoCore", font=("Segoe UI", 24, "bold"), 
                 foreground="#00b4ff", background="#121212").pack(pady=50)
        ttk.Label(splash, text="Loading...", font=("Segoe UI", 12), 
                 foreground="#e0e0e0", background="#121212").pack()
        
        # Close splash after delay
        self.root.after(1500, splash.destroy)
        self.root.after(1500, self.root.deiconify)
    
    def change_theme(self):
        self.configure_styles()
        self.update_text_widget_colors()
        self.save_settings()
    
    def change_font_size(self):
        self.setup_fonts()
        self.configure_styles()
        self.save_settings()
    
    def increase_font(self):
        if self.font_size.get() < 18:
            self.font_size.set(self.font_size.get() + 1)
            self.change_font_size()
    
    def decrease_font(self):
        if self.font_size.get() > 8:
            self.font_size.set(self.font_size.get() - 1)
            self.change_font_size()
    
    def reset_settings(self):
        self.theme.set("dark")
        self.font_size.set(11)
        self.change_theme()
        self.change_font_size()
        messagebox.showinfo("Settings Reset", "All settings have been reset to defaults.")
    
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                self.decrypt_text.delete("1.0", tk.END)
                self.decrypt_text.insert(tk.END, content)
                self.status_bar.config(text=f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")
    
    def save_file(self):
        content = self.decrypt_text.get("1.0", tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "No content to save.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                self.status_bar.config(text=f"Saved: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def new_file(self):
        self.input_text.delete("1.0", tk.END)
        self.decrypt_text.delete("1.0", tk.END)
        self.key_entry.delete(0, tk.END)
        self.decrypt_key_entry.delete(0, tk.END)
        self.status_bar.config(text="New file created")
    
    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self.key_entry.delete(0, tk.END)
    
    def clear_decrypt(self):
        self.decrypt_text.delete("1.0", tk.END)
        self.decrypt_key_entry.delete(0, tk.END)
    
    def clear_history(self):
        self.history_listbox.delete(0, tk.END)
        self.cipher_history = []
    
    def copy_history_item(self):
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            self.root.clipboard_clear()
            self.root.clipboard_append(item)
            self.status_bar.config(text="Copied to clipboard")
    
    def on_exit(self):
        self.save_settings()
        self.root.quit()
    
    def generate_key(self):
        cipher = self.cipher_var.get()
        if cipher == "AES":
            key = base64.b64encode(os.urandom(32)).decode()
        elif cipher == "DES3":
            key = base64.b64encode(os.urandom(24)).decode()
        elif cipher == "Caesar":
            key = str(randint(1, 25))
        elif cipher in ["Vigenère", "OTP"]:
            key = ''.join(chr(randint(97, 122)) for _ in range(16))
        else:  # Atbash, Rail Fence
            key = ""
        
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, key)
    
    def encrypt(self):
        cipher = self.cipher_var.get()
        plaintext = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        
        if not plaintext:
            messagebox.showwarning("Warning", "Please enter text to encrypt.")
            return
        
        try:
            ciphertext = self.ciphers.encrypt(cipher, plaintext, key)
            
            self.decrypt_text.delete("1.0", tk.END)
            self.decrypt_text.insert(tk.END, ciphertext)
            
            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cipher_history.append(f"[{timestamp}] Encrypted with {cipher}")
            self.history_listbox.insert(tk.END, self.cipher_history[-1])
            
            self.status_bar.config(text=f"Encrypted with {cipher}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")
    
    def decrypt(self):
        cipher = self.decrypt_cipher_var.get()
        ciphertext = self.decrypt_text.get("1.0", tk.END).strip()
        key = self.decrypt_key_entry.get().strip()
        
        if not ciphertext:
            messagebox.showwarning("Warning", "Please enter text to decrypt.")
            return
        
        try:
            plaintext = self.ciphers.decrypt(cipher, ciphertext, key)
            
            self.decrypt_text.delete("1.0", tk.END)
            self.decrypt_text.insert(tk.END, plaintext)
            
            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cipher_history.append(f"[{timestamp}] Decrypted with {cipher}")
            self.history_listbox.insert(tk.END, self.cipher_history[-1])
            
            self.status_bar.config(text=f"Decrypted with {cipher}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")
    
    def show_about(self):
        about_text = """QryptoCore - Encryption/Decryption Tool
Version 1.1.5

A comprehensive tool for classical encryption algorithms.
Supports AES, Caesar, Vigenère, OTP, Atbash, Rail Fence, and DES3.

© 2025 QryptoCore Team"""
        messagebox.showinfo("About QryptoCore", about_text)

    def open_user_manual(self):
        webbrowser.open("user_manual.html")

    def open_docs(self):
        webbrowser.open("documentation.html")