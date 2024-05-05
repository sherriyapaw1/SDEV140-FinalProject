import tkinter as tk
from tkinter import messagebox, PhotoImage


# Main class for Finance Tracker
class FinanceTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Finance Tracker')
        self.geometry('600x400')  # Set initial size of the main window
        self.transactions = self.load_transactions()  # Load transactions from file

        # Load images for buttons
        self.img_add = PhotoImage(file="add_icon.png")
        self.img_view = PhotoImage(file="view_icon.png")
        self.img_settings = PhotoImage(file="settings_icon.png")
        self.img_exit = PhotoImage(file="exit_icon.png")

        # Set up the main menu interface
        self.main_menu()

    # Function to set up the main menu
    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text='Welcome to Finance Tracker!', font=('Arial', 24)).pack(pady=20)
        tk.Button(self, text='Add Transaction', image=self.img_add, compound="left", command=self.add_transaction).pack(
            fill='x')
        tk.Button(self, text='View Reports', image=self.img_view, compound="left", command=self.view_reports).pack(
            fill='x')
        tk.Button(self, text='Settings', image=self.img_settings, compound="left", command=self.settings).pack(fill='x')
        tk.Button(self, text='Exit', image=self.img_exit, compound="left", command=self.exit_app).pack(fill='x')

    # Open AddTransactionWindow
    def add_transaction(self):
        new_window = AddTransactionWindow(self)

    # Open ViewReportsWindow
    def view_reports(self):
        reports_window = ViewReportsWindow(self, self.transactions)

    # Open SettingsWindow
    def settings(self):
        settings_window = SettingsWindow(self)

    # Quit the application
    def exit_app(self):
        self.quit()

    # Loads transactions from a file
    def load_transactions(self):
        try:
            with open('transactions.txt', 'r') as file:
                transactions = file.readlines()
            return [x.strip() for x in transactions]
        except FileNotFoundError:
            return []

    # Saves transactions to a file
    def save_transactions(self):
        with open('transactions.txt', 'w') as file:
            for transaction in self.transactions:
                file.write(transaction + "\n")


# Function for adding transactions
class AddTransactionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry('400x300')
        self.title('Add Transaction')

        tk.Label(self, text='Add a New Transaction', font=('Arial', 18)).pack(pady=10)
        tk.Label(self, text='Amount:').pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()
        tk.Button(self, text='Submit', command=self.submit_transaction).pack(pady=10)

    def submit_transaction(self):
        amount = self.amount_entry.get()
        if amount:
            try:
                amount = float(amount)
                formatted_amount = f"+{amount:.2f}" if amount >= 0 else f"{amount:.2f}"
                self.parent.transactions.append(formatted_amount)
                self.parent.save_transactions()
                messagebox.showinfo("Success", "Transaction added successfully!")
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")


# Function for viewing stored transactions
class ViewReportsWindow(tk.Toplevel):

    def __init__(self, parent, transactions):
        super().__init__(parent)
        self.geometry('500x400')
        self.title('View Reports')

        # Calculate and display the total sum of transactions
        total = sum(float(transaction) for transaction in transactions)
        report_text = "\n".join(transactions) + f"\nBalance: {total:+.2f}"

        # Window layout
        tk.Label(self, text='Financial Reports', font=('Arial', 18)).pack(pady=20)
        report_label = tk.Label(self, text=report_text, justify=tk.LEFT, font=('Arial', 12))
        report_label.pack(side="left", fill="both", expand=True)


# Function for changing settings
class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('400x300')
        self.title('Settings')

        tk.Label(self, text='Settings', font=('Arial', 18)).pack(pady=20)
        tk.Button(self, text='Change Font Size', command=self.change_font_size).pack()

    # Opens a dialog to change the font size
    def change_font_size(self):
        dialog = FontSizeDialog(self)
        dialog.grab_set()


# Function for setting the font size
class FontSizeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('300x150')
        self.title('Change Font Size')

        tk.Label(self, text="Enter new font size:").pack(pady=10)
        self.font_size_entry = tk.Entry(self)
        self.font_size_entry.pack(pady=10)

        tk.Button(self, text="Submit", command=self.submit).pack(pady=10)

    def submit(self):
        new_size = self.font_size_entry.get()
        if new_size.isdigit():
            new_size = int(new_size)
            self.master.option_add("*Font", f'Arial {new_size}')
            messagebox.showinfo("Font Size Changed", f"Font size changed to {new_size}")
            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid font size entered. Please enter a valid number.")


def main():
    app = FinanceTrackerApp()
    app.mainloop()


if __name__ == '__main__':
    main()
