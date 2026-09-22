import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ================= DATABASE SETUP =================
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    acc_num TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    pin TEXT NOT NULL,
    balance REAL NOT NULL
)
""")
conn.commit()

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("🏦Alfredo Ndwalane Banking App v1.0")
root.geometry("600x600")
root.config(bg="#e8f0f7")

# ================= FUNCTIONS =================
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# ---------------- ADMIN LOGIN ----------------
def admin_login_screen():
    clear_window()

    tk.Label(root, text="👨‍💼 Admin Login", font=("Arial", 20, "bold"), bg="#e8f0f7").pack(pady=20)

    tk.Label(root, text="Username:", bg="#e8f0f7").pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    tk.Label(root, text="Password:", bg="#e8f0f7").pack()
    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    def login_admin():
        user = user_entry.get()
        pwd = pass_entry.get()
        if user == "alfredon" and pwd == "@admin123":
            admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin credentials!")

    tk.Button(root, text="Login", command=login_admin, bg="#4CAF50", fg="white", width=15).pack(pady=10)
    tk.Button(root, text="Back", command=main_menu, bg="#888", fg="white", width=15).pack()

# ---------------- ADMIN PANEL ----------------
def admin_panel():
    clear_window()
    root.geometry("800x500")
    tk.Label(root, text="🏦 ADMIN PANEL", font=("Arial", 18, "bold"), bg="#e8f0f7").pack(pady=10)
    tk.Label(root, text="Manage Customers", font=("Arial", 14), bg="#e8f0f7").pack(pady=5)

    # Treeview
    tree = ttk.Treeview(root, columns=("acc", "name", "pin", "bal"), show="headings")
    tree.heading("acc", text="Account No")
    tree.heading("name", text="Name")
    tree.heading("pin", text="PIN")
    tree.heading("bal", text="Balance")
    tree.column("acc", width=100)
    tree.column("name", width=200)
    tree.column("pin", width=80)
    tree.column("bal", width=100, anchor="e")
    tree.pack(pady=10, fill="x")
    tree_scroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=tree_scroll.set)
    tree.pack(pady=10, fill="x")

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM customers")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

    refresh_table()

    # Input fields
    form = tk.Frame(root, bg="#e8f0f7")
    form.pack(pady=5)

    tk.Label(form, text="Account No:", bg="#e8f0f7").grid(row=0, column=0)
    tk.Label(form, text="Name:", bg="#e8f0f7").grid(row=1, column=0)
    tk.Label(form, text="PIN:", bg="#e8f0f7").grid(row=2, column=0)
    tk.Label(form, text="Balance:", bg="#e8f0f7").grid(row=3, column=0)
    
    acc_entry = tk.Entry(form)
    name_entry = tk.Entry(form)
    pin_entry = tk.Entry(form)
    bal_entry = tk.Entry(form)
    acc_entry.grid(row=0, column=1, padx=5, pady=2)
    name_entry.grid(row=1, column=1, padx=5, pady=2)
    pin_entry.grid(row=2, column=1, padx=5, pady=2)
    bal_entry.grid(row=3, column=1, padx=5, pady=2)

    def add_customer():
        acc = acc_entry.get().strip()
        name = name_entry.get().strip()
        pin = pin_entry.get().strip()
        bal = bal_entry.get().strip()
        if not (acc and name and pin and bal):
            messagebox.showerror("Error", "All fields required!")
            return
        try:
            cursor.execute("INSERT INTO customers VALUES (?, ?, ?, ?)", (acc, name, pin, float(bal)))
            conn.commit()
            refresh_table()
            acc_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            pin_entry.delete(0, tk.END)
            bal_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Customer added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Account already exists!")

    def delete_customer():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a customer to delete")
            return
        acc = tree.item(selected)["values"][0]
        cursor.execute("DELETE FROM customers WHERE acc_num=?", (acc,))
        conn.commit()
        refresh_table()
        messagebox.showinfo("Deleted", "Customer deleted successfully!")

    def update_customer():
        acc = acc_entry.get().strip()
        name = name_entry.get().strip()
        pin = pin_entry.get().strip()
        bal = bal_entry.get().strip()
        if not (acc and name and pin and bal):
            messagebox.showerror("Error", "All fields required!")
            return
        cursor.execute("UPDATE customers SET name=?, pin=?, balance=? WHERE acc_num=?",
        (name, pin, float(bal), acc))
        conn.commit()
        refresh_table()
        messagebox.showinfo("Updated", "Customer updated successfully!")
        
    def select_customer(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            acc_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            pin_entry.delete(0, tk.END)
            bal_entry.delete(0, tk.END)
            acc_entry.insert(0, values[0])
            name_entry.insert(0, values[1])
            pin_entry.insert(0, values[2])
            bal_entry.insert(0, values[3])

    tree.bind("<ButtonRelease-1>", select_customer)

    # Buttons
    btn_frame = tk.Frame(root, bg="#e8f0f7")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add", command=add_customer, bg="#4CAF50", fg="white", width=10).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Update", command=update_customer, bg="#2196F3", fg="white", width=10).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_customer, bg="#f44336", fg="white", width=10).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Refresh", command=refresh_table, bg="#9C27B0", fg="white", width=10).grid(row=0, column=3, padx=5)
    tk.Button(btn_frame, text="Logout", command=main_menu, bg="#555", fg="white", width=10).grid(row=0, column=4, padx=5)
    tk.Button(root, text="Back to Main Menu", command=main_menu, bg="#888", fg="white", width=20).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy, bg="#f44336", fg="white", width=20).pack(pady=5)
    tk.Button(root, text="Refresh Table", command=refresh_table, bg="#9C27B0", fg="white", width=20).pack(pady=5)
    tk.Button(root, text="Clear Input Fields", command=lambda: [acc_entry.delete(0, tk.END), name_entry.delete(0, tk.END), pin_entry.delete(0, tk.END), bal_entry.delete(0, tk.END)], bg="#FF9800", fg="white", width=20).pack(pady=5)

# ---------------- CUSTOMER LOGIN ----------------
def customer_login_screen():
    clear_window()
    root.geometry("600x600")
    tk.Label(root, text="👤 Customer Login", font=("Arial", 20, "bold"), bg="#e8f0f7").pack(pady=20)

    tk.Label(root, text="Account Number:", bg="#e8f0f7").pack()
    acc_entry = tk.Entry(root)
    acc_entry.pack()

    tk.Label(root, text="PIN:", bg="#e8f0f7").pack()
    pin_entry = tk.Entry(root, show="*")
    pin_entry.pack()

    def login_customer():
        acc = acc_entry.get()
        pin = pin_entry.get()
        cursor.execute("SELECT * FROM customers WHERE acc_num=? AND pin=?", (acc, pin))
        user = cursor.fetchone()
        if user:
            customer_panel(user)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    tk.Button(root, text="Login", command=login_customer, bg="#4CAF50", fg="white", width=15).pack(pady=10)
    tk.Button(root, text="Back", command=main_menu, bg="#888", fg="white", width=15).pack()

# ---------------- CUSTOMER PANEL ----------------
def customer_panel(user):
    clear_window()
    root.geometry("600x600")
    acc, name, pin, balance = user
    tk.Label(root, text=f"Welcome, {name}", font=("Arial", 18, "bold"), bg="#e8f0f7").pack(pady=15)

    balance_var = tk.StringVar(value=f"Balance: R{balance:.2f}")
    tk.Label(root, textvariable=balance_var, font=("Arial", 14), bg="#e8f0f7").pack(pady=10)

    def balance_check():
        cursor.execute("SELECT balance FROM customers WHERE acc_num=?", (acc,))
        return cursor.fetchone()[0]

    def update_balance(change):
        new_bal = balance_check() + change
        cursor.execute("UPDATE customers SET balance=? WHERE acc_num=?", (new_bal, acc))
        conn.commit()
        balance_var.set(f"Balance: R{new_bal:.2f}")

    def simple_input(title):
        top = tk.Toplevel(root)
        top.title(title)
        tk.Label(top, text=f"Enter {title}:", font=("Arial", 12)).pack(pady=5)
        entry = tk.Entry(top)
        entry.pack(pady=5)
        val = tk.DoubleVar()
        def submit():
            try:
                val.set(float(entry.get()))
                top.destroy()
            except:
                messagebox.showerror("Error", "Enter a valid number")
        tk.Button(top, text="OK", command=submit, bg="#4CAF50", fg="white").pack(pady=5)
        root.wait_window(top)
        return val.get() if val.get() != 0 else None

    def withdraw():
        amt = simple_input("Withdraw Amount")
        if amt is None:
            return
        if amt > 0 and amt <= balance_check():
            update_balance(-amt)
            messagebox.showinfo("Success", f"Withdrew R{amt:.2f}")
        else:
            messagebox.showerror("Error", "Invalid or insufficient funds")

    def deposit():
        amt = simple_input("Deposit Amount")
        if amt is None:
            return
        if amt > 0:
            update_balance(amt)
            messagebox.showinfo("Success", f"Deposited R{amt:.2f}")
        else:
            messagebox.showerror("Error", "Invalid amount")
    
    def change_pin():
        top = tk.Toplevel(root)
        top.title("Change PIN")

        tk.Label(top, text="Current PIN:", font=("Arial", 12)).pack(pady=5)
        current_pin = tk.Entry(top, show="*")
        current_pin.pack(pady=5)

        tk.Label(top, text="New PIN:", font=("Arial", 12)).pack(pady=5)
        new_pin = tk.Entry(top, show="*")
        new_pin.pack(pady=5)

        tk.Label(top, text="Confirm New PIN:", font=("Arial", 12)).pack(pady=5)
        confirm_pin = tk.Entry(top, show="*")
        confirm_pin.pack(pady=5)

        def save_pin():
            cur = current_pin.get()
            new = new_pin.get()
            conf = confirm_pin.get()

            cursor.execute("SELECT pin FROM customers WHERE acc_num=?", (acc,))
            old_pin = cursor.fetchone()[0]

            if cur != old_pin:
                messagebox.showerror("Error", "Current PIN is incorrect!")
            elif new != conf:
                messagebox.showerror("Error", "New PINs do not match!")
            elif len(new) < 4:
                messagebox.showerror("Error", "PIN must be at least 4 digits!")
            else:
                cursor.execute("UPDATE customers SET pin=? WHERE acc_num=?", (new, acc))
                conn.commit()
                messagebox.showinfo("Success", "PIN changed successfully!")
                top.destroy()

        tk.Button(top, text="Save", command=save_pin, bg="#2196F3", fg="white").pack(pady=10)

    # Buttons
    tk.Button(root, text="Withdraw", command=withdraw, bg="#f44336", fg="white", width=15).pack(pady=5)
    tk.Button(root, text="Deposit", command=deposit, bg="#4CAF50", fg="white", width=15).pack(pady=5)
    tk.Button(root, text="Change PIN", command=change_pin, bg="#FF9800", fg="white", width=15).pack(pady=5)
    tk.Button(root, text="Check Balance", command=lambda: messagebox.showinfo("Balance", f"Current Balance: R{balance_check():.2f}"), bg="#2196F3", fg="white", width=15).pack(pady=5)
    tk.Button(root, text="Logout", command=main_menu, bg="#555", fg="white", width=15).pack(pady=15)

# ---------------- MAIN MENU ----------------
def main_menu():
    clear_window()
    root.geometry("600x600")
    tk.Label(root, text="🏦 Bank Management System", font=("Arial", 18, "bold"), bg="#e8f0f7").pack(pady=40)
    tk.Button(root, text="Admin Login", command=admin_login_screen, bg="#2196F3", fg="white", width=20, height=2).pack(pady=10)
    tk.Button(root, text="Customer Login", command=customer_login_screen, bg="#4CAF50", fg="white", width=20, height=2).pack(pady=10)
    tk.Button(root, text="Exit", command=root.destroy, bg="#f44336", fg="white", width=20, height=2).pack(pady=10)

# Start App
main_menu()
root.mainloop()

