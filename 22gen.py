import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import logging
import re

# Configure logging
logging.basicConfig(filename='spl_token_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to run solana commands and return the output
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", e.stderr.strip())
        logging.error(e.stderr.strip())
        return None

class SPLTokenGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SPLgen")
        self.geometry("250x250")

        self.token_address = tk.StringVar()
        self.token_account_address = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="SPL Token Address:").pack(pady=5)
        ttk.Entry(self, textvariable=self.token_address).pack(pady=5)
        
        ttk.Button(self, text="Create SPL Token", command=self.create_token).pack(pady=5)
        ttk.Button(self, text="Create Token Account", command=self.create_token_account).pack(pady=5)
        ttk.Button(self, text="Mint Tokens", command=self.mint_tokens).pack(pady=5)

    def create_token(self):
        command = ["spl-token", "create-token"]
        output = run_command(command)
        if output:
            match = re.search(r"Creating token (?P<token>\w+)", output)
            if match:
                token_address = match.group("token")
                self.token_address.set(token_address)
                logging.info(f"Token Created: {token_address}")
                messagebox.showinfo("Success", f"Token Created: {token_address}")
            else:
                messagebox.showerror("Error", "Failed to parse token address.")

    def create_token_account(self):
        if not self.token_address.get():
            messagebox.showerror("Error", "Please create a token first.")
            return
        command = ["spl-token", "create-account", self.token_address.get()]
        output = run_command(command)
        if output:
            match = re.search(r"Creating account (?P<account>\w+)", output)
            if match:
                account_address = match.group("account")
                self.token_account_address.set(account_address)
                logging.info(f"Token Account Created: {account_address}")
                messagebox.showinfo("Success", f"Token Account Created: {account_address}")
            else:
                messagebox.showerror("Error", "Failed to parse token account address.")

    def mint_tokens(self):
        amount = simpledialog.askstring("Mint Tokens", "Enter the amount to mint:")
        if not amount or not self.token_address.get() or not self.token_account_address.get():
            messagebox.showerror("Error", "Please ensure a token is created and an amount is entered.")
            return
        command = ["spl-token", "mint", self.token_address.get(), amount, self.token_account_address.get()]
        output = run_command(command)
        if output:
            messagebox.showinfo("Success", f"Minted {amount} tokens to {self.token_account_address.get()}")
            logging.info(f"Minted {amount} tokens to {self.token_account_address.get()}")

if __name__ == "__main__":
    app = SPLTokenGUI()
    app.mainloop()
