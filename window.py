import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Менеджер аккаунтов")
root.geometry("400x300")

label = ctk.CTkLabel(root, text="Привет, брат!", font=("Arial", 18))
label.pack(pady=20)

button = ctk.CTkButton(root, text="Нажми меня", command=lambda: label.configure(text="Тёмная тема работает!"))
button.pack()

root.mainloop()