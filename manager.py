import customtkinter as ctk
import json
import os
import tkinter as tk
from tkinter import messagebox

FILE = "accounts.json"

def load_accounts():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)

accounts = load_accounts()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Менеджер аккаунтов")
root.geometry("650x820")

platforms = [
    "Steam",
    "Epic Games",
    "GOG",
    "Battle.net",
    "Telegram",
    "WhatsApp",
    "Viber",
    "Discord",
    "VK",
    "Одноклассники",
    "Instagram",
    "Facebook",
    "Google",
    "Yandex",
    "Mail.ru",
    "Тарков (EFT)",
    "Rust",
    "Apex Legends",
    "CS2",
    "Uplay",
    "Origin",
    "Rockstar Games",
    "Riot Games",
    "Другая"
]

def update_platform_field():
    if platform_menu.get() == "Другая":
        other_platform_entry.configure(state="normal")
    else:
        other_platform_entry.configure(state="disabled")

ctk.CTkLabel(root, text="Имя аккаунта:").pack(pady=(10, 0))
entry_name = ctk.CTkEntry(root, width=320)
entry_name.pack(pady=(0, 5))

ctk.CTkLabel(root, text="Логин:").pack(pady=(0, 0))
entry_login = ctk.CTkEntry(root, width=320)
entry_login.pack(pady=(0, 5))

ctk.CTkLabel(root, text="Пароль:").pack(pady=(0, 0))
entry_password = ctk.CTkEntry(root, width=320, show="*")
entry_password.pack(pady=(0, 5))

ctk.CTkLabel(root, text="Почта:").pack(pady=(0, 0))
entry_email = ctk.CTkEntry(root, width=320)
entry_email.pack(pady=(0, 5))

ctk.CTkLabel(root, text="Платформа:").pack(pady=(0, 0))
platform_menu = ctk.CTkComboBox(root, values=platforms, width=320, command=lambda e: update_platform_field())
platform_menu.set("Steam")
platform_menu.pack(pady=(0, 5))

other_platform_entry = ctk.CTkEntry(root, width=320, placeholder_text="Своя платформа")
other_platform_entry.pack(pady=(0, 5))
other_platform_entry.configure(state="disabled")

ctk.CTkLabel(root, text="Двухфакторка:").pack(pady=(0, 0))
twofa_var = ctk.StringVar(value="Нет")
ctk.CTkRadioButton(root, text="Да", variable=twofa_var, value="Да").pack()
ctk.CTkRadioButton(root, text="Нет", variable=twofa_var, value="Нет").pack()

ctk.CTkLabel(root, text="Поиск:").pack(pady=(10, 0))
search_entry = ctk.CTkEntry(root, width=320, placeholder_text="Введи имя аккаунта")
search_entry.pack(pady=(0, 5))

listbox = tk.Listbox(root, width=70, height=12, bg="#1e1e1e", fg="white", selectbackground="#3b82f6")
listbox.pack(pady=(10, 5))

detail_label = ctk.CTkLabel(root, text="Нажми на аккаунт, чтобы увидеть данные", font=("Arial", 12), wraplength=550)
detail_label.pack(pady=(5, 5))

def refresh_list():
    listbox.delete(0, "end")
    for acc in accounts:
        listbox.insert("end", f"{acc['name']} | {acc['login']} | {acc['platform']}")

def clear_fields():
    entry_name.delete(0, "end")
    entry_login.delete(0, "end")
    entry_password.delete(0, "end")
    entry_email.delete(0, "end")
    other_platform_entry.delete(0, "end")
    twofa_var.set("Нет")

def add_account():
    name = entry_name.get()
    login = entry_login.get()
    password = entry_password.get()
    email = entry_email.get()
    platform = platform_menu.get()
    twofa = twofa_var.get()

    if platform == "Другая":
        platform = other_platform_entry.get() or "Другая"

    if not name or not login:
        messagebox.showwarning("Внимание", "Имя и логин обязательны!")
        return

    account = {
        "name": name,
        "login": login,
        "password": password,
        "email": email,
        "platform": platform,
        "twofa": twofa,
    }

    accounts.append(account)
    save_accounts(accounts)
    refresh_list()
    clear_fields()

def delete_account():
    selection = listbox.curselection()
    if not selection:
        messagebox.showinfo("Инфо", "Сначала выбери аккаунт.")
        return

    index = selection[0]
    acc = accounts[index]

    answer = messagebox.askyesno("Удаление", f"Удалить {acc['name']}?")
    if answer:
        accounts.pop(index)
        save_accounts(accounts)
        refresh_list()
        detail_label.configure(text="Нажми на аккаунт, чтобы увидеть данные")

def search_accounts():
    query = search_entry.get().lower()
    listbox.delete(0, "end")

    for acc in accounts:
        if query in acc["name"].lower():
            listbox.insert("end", f"{acc['name']} | {acc['login']} | {acc['platform']}")

def show_account_details(event):
    selection = listbox.curselection()
    if not selection:
        return

    index = selection[0]
    acc = accounts[index]

    info = (
        f"Имя: {acc['name']} | "
        f"Логин: {acc['login']} | "
        f"Пароль: {acc['password']} | "
        f"Почта: {acc['email']} | "
        f"Платформа: {acc['platform']} | "
        f"Двухфакторка: {acc['twofa']}"
    )
    detail_label.configure(text=info)

listbox.bind("<<ListboxSelect>>", show_account_details)

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Добавить", command=add_account).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Удалить", command=delete_account).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Очистить", command=clear_fields).pack(side="left", padx=5)
ctk.CTkButton(button_frame, text="Поиск", command=search_accounts).pack(side="left", padx=5)

refresh_list()

root.mainloop()