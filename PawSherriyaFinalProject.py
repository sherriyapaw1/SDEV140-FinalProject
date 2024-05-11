import tkinter as tk
from tkinter import messagebox, PhotoImage, simpledialog, filedialog, ttk
import csv
from datetime import datetime

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

    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text='Welcome to Finance Tracker!', font=('Arial', 24)).pack(pady=20)
        tk.Button(self, text='Add Transaction', image=self.img_add, compound="left", command=self.add_transaction).pack(fill='x')
        tk.Button(self, text='View Reports', image=self.img_view, compound="left", command=self.view_reports).pack(fill='x')
        tk.Button(self, text='Settings', image=self.img_settings, compound="left", command=self.settings).pack(fill='x')
        tk.Button(self, text='Exit', image=self.img_exit, compound="left", command=self.exit_app).pack(fill='x')

    def add_transaction(self):
        new_window = AddTransactionWindow(self)

    def view_reports(self):
        reports_window = ViewReportsWindow(self, self.transactions)

    def settings(self):
        settings_window = SettingsWindow(self)

    def exit_app(self):
        self.quit()

    def load_transactions(self):
        try:
            with open('transactions.txt', 'r') as file:
                transactions = [line.strip().split(',') for line in file if line.strip()]
            return transactions
        except FileNotFoundError:
            return []

    def save_transactions(self):
        with open('transactions.txt', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.transactions)

# Add Transaction Window
class AddTransactionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry('400x300')
        self.title('Add Transaction')

        # Date
        tk.Label(self, text='Date (YYYY-MM-DD):').pack()
        self.date_entry = tk.Entry(self)
        self.date_entry.pack()

        # Category
        tk.Label(self, text='Category:').pack()
        self.category_var = tk.StringVar(self)
        self.category_option = ttk.Combobox(self, textvariable=self.category_var, values=["Food", "Rent", "Salary", "Entertainment", "Other"])
        self.category_option.pack()

        # Amount
        tk.Label(self, text='Amount: negative num for expense, positive num for income').pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        # Submit Button
        tk.Button(self, text='Submit', command=self.submit_transaction).pack(pady=10)

    def submit_transaction(self):
        date = self.date_entry.get()
        category = self.category_var.get()
        amount = self.amount_entry.get()
        if date and category and amount:
            try:
                datetime.strptime(date, '%Y-%m-%d')  # Validate date format
                formatted_amount = f"{float(amount):+.2f}"
                self.parent.transactions.append([date, category, formatted_amount])
                self.parent.save_transactions()
                messagebox.showinfo("Success", "Transaction added successfully!")
                self.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

# View Reports Window
class ViewReportsWindow(tk.Toplevel):
    def __init__(self, parent, transactions):
        super().__init__(parent)
        self.geometry('500x400')
        self.title('View Reports')

        # Category Filter
        tk.Label(self, text='Filter by:').pack()
        self.filter_var = tk.StringVar(self)
        self.filter_option = ttk.Combobox(self, textvariable=self.filter_var, values=["All", "Income", "Expenses"])
        self.filter_option.pack()
        self.filter_option.bind("<<ComboboxSelected>>", self.update_view)

        # Display Transactions
        self.transactions = transactions
        self.display = tk.Text(self, wrap='word')
        self.display.pack(pady=10, fill='both', expand=True)
        self.update_view()

    def update_view(self, event=None):
        filter = self.filter_var.get()
        filtered_transactions = [t for t in self.transactions if filter == "All" or (filter == "Income" and float(t[2]) > 0) or (filter == "Expenses" and float(t[2]) < 0)]
        report_text = "\n".join([",".join(t) for t in filtered_transactions])
        total = sum(float(t[2]) for t in filtered_transactions)
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, report_text + f"\n\nBalance: {total:+.2f}")

# Settings Window
class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('400x300')
        self.title('Settings')

        tk.Label(self, text='Settings', font=('Arial', 18)).pack(pady=20)
        tk.Button(self, text='Change Font Size', command=self.change_font_size).pack()

    def change_font_size(self):
        dialog = FontSizeDialog(self)
        dialog.grab_set()

# Font Size Dialog
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
