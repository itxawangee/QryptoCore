import tkinter as tk
from gui import QryptoCore

def main():
    root = tk.Tk()
    root.withdraw()  
    app = QryptoCore(root)
    root.mainloop()

if __name__ == "__main__":
    main()