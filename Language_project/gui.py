import sys
import os
from .lexer import Lexer  # Updated to relative import
from .language_parser import MyRecursiveDescentParser  # Assuming this also needs updating

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

class LanguageParserGUI:
    def __init__(self, master):
        self.master = master
        master.title("Language Parser")
        self.init_widgets()

    def init_widgets(self):
        """ Initialize the GUI widgets. """
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(padx=10, pady=10)
        parse_button = tk.Button(self.master, text="Parse Code", command=self.run_parser)
        parse_button.pack(side=tk.BOTTOM, pady=10)

    def run_parser(self):
        """ Extract text from text_area, tokenize and parse it, show results in messagebox. """
        code = self.text_area.get('1.0', tk.END)
        lexer = Lexer(code)
        try:
            tokens = lexer.tokenize()
            parser = MyRecursiveDescentParser(tokens)  # Use the updated class name
            parser.parse()
            messagebox.showinfo("Success", "Parsing completed successfully. No errors found.")
        except Exception as e:
            messagebox.showerror("Parsing Error", str(e))

def main():
    root = tk.Tk()
    gui = LanguageParserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
