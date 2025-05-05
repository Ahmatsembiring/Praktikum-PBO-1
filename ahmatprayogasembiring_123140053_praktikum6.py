import tkinter as tk
from tkinter import messagebox
import os
import csv

class UserManager:
    def __init__(self, filepath="users_data.csv"):
        self.filepath = filepath
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists(self.filepath):
            with open(self.filepath, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    users[row['username']] = row['password']
        return users

    def save_user(self, username, password):
        file_exists = os.path.isfile(self.filepath)
        with open(self.filepath, "a", newline="") as csvfile:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists or os.stat(self.filepath).st_size == 0:
                writer.writeheader()
            writer.writerow({'username': username, 'password': password})
        self.users[username] = password

    def validate_user(self, username, password):
        return self.users.get(username) == password

    def is_registered(self, username):
        return username in self.users


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Login")
        self.root.geometry("480x300")

        self.user_manager = UserManager()

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=40)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e", padx=10, pady=5)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1)
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", width=20, command=self.login_user).grid(row=2, column=0, columnspan=2, pady=15)
        tk.Button(self.login_frame, text="Belum punya akun? Daftar", command=self.open_register_window).grid(row=3, column=0, columnspan=2)

    def login_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Kosong", "Harap isi username dan password.")
            return

        if self.user_manager.validate_user(username, password):
            messagebox.showinfo("Login Sukses", f"Selamat datang, {username}!")
        else:
            messagebox.showerror("Gagal", "Username atau password salah.")

    def open_register_window(self):
        RegisterWindow(self.root, self.user_manager)


class RegisterWindow:
    def __init__(self, root, user_manager):
        self.window = tk.Toplevel(root)
        self.window.title("Daftar Akun Baru")
        self.window.geometry("480x300")

        self.user_manager = user_manager

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var = tk.StringVar()

        reg_frame = tk.Frame(self.window)
        reg_frame.pack(pady=30)

        tk.Label(reg_frame, text="Username:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        tk.Label(reg_frame, text="Password:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        tk.Label(reg_frame, text="Konfirmasi Password:").grid(row=2, column=0, sticky="e", padx=10, pady=5)

        tk.Entry(reg_frame, textvariable=self.username_var).grid(row=0, column=1)
        tk.Entry(reg_frame, textvariable=self.password_var, show="*").grid(row=1, column=1)
        tk.Entry(reg_frame, textvariable=self.confirm_var, show="*").grid(row=2, column=1)

        tk.Button(reg_frame, text="Daftar", width=20, command=self.register_user).grid(row=3, column=0, columnspan=2, pady=15)

    def register_user(self):
        uname = self.username_var.get().strip()
        pwd = self.password_var.get().strip()
        conf = self.confirm_var.get().strip()

        if not uname or not pwd:
            messagebox.showwarning("Input Kosong", "Username dan password tidak boleh kosong.")
            return

        if self.user_manager.is_registered(uname):
            messagebox.showerror("Gagal", "Username sudah terdaftar.")
            return

        if pwd != conf:
            messagebox.showerror("Gagal", "Password tidak sama dengan konfirmasi.")
            return

        self.user_manager.save_user(uname, pwd)
        messagebox.showinfo("Berhasil", "Registrasi berhasil. Silakan login.")
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
